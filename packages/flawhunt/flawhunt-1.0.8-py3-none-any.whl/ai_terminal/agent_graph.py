from typing import TypedDict, Annotated, List, Union, Dict, Any, Literal
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import json
from rich.console import Console

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    loop_count: int
    last_tool: str

class AgentGraph:
    def __init__(self, llm, tools: List[BaseTool], system_prompt: str, verbose: bool = False):
        self.llm = llm
        self.tools = tools
        self.system_prompt = system_prompt
        self.verbose = verbose
        self.console = Console()
        
        # Bind tools to the LLM
        # Handle cases where llm.lc_model might be None or not support bind_tools
        if hasattr(llm.lc_model, "bind_tools"):
            self.model = llm.lc_model.bind_tools(tools)
        else:
            # Fallback if bind_tools is not supported (e.g. older models or wrong wrapper)
            # This is a critical fallback for stability
            self.model = llm.lc_model
            
        self.workflow = self._build_graph()
        
    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", self._execute_tools)
        workflow.add_node("loop_monitor", self._monitor_loop)

        workflow.set_entry_point("agent")

        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END,
                "loop_detected": "loop_monitor"
            }
        )

        workflow.add_edge("tools", "agent")
        workflow.add_edge("loop_monitor", "agent")

        return workflow.compile()

    def _call_model(self, state: AgentState):
        messages = state["messages"]
        
        # Ensure system prompt is the first message
        if not isinstance(messages[0], SystemMessage):
            messages = [SystemMessage(content=self.system_prompt)] + messages
        else:
            # Update system prompt just in case
            messages[0] = SystemMessage(content=self.system_prompt)
            
        with self.console.status("[bold green]Thinking...[/bold green]"):
            response = self.model.invoke(messages)
            
        return {"messages": [response]}

    def _execute_tools(self, state: AgentState):
        """Execute tools with visual progress feedback."""
        messages = state["messages"]
        last_message = messages[-1]
        tool_calls = last_message.tool_calls
        
        results = []
        
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_call_id = tool_call["id"]
            
            # Find the tool instance
            tool_instance = next((t for t in self.tools if t.name == tool_name), None)
            
            if tool_instance:
                status_msg = f"[bold cyan]Executing {tool_name}...[/bold cyan]"
                
                # Check if tool is interactive (might ask for user input)
                # Shell tools often ask for confirmation in safe mode
                # 'shell_run' corresponds to ShellTool, 'smart_shell' to SmartShellTool
                is_interactive = tool_name in ["shell_run", "shell", "smart_shell", "repl_tool"]
                
                try:
                    if is_interactive:
                        # For interactive tools, just print the status and run directly
                        # This avoids the spinner eating the input prompt
                        self.console.print(status_msg)
                        tool_output = tool_instance.invoke(tool_args)
                    else:
                        # For non-interactive tools, we can use the nice spinner
                        with self.console.status(status_msg):
                            tool_output = tool_instance.invoke(tool_args)
                            
                except Exception as e:
                    tool_output = f"Error executing {tool_name}: {str(e)}"
            else:
                tool_output = f"Error: Tool '{tool_name}' not found."
            
            results.append(ToolMessage(content=str(tool_output), tool_call_id=tool_call_id))
            
        return {"messages": results}

    def _should_continue(self, state: AgentState) -> Literal["continue", "end", "loop_detected"]:
        messages = state["messages"]
        last_message = messages[-1]
        
        # Check for tool calls
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            # Loop Detection Logic
            # Look back at previous AIMessages to see if we are repeating the exact same tool call
            # traversing backwards
            
            same_call_count = 0
            current_calls = last_message.tool_calls
            
            # We iterate backwards through messages, skipping ToolMessages, looking for AIMessages
            for msg in reversed(messages[:-1]):
                if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
                    if msg.tool_calls == current_calls:
                        same_call_count += 1
                    else:
                        # Sequence broken
                        break
                elif isinstance(msg, HumanMessage):
                    # User input breaks the loop check usually
                    break
            
            if same_call_count >= 2: # This means 3 times total (current + 2 previous)
                if self.verbose:
                    print(f"Loop detected: {current_calls[0].get('name')} called {same_call_count + 1} times.")
                return "loop_detected"
            
            return "continue"
            
        return "end"

    def _monitor_loop(self, state: AgentState):
        # This node is triggered when a loop is detected.
        # We inject a message to force the agent to rethink.
        
        hint = "SYSTEM_ALERT: You are repeating the exact same tool call continuously. This approach is not working. You MUST try a DIFFERENT tool or strategy. Do not call the same tool with the same arguments again."
        
        return {
            "messages": [HumanMessage(content=hint)],
            "loop_count": state.get("loop_count", 0) + 1
        }

    def invoke(self, user_input: str, conversation_history=None):
        # Initialize state with conversation history if available
        # meaningful context injection
        
        messages = [HumanMessage(content=user_input)]
        
        inputs = {
            "messages": messages,
            "loop_count": 0,
            "last_tool": ""
        }
        
        config = {"recursion_limit": 15} # Allow enough steps for complex tasks
        
        try:
            result = self.workflow.invoke(inputs, config=config)
            
            # robustly extract text
            last_message = result["messages"][-1]
            return last_message.content
        except Exception as e:
            # Fallback for stability
            return f"Error during execution: {str(e)}"
