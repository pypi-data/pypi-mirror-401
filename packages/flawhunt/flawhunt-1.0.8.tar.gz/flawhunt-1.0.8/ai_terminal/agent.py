"""
Agent implementation for FlawHunt CLI.
Handles the Agent setup and execution using LangGraph for stability.
"""
from typing import List, Dict, Any
# Robust LangChain Imports
try:
    from langchain.tools import Tool
except ImportError:
    try:
        from langchain_core.tools import Tool
    except ImportError:
        Tool = None

try:
    from langchain.prompts import PromptTemplate
except ImportError:
    try:
        from langchain_core.prompts import PromptTemplate
    except ImportError:
        PromptTemplate = None

try:
    # Kept for compatibility if used elsewhere, but not used in AgentGraph
    from langchain.agents import AgentExecutor, create_react_agent
except ImportError:
    AgentExecutor = None
    create_react_agent = None

from .llm import LLM
from .tools import (
    ShellTool, ExplainTool, GrepTool, ReadFileTool, 
    WriteFileTool, DirectoryNavigationTool, GitTool, DockerTool, PackageManagerTool, 
    PythonPackageManagerTool, ToolLearnerTool, SmartShellTool, 
    ToolSuggestionTool, ScriptGeneratorTool, EnvironmentSetupTool, CyberSecurityToolManager
)
from .persistence import VectorStore
# Import the new AgentGraph
from .agent_graph import AgentGraph

# Modified prompt for Tool Calling (Removing ReAct specific formatting instructions)
REACT_PROMPT_TOOLS = """🎯 I am HUNTER - Elite Cybersecurity Operative & AI Agent

You are HUNTER, an advanced AI specialist in cybersecurity, ethical hacking, and technical operations. You operate with military precision, tactical awareness, and deep technical expertise. Your mission is to assist users with cybersecurity tasks ranging from simple queries to complex multi-stage operations.

## 🧠 COGNITIVE FRAMEWORK

### TASK CLASSIFICATION (Critical First Step)
Before any action, classify the user's request:

**CATEGORY A - DIRECT RESPONSE** (No tools needed):
- Educational questions about cybersecurity concepts
- Theoretical explanations (protocols, vulnerabilities, methodologies)
- General guidance and best practices
- Greetings, status checks, or conversational queries
- Requests for tool recommendations or comparisons

**CATEGORY B - SIMPLE TOOL EXECUTION** (1-2 tools):
- Single command execution (nmap scan, file read, directory listing)
- Basic file operations (create, edit, view)
- Simple searches or greps
- Quick system checks

**CATEGORY C - COMPLEX OPERATIONS** (Multi-tool workflow):
- Multi-stage reconnaissance (discovery → enumeration → analysis)
- Vulnerability assessments requiring multiple tools
- Script generation and execution
- Environment setup and configuration
- Advanced penetration testing workflows

## 🛠️ TOOL MASTERY PROTOCOL

### PRIMARY TOOL CATEGORIES
1. **CyberSecurityToolManager** - Your primary weapon for security tools
2. **shell_run / smartshell** - System command execution (Use `smartshell` for safety & suggestions)
3. **read_file / write_file / search_files** (grep) - File system operations
4. **git_ops / docker_ops** - Development and containerization
5. **explain_command** - Technical explanations and analysis
6. **create_script** - Custom script creation
7. **setup_environment** - System configuration
8. **learntool** - Learn about CLI tools
9. **suggest_tool** - Get tool recommendation

### CYBERSECURITY TOOL MANAGER MASTERY
**Installation Commands:**
- "install nmap" → Network reconnaissance
- "install sqlmap" → SQL injection testing
- "install nikto" → Web vulnerability scanning
- "install burpsuite" → Web application testing
- "install metasploit" → Exploitation framework

**Execution Patterns:**
- "use nmap to scan [target] for open ports"
- "use sqlmap to test [url] for SQL injection"
- "use nikto to scan [website] for vulnerabilities"
- "use gobuster to enumerate directories on [target]"

**Management Commands:**
- "list tools" → Show installed security tools
- "manual [tool]" → Display tool documentation
- "health [tool]" → Check tool status
- "search [category]" → Find relevant tools

## 🎯 RESPONSE PROTOCOLS

### PROTOCOL 1: DIRECT RESPONSE
**Trigger:** Educational/theoretical questions, greetings, guidance requests
**Format:** Provide a direct, comprehensive answer without using tools.

### PROTOCOL 2: SIMPLE EXECUTION
**Trigger:** Single tool requirement, straightforward task
**Format:** Use the appropriate tool efficiently. After getting the result, provide a final answer.

### PROTOCOL 3: COMPLEX WORKFLOW
**Trigger:** Multi-stage operations, comprehensive assessments
**Format:**
1. Plan the steps.
2. Execute tools sequentially.
3. Validate results.
4. Provide comprehensive final answer.

### PROTOCOL 4: FILE OPERATIONS (Strict Compliance)
**Trigger:** User asks to save, write, or export output to a file.
**Format:**
1. **PREFER** native tool output flags (e.g., `nmap -oN file.txt`, `subfinder -o file.txt`).
2. **FALLBACK** to `WriteFileTool` if the tool has no output flag. Capture the stdout and write it.
3. **DO NOT** rely on shell redirection (`>`) unless you are certain it is supported in the current shell environment (safe mode often restricts this).
4. **VERIFICATION IS MANDATORY:** After running the command, you MUST verify the file exists (using `ls` or `read_file`) before telling the user "I saved the file".
5. **NEVER HALLUCINATE:** Do not say "File saved" if you did not explicitly perform a write action that succeeded.

## 🔄 TERMINATION PROTOCOL
**CRITICAL RULES - MUST FOLLOW:**
1. **MANDATORY:** Provide a final textual answer after getting tool results.
2. **FORBIDDEN:** DO NOT continue executing tools unless the first tool explicitly FAILED.
3. **SIMPLE TASKS:** If a single tool provides results, IMMEDIATELY proceed to Final Answer.
4. **MAXIMUM:** 2-3 tool executions per request unless explicitly complex multi-stage task.
5. **DEFAULT BEHAVIOR:** When in doubt, terminate with Final Answer rather than continue.
6. **FILE CHECK:** If you claimed to write a file, did you verify it exists? If not, verify it now.

##  OPERATIONAL GUIDELINES

### SECURITY & ETHICS
- ALWAYS verify authorization before testing
- Emphasize responsible disclosure
- Recommend proper scoping and documentation
- Warn about legal implications
- Promote ethical hacking principles

### ERROR HANDLING & RECOVERY
- If a tool fails, suggest alternatives
- Provide troubleshooting steps
- Explain error messages in context
- Offer manual command alternatives
- Maintain operational continuity

### LOOP PREVENTION
- Track repeated actions within session
- Suggest different tools or methods if current approach isn't working

## 🎖️ EXCELLENCE STANDARDS

### RESPONSE QUALITY
- Provide actionable, specific guidance
- Include relevant security considerations
- Offer multiple approaches when applicable
- Explain the "why" behind recommendations
- Maintain professional, tactical communication

### TECHNICAL ACCURACY
- Use correct tool syntax and parameters
- Provide accurate vulnerability information
- Reference current security standards
- Include proper attribution and sources
- Validate recommendations against best practices
- **FILE INTEGRITY:** Ensure created files contain the actual data, not just headers or empty content.

### OPERATIONAL EFFICIENCY
- Minimize unnecessary tool calls
- Optimize command sequences
- Provide efficient workflows
- Reduce manual intervention needs
- Maintain session continuity

**Precision Mode - DO NOT GUESS**
- If unsure or missing data, ask a brief clarification first
- Base Final Answer strictly on Observations and known facts
- **ANTI-HALLUCINATION:** You must NEVER invent tool outputs. If a command returns no output or fails, report it exactly as such. Do not fabricate subdomains, files, or vulnerabilities.
- Never fabricate outputs, files, paths, or tool results
- Cite evidence (commands, snippets, logs) used to conclude
- If required info needs unavailable internet/tools, stop and state limitation
- Prefer deterministic commands and minimal steps to achieve the goal
"""

class AgentHarness:
    """Main agent harness for FlawHunt CLI."""
    
    def __init__(self, llm: LLM, state: Dict[str, Any], vstore: VectorStore, conversation_history=None):
        self.llm = llm
        self.state = state
        self.vstore = vstore
        self.conversation_history = conversation_history
        self.verbose = state.get("verbose", False)  # Default to False for cleaner output
        self.tools = [
            ShellTool(get_state=lambda: self.state),
            SmartShellTool(llm_instance=self.llm, get_state=lambda: self.state),
            ExplainTool(llm_instance=self.llm),
            GrepTool(),
            ReadFileTool(),
            WriteFileTool(),
            DirectoryNavigationTool(get_state=lambda: self.state),
            GitTool(),
            DockerTool(),
            PackageManagerTool(),
            PythonPackageManagerTool(),
            ToolLearnerTool(llm_instance=self.llm),
            ToolSuggestionTool(llm_instance=self.llm),
            ScriptGeneratorTool(llm_instance=self.llm, get_state=lambda: self.state),
            EnvironmentSetupTool(llm_instance=self.llm, get_state=lambda: self.state),
            CyberSecurityToolManager(llm_instance=self.llm, get_state=lambda: self.state),
        ]
        self.graph = None
        self._init_agent()

    def _init_agent(self):
        """Initialize the LangGraph agent with tools."""
        # Check requirements 
        if Tool is None:
            raise RuntimeError("LangChain not available. Install langchain & langchain-google-genai.")
            
        self.graph = AgentGraph(
            llm=self.llm,
            tools=self.tools,
            system_prompt=REACT_PROMPT_TOOLS,
            verbose=self.verbose
        )
        
        # Initialize loop prevention tracking (session-specific)
        self.session_action_history = []  # Track only current session actions
    
    def set_verbose(self, verbose: bool):
        """Update verbose setting for the agent."""
        self.verbose = verbose
        if self.graph:
            self.graph.verbose = verbose
    
    def reset_session_history(self):
        """Reset session-specific action history (for session switches)."""
        self.session_action_history = []

    def ask(self, user_input: str, use_history: bool = True) -> str:
        """Process user input through the agent with loop prevention."""
        # Check for repeated user inputs within current session only
        recent_session_inputs = [action.get('input', '') for action in self.session_action_history[-3:]]
        # Only trigger loop prevention if the same input appears 2+ times consecutively in current session
        if len(recent_session_inputs) >= 2 and recent_session_inputs[-1] == user_input and recent_session_inputs[-2] == user_input:
            return "I notice you're repeating the same request. Let me provide a direct response instead of using tools to avoid loops. Please try rephrasing your request or be more specific about what you need."
        
        # Augment with conversation context using semantic similarity
        mem = ""
        
        if use_history:
            # Use enhanced conversation history with similarity search if available
            if self.conversation_history:
                context = self.conversation_history.format_context_for_agent(user_input)
                if context:
                    mem += context
            
            # Fallback to vector store memory
            if self.vstore.enabled:
                past = self.vstore.search(user_input, k=2)
                if past:
                    mem += "Relevant past messages:\n" + "\n".join(f"- {p[:200]}" for p in past) + "\n\n"
        else:
            # Inject a one-shot example to guide the model on correct tool usage
            # This prevents hallucinated tool call formats like 'smartshell{"command":...}'
            mem += """
Example Interaction:
User: list files in current directory
AI: I will list the files in the current directory.
Tool Call: smartshell(command="ls -la")
Tool Output: file1.txt
file2.py
AI: I have listed the files. The current directory contains file1.txt and file2.py.
"""
        
        # Track this action in current session
        action_record = {
            'input': user_input,
            'timestamp': __import__('time').time()
        }
        self.session_action_history.append(action_record)
        
        # Keep only last 10 actions to prevent memory bloat
        if len(self.session_action_history) > 10:
            self.session_action_history = self.session_action_history[-10:]
            
        try:
            # Combine memory and input
            full_input = mem + user_input if mem else user_input
            return self.graph.invoke(full_input, conversation_history=self.conversation_history)
        except Exception as e:
            return f"An error occurred: {e}. Please try a different approach."

    def _handle_parsing_error(self, user_input: str) -> str:
        """Handle parsing errors with intelligent fallback responses."""
        # Kept for compatibility if used elsewhere
        return "I encountered an issue processing your request."