#!/usr/bin/env python3
"""
Enhanced AI Terminal (safe-by-default)
Natural language to shell with dynamic tool installation and learning
Gemini + LangChain ReAct agent with adaptive tool generation

Features:
- Dynamic package installation (system & Python)
- Automatic tool discovery and command generation
- Learning from man pages and help output
- Smart command suggestions and auto-completion
- Enhanced memory with tool knowledge persistence

Requirements (install as needed):
pip install google-generativeai langchain langchain-google-genai prompt_toolkit typer rich faiss-cpu sentence-transformers requests beautifulsoup4

Environment:
export GEMINI_API_KEY=your_key

Run:
python enhanced_ai_terminal.py
"""

import os
import re
import json
import shlex
import signal
import subprocess
import sys
import time
import platform
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable, ClassVar, Set
from concurrent.futures import ThreadPoolExecutor, as_completed

# Third-party imports
try:
    import google.generativeai as genai
except Exception:
    genai = None

try:
    from langchain.tools import BaseTool
    from langchain.agents import Tool, AgentExecutor, create_react_agent
    from langchain.prompts import PromptTemplate
    from langchain_google_genai import ChatGoogleGenerativeAI
except Exception:
    BaseTool = object
    Tool = None
    AgentExecutor = None
    create_react_agent = None
    PromptTemplate = None
    ChatGoogleGenerativeAI = None

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.completion import WordCompleter
except Exception:
    PromptSession = None

try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
except Exception:
    faiss = None
    np = None
    SentenceTransformer = None

try:
    import requests
    from bs4 import BeautifulSoup
except Exception:
    requests = None
    BeautifulSoup = None

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
from rich.progress import track
from rich import box

console = Console()

def shutil_which(bin_name: str) -> Optional[str]:
    """Cross-platform which command."""
    from shutil import which
    return which(bin_name)

# Configuration
APP_DIR = Path.home() / ".ai_terminal"
APP_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = APP_DIR / "state.json"
TOOLS_DB_FILE = APP_DIR / "tools_knowledge.json"
VECTOR_FILE = APP_DIR / "vector.pkl"
FAISS_FILE = str(APP_DIR / "faiss.index")
HISTORY_FILE = str(APP_DIR / "repl_history.txt")
DEFAULT_MODEL = "moonshotai/kimi-k2-instruct-0905 "
GEMINI_API_KEY = ""

# Platform Detection
def get_platform_info():
    """Get platform-specific information."""
    system = platform.system().lower()
    return {
        "system": system,
        "is_windows": system == "windows",
        "is_linux": system == "linux",
        "is_darwin": system == "darwin",
        "shell_executable": get_shell_executable(system),
        "path_separator": "\\" if system == "windows" else "/",
        "package_manager": get_package_manager(system),
    }

def get_shell_executable(system: str) -> Optional[str]:
    """Get the appropriate shell executable for the platform."""
    if system == "windows":
        for shell in ["powershell.exe", "cmd.exe"]:
            if shutil_which(shell):
                return shell
        return "cmd.exe"
    else:
        for shell in ["/bin/bash", "/bin/sh", "/bin/zsh"]:
            if Path(shell).exists():
                return shell
        return "/bin/sh"

def get_package_manager(system: str) -> str:
    """Detect the system package manager."""
    if system == "linux":
        if shutil_which("apt"):
            return "apt"
        elif shutil_which("yum"):
            return "yum"
        elif shutil_which("dnf"):
            return "dnf"
        elif shutil_which("pacman"):
            return "pacman"
        elif shutil_which("zypper"):
            return "zypper"
    elif system == "darwin":
        if shutil_which("brew"):
            return "brew"
        elif shutil_which("port"):
            return "port"
    elif system == "windows":
        if shutil_which("choco"):
            return "choco"
        elif shutil_which("winget"):
            return "winget"
    return "unknown"

PLATFORM_INFO = get_platform_info()

# Enhanced Safety Patterns
DANGEROUS_PATTERNS = [
    # Unix/Linux dangerous patterns
    r"rm\s+-rf\s+/\b",
    r":\s*\{\s*:\s*\|\s*:\s*&\s*\};\s*:",  # fork bomb
    r"mkfs\.",
    r"dd\s+if=",
    r"^\s*shutdown\b",
    r"^\s*reboot\b",
    r"^\s*halt\b",
    r"\biptables\b.*\bflush\b",
    r"\bchown\s+-R\s+root\b",
    r"\bchmod\s+0{3,4}\b",
    # Windows dangerous patterns
    r"\bdel\s+/[sq]\s+C:\\\*",
    r"\brd\s+/[sq]\s+C:\\",
    r"\bformat\s+C:",
    r"\bfdisk\s+",
    r"\bdiskpart\b",
    r"\breg\s+delete\s+HKLM",
    r"\breg\s+delete\s+HKCU",
    r"\bnetsh\s+firewall\s+set\s+opmode\s+disable",
    # Network/Security sensitive
    r"\bcurl\b.*\|\s*bash",
    r"\bwget\b.*\|\s*bash",
    r"\bsudo\s+.*\s+-rf\s+/",
]

def looks_dangerous(cmd: str) -> bool:
    """Check if a command looks dangerous."""
    for pat in DANGEROUS_PATTERNS:
        if re.search(pat, cmd, re.IGNORECASE):
            return True
    return False

# Persistence
def load_state() -> Dict[str, Any]:
    """Load application state."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            pass
    return {
        "safe_mode": True,
        "use_faiss": False,
        "model": DEFAULT_MODEL,
        "memory": [],
        "installed_tools": set(),
        "auto_install": False,
        "learning_mode": True,
    }

def save_state(state: Dict[str, Any]) -> None:
    """Save application state."""
    # Convert set to list for JSON serialization
    state_copy = state.copy()
    if "installed_tools" in state_copy and isinstance(state_copy["installed_tools"], set):
        state_copy["installed_tools"] = list(state_copy["installed_tools"])
    STATE_FILE.write_text(json.dumps(state_copy, indent=2))

def load_tools_knowledge() -> Dict[str, Any]:
    """Load tools knowledge database."""
    if TOOLS_DB_FILE.exists():
        try:
            return json.loads(TOOLS_DB_FILE.read_text())
        except Exception:
            pass
    return {"tools": {}, "last_updated": 0}

def save_tools_knowledge(knowledge: Dict[str, Any]) -> None:
    """Save tools knowledge database."""
    knowledge["last_updated"] = time.time()
    TOOLS_DB_FILE.write_text(json.dumps(knowledge, indent=2))

# Enhanced Vector Store
@dataclass
class EnhancedVectorStore:
    enabled: bool = False
    model_name: str = "all-MiniLM-L6-v2"
    encoder: Any = None
    index: Any = None
    texts: List[str] = field(default_factory=list)
    metadata: List[Dict] = field(default_factory=list)

    def __post_init__(self):
        if faiss is not None and SentenceTransformer is not None:
            try:
                self.encoder = SentenceTransformer(self.model_name)
                dim = self.encoder.get_sentence_embedding_dimension()
                self.index = faiss.IndexFlatL2(dim)
                self.enabled = True
                if Path(FAISS_FILE).exists():
                    try:
                        self.index = faiss.read_index(FAISS_FILE)
                        # Load metadata
                        if VECTOR_FILE.exists():
                            import pickle
                            with open(VECTOR_FILE, 'rb') as f:
                                data = pickle.load(f)
                                self.texts = data.get('texts', [])
                                self.metadata = data.get('metadata', [])
                    except Exception:
                        pass
            except Exception:
                self.enabled = False

    def add(self, text: str, metadata: Dict = None):
        """Add text with optional metadata to the vector store."""
        if not self.enabled:
            return
        vec = self.encoder.encode([text]).astype("float32")
        self.index.add(vec)
        self.texts.append(text)
        self.metadata.append(metadata or {})
        self._save()

    def search(self, query: str, k: int = 3, filter_type: str = None) -> List[Dict]:
        """Search with optional filtering by metadata type."""
        if not self.enabled or self.index is None or self.index.ntotal == 0:
            return []
        
        q = self.encoder.encode([query]).astype("float32")
        D, I = self.index.search(q, min(k * 2, self.index.ntotal))
        
        results = []
        for idx, score in zip(I[0], D[0]):
            if 0 <= idx < len(self.texts):
                meta = self.metadata[idx] if idx < len(self.metadata) else {}
                if filter_type is None or meta.get("type") == filter_type:
                    results.append({
                        "text": self.texts[idx],
                        "metadata": meta,
                        "score": float(score)
                    })
                if len(results) >= k:
                    break
        
        return results

    def _save(self):
        """Save the vector store to disk."""
        try:
            faiss.write_index(self.index, FAISS_FILE)
            import pickle
            with open(VECTOR_FILE, 'wb') as f:
                pickle.dump({
                    'texts': self.texts,
                    'metadata': self.metadata
                }, f)
        except Exception:
            pass

# Enhanced LLM Wrapper
class EnhancedLLM:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.langchain_mode = False
        self.lc_model = None
        
        if ChatGoogleGenerativeAI is not None and GEMINI_API_KEY:
            try:
                self.lc_model = ChatGoogleGenerativeAI(
                    model=model, 
                    google_api_key=GEMINI_API_KEY, 
                    temperature=0.2,
                    max_output_tokens=4000
                )
                self.langchain_mode = True
            except Exception as e:
                console.print(f"[yellow]LangChain Google GenAI init failed: {e}[/yellow]")
        
        if not self.langchain_mode and genai is not None and GEMINI_API_KEY:
            genai.configure(api_key=GEMINI_API_KEY)
            try:
                self.sdk_model = genai.GenerativeModel(model_name=model)
            except Exception as e:
                console.print(f"[red]Gemini SDK init failed: {e}[/red]")
                self.sdk_model = None
        else:
            self.sdk_model = None

    def invoke(self, prompt: str) -> str:
        """Invoke the LLM with a prompt."""
        if self.langchain_mode and self.lc_model is not None:
            resp = self.lc_model.invoke(prompt)
            return getattr(resp, "content", str(resp))
        
        if self.sdk_model is not None:
            resp = self.sdk_model.generate_content(prompt)
            return getattr(resp, "text", str(resp))
        
        raise RuntimeError("No LLM available. Set GEMINI_API_KEY and install deps.")

    def generate_command_help(self, tool_name: str, help_text: str) -> str:
        """Generate intelligent command help using LLM."""
        prompt = f"""
Analyze this command-line tool and generate a concise usage guide:

Tool: {tool_name}
Help/Manual Text:
{help_text[:3000]}

Generate a structured response with:
1. Brief description (1-2 sentences)
2. Most common use cases (3-5 examples)
3. Important flags/options
4. Example commands with explanations

Keep it practical and focus on real-world usage.
"""
        try:
            return self.invoke(prompt)
        except Exception as e:
            return f"Error generating help: {e}"

# Utility Functions
def run_subprocess(cmd: str, timeout: int = 60, capture_stderr: bool = True) -> str:
    """Run a shell command safely in a subprocess."""
    try:
        if PLATFORM_INFO["is_windows"]:
            p = subprocess.run(
                cmd, shell=True, text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT if capture_stderr else subprocess.PIPE,
                timeout=timeout, encoding='utf-8', errors='replace'
            )
        else:
            p = subprocess.run(
                cmd, shell=True, text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT if capture_stderr else subprocess.PIPE,
                timeout=timeout,
                executable=PLATFORM_INFO["shell_executable"],
                encoding='utf-8', errors='replace'
            )
        return p.stdout.strip() if p.stdout else ""
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Error running command: {e}"

def extract_tool_info(tool_name: str) -> Dict[str, str]:
    """Extract comprehensive information about a tool."""
    info = {"name": tool_name, "help": "", "man": "", "version": "", "location": ""}
    
    # Get tool location
    if PLATFORM_INFO["is_windows"]:
        info["location"] = run_subprocess(f"where {tool_name}", timeout=10)
    else:
        info["location"] = run_subprocess(f"which {tool_name}", timeout=10)
    
    # Get version info
    for flag in ["--version", "-version", "-V", "/?"]:
        version = run_subprocess(f"{tool_name} {flag}", timeout=10)
        if version and "not found" not in version.lower():
            info["version"] = version[:500]
            break
    
    # Get help info
    for flag in ["--help", "-help", "-h", "/?"]:
        help_text = run_subprocess(f"{tool_name} {flag}", timeout=15)
        if help_text and "not found" not in help_text.lower():
            info["help"] = help_text[:2000]
            break
    
    # Get man page (Unix-like systems only)
    if not PLATFORM_INFO["is_windows"]:
        man_text = run_subprocess(f"MANWIDTH=90 man {tool_name} | col -b | head -n 200", timeout=20)
        if man_text and "No manual entry" not in man_text:
            info["man"] = man_text[:3000]
    
    return info

# Enhanced Tools
class PackageManagerTool(BaseTool):
    name: str = "package_manager"
    description: str = "Install system packages using the detected package manager. Input: package_name or 'search package_name'"
    get_state: Callable[[], Dict[str, Any]]

    def __init__(self, get_state: Callable[[], Dict[str, Any]]):
        super().__init__(get_state=get_state)

    def _run(self, query: str) -> str:
        query = query.strip()
        if not query:
            return "Provide a package name or 'search <term>'"

        pm = PLATFORM_INFO["package_manager"]
        if pm == "unknown":
            return "No supported package manager detected"

        state = self.get_state()
        
        if query.startswith("search "):
            search_term = query[7:].strip()
            return self._search_package(pm, search_term)
        else:
            return self._install_package(pm, query, state)

    def _search_package(self, pm: str, term: str) -> str:
        """Search for packages."""
        commands = {
            "apt": f"apt search {term}",
            "yum": f"yum search {term}",
            "dnf": f"dnf search {term}",
            "pacman": f"pacman -Ss {term}",
            "brew": f"brew search {term}",
            "choco": f"choco search {term}",
            "winget": f"winget search {term}"
        }
        
        cmd = commands.get(pm)
        if not cmd:
            return f"Search not implemented for {pm}"
        
        return run_subprocess(cmd, timeout=30)

    def _install_package(self, pm: str, package: str, state: Dict) -> str:
        """Install a package."""
        install_commands = {
            "apt": f"sudo apt update && sudo apt install -y {package}",
            "yum": f"sudo yum install -y {package}",
            "dnf": f"sudo dnf install -y {package}",
            "pacman": f"sudo pacman -S --noconfirm {package}",
            "brew": f"brew install {package}",
            "choco": f"choco install {package} -y",
            "winget": f"winget install {package}"
        }
        
        cmd = install_commands.get(pm)
        if not cmd:
            return f"Installation not supported for {pm}"

        if not state.get("auto_install", False):
            console.print(f"[yellow]About to run:[/yellow] {cmd}")
            if not Confirm.ask("Proceed with installation?", default=False):
                return "Installation canceled"

        result = run_subprocess(cmd, timeout=300)
        
        # Mark as installed and learn about it
        if "successfully" in result.lower() or "installed" in result.lower():
            state.setdefault("installed_tools", set()).add(package)
            return f"Successfully installed {package}\n{result[:500]}"
        
        return result

    async def _arun(self, query: str) -> str:
        return self._run(query)

class PythonPackageManagerTool(BaseTool):
    name: str = "python_packages"
    description: str = "Install Python packages using pip. Input: 'install package_name' or 'search package_name' or 'list'"

    def _run(self, query: str) -> str:
        query = query.strip()
        if not query:
            return "Provide: 'install <package>', 'search <package>', or 'list'"

        parts = query.split(maxsplit=1)
        action = parts[0].lower()
        
        if action == "list":
            return run_subprocess("pip list", timeout=30)
        
        if len(parts) < 2:
            return "Provide package name after action"
        
        package = parts[1]
        
        if action == "search":
            # Use PyPI API for search since pip search is deprecated
            try:
                if requests is None:
                    return "requests library not available for search"
                
                response = requests.get(f"https://pypi.org/search/?q={package}", timeout=10)
                if response.status_code == 200 and BeautifulSoup is not None:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    results = []
                    for result in soup.find_all('a', class_='package-snippet')[:10]:
                        name = result.find('span', class_='package-snippet__name')
                        desc = result.find('p', class_='package-snippet__description')
                        if name:
                            results.append(f"{name.text}: {desc.text if desc else 'No description'}")
                    return "\n".join(results) if results else "No packages found"
                else:
                    return f"Search failed: HTTP {response.status_code}"
            except Exception as e:
                return f"Search error: {e}"
        
        elif action == "install":
            if not Confirm.ask(f"Install Python package '{package}'?", default=False):
                return "Installation canceled"
            
            result = run_subprocess(f"pip install {package}", timeout=180)
            if "Successfully installed" in result:
                return f"Successfully installed {package}"
            return result
        
        else:
            return "Supported actions: install, search, list"

    async def _arun(self, query: str) -> str:
        return self._run(query)

class ToolLearnerTool(BaseTool):
    name: str = "learn_tool"
    description: str = "Learn about an installed command-line tool by reading its manual and help. Input: tool_name"
    
    def __init__(self, llm: EnhancedLLM, vstore: EnhancedVectorStore, knowledge_db: Dict):
        super().__init__()
        self._llm = llm
        self._vstore = vstore
        self._knowledge_db = knowledge_db

    def _run(self, tool_name: str) -> str:
        tool_name = tool_name.strip()
        if not tool_name:
            return "Provide a tool name to learn about"

        # Check if tool exists
        if not shutil_which(tool_name):
            return f"Tool '{tool_name}' not found in PATH"

        # Check if we already have knowledge about this tool
        if tool_name in self._knowledge_db.get("tools", {}):
            cached = self._knowledge_db["tools"][tool_name]
            age = time.time() - cached.get("learned_at", 0)
            if age < 7 * 24 * 3600:  # 7 days
                return f"Already learned about {tool_name}. Use ':toolhelp {tool_name}' to see details."

        console.print(f"[yellow]Learning about {tool_name}...[/yellow]")
        
        # Extract tool information
        tool_info = extract_tool_info(tool_name)
        
        # Generate intelligent help using LLM
        help_text = tool_info.get("help", "") + "\n" + tool_info.get("man", "")
        if help_text.strip():
            intelligent_help = self._llm.generate_command_help(tool_name, help_text)
        else:
            intelligent_help = "No help text available"

        # Store in knowledge database
        self._knowledge_db.setdefault("tools", {})[tool_name] = {
            "info": tool_info,
            "intelligent_help": intelligent_help,
            "learned_at": time.time(),
            "usage_count": 0
        }
        save_tools_knowledge(self._knowledge_db)

        # Add to vector store
        if self._vstore.enabled:
            self._vstore.add(
                f"Tool: {tool_name}\n{intelligent_help}",
                {"type": "tool", "name": tool_name}
            )

        return f"Successfully learned about {tool_name}!\n\n{intelligent_help[:800]}..."

    async def _arun(self, tool_name: str) -> str:
        return self._run(tool_name)

class SmartShellTool(BaseTool):
    name: str = "smart_shell"
    description: str = "Execute shell commands with intelligent suggestions and safety checks."
    
    def __init__(self, get_state: Callable, knowledge_db: Dict, vstore: EnhancedVectorStore):
        super().__init__()
        self._get_state = get_state
        self._knowledge_db = knowledge_db
        self._vstore = vstore

    def _run(self, command: str) -> str:
        command = command.strip()
        state = self._get_state()
        
        if looks_dangerous(command):
            return "Blocked: command flagged as dangerous."

        # Extract command name for intelligent suggestions
        cmd_parts = shlex.split(command) if not PLATFORM_INFO["is_windows"] else command.split()
        if cmd_parts:
            cmd_name = cmd_parts[0]
            
            # Check if we have knowledge about this tool
            if cmd_name in self._knowledge_db.get("tools", {}):
                tool_info = self._knowledge_db["tools"][cmd_name]
                tool_info["usage_count"] = tool_info.get("usage_count", 0) + 1
                save_tools_knowledge(self._knowledge_db)
            
            # Suggest learning if unknown tool
            elif shutil_which(cmd_name) and cmd_name not in ["ls", "cd", "pwd", "echo", "cat"]:
                console.print(f"[dim]Hint: Use 'learn_tool {cmd_name}' to get intelligent help for this tool[/dim]")

        if state.get("safe_mode", True):
            confirmed = Confirm.ask(f"[bold]Run[/bold] [cyan]{command}[/cyan]?", default=False)
            if not confirmed:
                return "Canceled."

        result = run_subprocess(command)
        
        # Learn from successful commands
        if self._vstore.enabled and result and "command not found" not in result.lower():
            self._vstore.add(
                f"Command: {command}\nResult: {result[:500]}",
                {"type": "command", "command": command}
            )
        
        return result

    async def _arun(self, command: str) -> str:
        return self._run(command)

class ToolSuggestionTool(BaseTool):
    name: str = "suggest_tools"
    description: str = "Suggest tools for a specific task. Input: description of what you want to do"
    
    def __init__(self, llm: EnhancedLLM, knowledge_db: Dict):
        super().__init__()
        self._llm = llm
        self._knowledge_db = knowledge_db

    def _run(self, task_description: str) -> str:
        task_description = task_description.strip()
        if not task_description:
            return "Describe what you want to accomplish"

        # Get list of known tools
        known_tools = list(self._knowledge_db.get("tools", {}).keys())
        
        # Common tool suggestions by category
        tool_categories = {
            "text processing": ["awk", "sed", "grep", "cut", "sort", "uniq", "jq"],
            "file operations": ["find", "rsync", "tar", "zip", "unzip"],
            "network": ["curl", "wget", "netstat", "ss", "ping", "nmap"],
            "system monitoring": ["htop", "iotop", "df", "du", "free", "ps"],
            "development": ["git", "make", "docker", "kubectl", "npm", "pip"],
            "media": ["ffmpeg", "imagemagick", "youtube-dl"],
        }

        # Use LLM to suggest appropriate tools
        prompt = f"""
Given this task: "{task_description}"

Suggest 3-5 command-line tools that would be helpful, prioritizing:
1. Tools from this known list: {', '.join(known_tools[:20])}
2. Common tools for the task type

For each suggestion, provide:
- Tool name
- Why it's relevant
- Basic usage example

Task: {task_description}
"""
        
        try:
            suggestions = self._llm.invoke(prompt)
            return suggestions
        except Exception as e:
            # Fallback to simple matching
            suggestions = []
            for category, tools in tool_categories.items():
                if any(word in task_description.lower() for word in category.split()):
                    suggestions.extend(tools[:3])
            
            if suggestions:
                return f"Suggested tools for '{task_description}':\n" + "\n".join(f"- {tool}" for tool in suggestions[:5])
            else:
                return "No specific tool suggestions found. Try describing your task differently."

    async def _arun(self, task_description: str) -> str:
        return self._run(task_description)

# Enhanced Agent with Dynamic Tools
ENHANCED_REACT_PROMPT = """You are an enhanced AI terminal assistant with dynamic tool capabilities. You can:

1. Install system packages and Python packages
2. Learn about new tools by reading their documentation
3. Suggest appropriate tools for tasks
4. Execute commands with intelligent assistance
5. Remember and learn from interactions

Always explain what you're doing and suggest better alternatives when possible.

Available tools: {tools}

Use this format:
Question: the input question you must answer
Thought: think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought:{agent_scratchpad}"""

class EnhancedAgentHarness:
    def __init__(self, llm: EnhancedLLM, state: Dict[str, Any], vstore: EnhancedVectorStore):
        self.llm = llm
        self.state = state
        self.vstore = vstore
        self.knowledge_db = load_tools_knowledge()
        
        # Convert installed_tools back to set if it's a list
        if "installed_tools" in state and isinstance(state["installed_tools"], list):
            state["installed_tools"] = set(state["installed_tools"])
        
        self.tools = self._create_tools()
        self.executor = None
        self._init_agent()

    def _create_tools(self) -> List[BaseTool]:
        """Create the list of available tools."""
        tools = [
            PackageManagerTool(get_state=lambda: self.state),
            PythonPackageManagerTool(),
            ToolLearnerTool(self.llm, self.vstore, self.knowledge_db),
            SmartShellTool(lambda: self.state, self.knowledge_db, self.vstore),
            ToolSuggestionTool(self.llm, self.knowledge_db),
            # Keep the original tools for compatibility
            ExplainTool(),
            GrepTool(),
            ReadFileTool(),
            WriteFileTool(),
            GitTool(),
            DockerTool(),
        ]
        return tools

    def _init_agent(self):
        """Initialize the LangChain agent."""
        if create_react_agent is None or Tool is None or AgentExecutor is None or PromptTemplate is None:
            raise RuntimeError("LangChain not available. Install langchain & langchain-google-genai.")

        tools = [Tool.from_function(t._run, name=t.name, description=t.description) for t in self.tools]
        prompt = PromptTemplate.from_template(ENHANCED_REACT_PROMPT)
        
        agent = create_react_agent(self.llm.lc_model, tools=tools, prompt=prompt)
        self.executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=False, 
            handle_parsing_errors=True,
            max_iterations=6
        )

    def ask(self, user_input: str) -> str:
        """Process user input with enhanced context."""
        # Augment with relevant context
        context_parts = []
        
        # Add tool knowledge context
        if self.vstore.enabled:
            tool_context = self.vstore.search(user_input, k=3, filter_type="tool")
            if tool_context:
                context_parts.append("Relevant tool knowledge:")
                for item in tool_context:
                    context_parts.append(f"- {item['text'][:200]}...")
        
        # Add command history context
        if self.vstore.enabled:
            cmd_context = self.vstore.search(user_input, k=2, filter_type="command")
            if cmd_context:
                context_parts.append("Similar commands used before:")
                for item in cmd_context:
                    context_parts.append(f"- {item['text'][:150]}...")
        
        # Add installed tools context
        installed = self.state.get("installed_tools", set())
        if installed:
            context_parts.append(f"Recently installed tools: {', '.join(list(installed)[-10:])}")

        context = "\n".join(context_parts)
        if context:
            context += "\n\n"

        try:
            result = self.executor.invoke({"input": context + user_input})
            return result.get("output", "No response generated")
        except Exception as e:
            return f"[Agent error] {e}\n\nTry simplifying your request or use direct commands."

# Original Tools (Enhanced)
class ExplainTool(BaseTool):
    name: str = "explain_command"
    description: str = "Explain what a shell command would do. Enhanced with platform-specific help."

    def _run(self, command: str) -> str:
        command = command.strip()
        if not command:
            return "Provide a command to explain."

        parts = shlex.split(command) if not PLATFORM_INFO["is_windows"] else command.split()
        head = parts[0] if parts else command
        info = []

        if PLATFORM_INFO["is_windows"]:
            # Windows-specific explanations
            info.append(f"Command location: {run_subprocess(f'where {head}')}")
            info.append(f"Built-in help: {run_subprocess(f'help {head}')}")
            if "powershell" in PLATFORM_INFO["shell_executable"].lower():
                info.append(f"PowerShell help: {run_subprocess(f'powershell -Command \"Get-Help {head} -ErrorAction SilentlyContinue\"')}")
        else:
            # Unix-like systems
            info.append(f"Command type: {run_subprocess(f'type -a {shlex.quote(head)}')}")
            info.append(f"Command location: {run_subprocess(f'which {shlex.quote(head)}')}")
            
            # Enhanced help sources
            tl = run_subprocess(f"tldr {shlex.quote(head)}")
            if "not found" not in tl.lower() and "command not found" not in tl.lower():
                info.append("TLDR Examples:\n" + tl)
            
            # Get brief man page
            man = run_subprocess(f"MANWIDTH=90 man {shlex.quote(head)} | col -b | head -n 50")
            if man and "No manual entry" not in man and "command not found" not in man.lower():
                info.append("Manual (brief):\n" + man)
            
            # Try --help
            help_text = run_subprocess(f"{shlex.quote(head)} --help")
            if help_text and len(help_text) > 10:
                info.append("Help text:\n" + help_text[:1000])

        # Command breakdown for complex commands
        if len(parts) > 1:
            info.append(f"\nCommand breakdown:")
            info.append(f"- Base command: {head}")
            info.append(f"- Arguments: {' '.join(parts[1:])}")

        return "\n\n".join([i for i in info if i and i.strip()])

    async def _arun(self, command: str) -> str:
        return self._run(command)

class GrepTool(BaseTool):
    name: str = "search_files" 
    description: str = "Search text in files. Enhanced with multiple search tools."

    def _run(self, pattern: str) -> str:
        pattern = pattern.strip()
        if not pattern:
            return "Provide a search pattern."

        # Try different search tools in order of preference
        search_tools = []
        
        if shutil_which("rg"):  # ripgrep (fastest)
            search_tools.append(('ripgrep', f'rg -n --color never "{pattern}"'))
        
        if shutil_which("ag"):  # the silver searcher
            search_tools.append(('ag', f'ag --nocolor "{pattern}"'))
        
        if PLATFORM_INFO["is_windows"]:
            search_tools.append(('findstr', f'findstr /s /n /i "{pattern}" *.*'))
        else:
            search_tools.append(('grep', f'grep -RIn --color=never "{pattern}" .'))

        for tool_name, cmd in search_tools:
            result = run_subprocess(cmd, timeout=30)
            if result and "command not found" not in result.lower():
                return f"Search results using {tool_name}:\n{result[:2000]}{'...[truncated]' if len(result) > 2000 else ''}"
        
        return "No search tool available or no results found."

    async def _arun(self, pattern: str) -> str:
        return self._run(pattern)

class ReadFileTool(BaseTool):
    name: str = "read_file"
    description: str = "Read files with smart encoding detection and size limits."

    def _run(self, path: str) -> str:
        path = path.strip()
        if not path:
            return "Provide a file path."

        p = Path(path).expanduser()
        if not p.exists():
            return f"File not found: {path}"
        
        if not p.is_file():
            return f"Path is not a file: {path}"
        
        # Check file size
        size = p.stat().st_size
        if size > 10 * 1024 * 1024:  # 10MB limit
            return f"File too large: {size:,} bytes. Use head/tail commands instead."

        try:
            # Try different encodings
            for encoding in ['utf-8', 'latin1', 'cp1252']:
                try:
                    data = p.read_text(encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                return "Could not decode file with common encodings."
            
            # Truncate if too long
            if len(data) > 8000:
                return data[:8000] + f"\n...[truncated, {len(data)} total chars]"
            
            return data
            
        except Exception as e:
            return f"Error reading file: {e}"

    async def _arun(self, path: str) -> str:
        return self._run(path)

class WriteFileTool(BaseTool):
    name: str = "write_file"
    description: str = "Write content to files with backup and safety checks."

    def _run(self, payload: str) -> str:
        try:
            obj = json.loads(payload)
            path = Path(obj["path"]).expanduser()
            content = obj.get("content", "")
            backup = obj.get("backup", True)
        except Exception:
            return "Payload must be JSON with 'path' and 'content'. Optional: 'backup': true/false"

        # Safety check for important system files
        dangerous_paths = ['/etc/', '/bin/', '/usr/bin/', '/sys/', '/proc/']
        if any(str(path).startswith(dp) for dp in dangerous_paths):
            return f"Blocked: Writing to system directory {path}"

        # Create backup if file exists
        if backup and path.exists() and path.is_file():
            backup_path = path.with_suffix(path.suffix + '.backup')
            try:
                backup_path.write_bytes(path.read_bytes())
                console.print(f"[dim]Created backup: {backup_path}[/dim]")
            except Exception as e:
                console.print(f"[yellow]Could not create backup: {e}[/yellow]")

        path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            path.write_text(content, encoding='utf-8')
            return f"Wrote {len(content):,} characters to {path}"
        except Exception as e:
            return f"Error writing file: {e}"

    async def _arun(self, payload: str) -> str:
        return self._run(payload)

class GitTool(BaseTool):
    name: str = "git_ops"
    description: str = "Enhanced git operations with safety checks and intelligent suggestions."
    
    SAFE_SUBCMDS: ClassVar[List[str]] = [
        "status", "branch", "checkout", "log", "diff", "add", "commit", 
        "push", "pull", "fetch", "stash", "remote", "show", "config",
        "tag", "merge", "rebase"
    ]

    def _run(self, inp: str) -> str:
        inp = inp.strip()
        if not inp:
            return "Provide a git subcommand. Available: " + ", ".join(self.SAFE_SUBCMDS)

        if not shutil_which("git"):
            return "Git is not installed or not in PATH."

        parts = inp.split()
        subcmd = parts[0]
        
        if subcmd not in self.SAFE_SUBCMDS:
            return f"Subcommand '{subcmd}' not in allowed list: {', '.join(self.SAFE_SUBCMDS)}"

        # Enhanced safety for destructive operations
        destructive_ops = ["reset", "rebase", "merge"]
        if subcmd in destructive_ops:
            if not Confirm.ask(f"'{subcmd}' can be destructive. Continue?", default=False):
                return "Operation canceled."

        # Smart defaults and suggestions
        if subcmd == "commit" and len(parts) == 1:
            return "Commit requires a message. Use: git commit -m \"Your message\""
        
        if subcmd == "push" and len(parts) == 1:
            # Check if upstream is set
            branch_info = run_subprocess("git branch --show-current", timeout=5)
            if branch_info:
                console.print(f"[dim]Pushing current branch: {branch_info}[/dim]")

        result = run_subprocess(f"git {inp}", timeout=60)
        
        # Post-operation suggestions
        if subcmd == "status" and "nothing to commit" not in result:
            console.print("[dim]Hint: Use 'git add .' to stage all changes[/dim]")
        
        return result

    async def _arun(self, inp: str) -> str:
        return self._run(inp)

class DockerTool(BaseTool):
    name: str = "docker_ops"
    description: str = "Enhanced Docker operations with container management and safety."

    def _run(self, inp: str) -> str:
        inp = inp.strip()
        if not inp:
            return "Provide a docker command. Examples: ps, images, logs <container>, exec -it <container> bash"

        if not shutil_which("docker"):
            return "Docker not installed or not accessible."

        parts = inp.split()
        subcmd = parts[0] if parts else ""
        
        # Check Docker daemon
        status_check = run_subprocess("docker info", timeout=10)
        if "Cannot connect to the Docker daemon" in status_check:
            return "Docker daemon is not running. Start it first."

        # Safety checks for destructive operations
        destructive_cmds = ["rm", "rmi", "system prune", "container prune", "image prune", "volume prune"]
        is_destructive = any(cmd in inp for cmd in destructive_cmds)
        
        if is_destructive:
            console.print(f"[yellow]Destructive Docker operation: {inp}[/yellow]")
            if not Confirm.ask("This may delete containers/images/volumes. Continue?", default=False):
                return "Operation canceled."

        # Enhanced commands with better output
        if subcmd == "ps":
            # Show more detailed container info
            result = run_subprocess("docker ps --format 'table {{.Names}}\\t{{.Image}}\\t{{.Status}}\\t{{.Ports}}'", timeout=30)
        else:
            result = run_subprocess(f"docker {inp}", timeout=120)

        # Post-operation suggestions
        if subcmd == "build" and "Successfully built" in result:
            console.print("[dim]Hint: Use 'docker images' to see your new image[/dim]")
        
        return result

    async def _arun(self, inp: str) -> str:
        return self._run(inp)

# Enhanced REPL
ENHANCED_BANNER = Panel.fit(
    f"[bold cyan]Enhanced AI Terminal[/bold cyan] — Intelligent shell automation\n"
    f"[dim]Platform: {PLATFORM_INFO['system'].title()} | Package Manager: {PLATFORM_INFO['package_manager']} | Learning Mode: ON[/dim]",
    border_style="cyan",
)

ENHANCED_HELP = f"""
[bold]Enhanced AI Terminal Help[/bold]

[cyan]Meta Commands:[/cyan]
:help              Show this help
:safe on|off       Toggle safe mode
:autoinstall on|off Toggle automatic package installation
:model NAME        Switch Gemini model
:history           Show conversation memory
:toolhelp <tool>   Show learned information about a tool
:toollist          List all learned tools
:platform          Show platform information
:clear             Clear screen
:quit              Exit

[cyan]Direct Commands:[/cyan]
!<cmd>             Execute shell command directly
?<cmd>             Explain a command without running it

[cyan]AI Capabilities:[/cyan]
- "install package X"          → Installs system/Python packages
- "learn about tool Y"         → Analyzes tool documentation
- "suggest tools for Z task"   → Recommends appropriate tools
- "how do I do X"             → Provides commands and explanations

[cyan]Smart Features:[/cyan]
- Automatic tool discovery and learning
- Intelligent command suggestions
- Context-aware help and examples
- Memory of successful commands
- Package management integration

Platform: {PLATFORM_INFO['system'].title()} | Shell: {PLATFORM_INFO['shell_executable']}
Package Manager: {PLATFORM_INFO['package_manager']}
"""

def create_completer(knowledge_db: Dict) -> Optional[WordCompleter]:
    """Create an intelligent command completer."""
    if not PromptSession:
        return None
    
    # Build completion words
    words = [
        # Meta commands
        ":help", ":safe", ":autoinstall", ":model", ":history", 
        ":toolhelp", ":toollist", ":platform", ":clear", ":quit",
        # Common tasks
        "install", "learn about", "suggest tools for", "explain",
        "search for", "help with",
    ]
    
    # Add known tools
    tools = list(knowledge_db.get("tools", {}).keys())
    words.extend(tools)
    
    # Add common commands
    common_cmds = ["ls", "cd", "pwd", "cat", "grep", "find", "git", "docker", "vim", "nano"]
    words.extend(common_cmds)
    
    return WordCompleter(words, ignore_case=True)

def main():
    """Enhanced main function with full functionality."""
    # Initialize
    state = load_state()
    if not GEMINI_API_KEY:
        console.print("[red]GEMINI_API_KEY is not set. Please set your API key.[/red]")
        sys.exit(1)

    try:
        llm = EnhancedLLM(model=state.get("model", DEFAULT_MODEL))
        vstore = EnhancedVectorStore()
        agent = EnhancedAgentHarness(llm, state, vstore)
    except Exception as e:
        console.print(f"[red]Failed to initialize AI components: {e}[/red]")
        console.print("[yellow]Check your API key and internet connection.[/yellow]")
        sys.exit(1)

    console.print(ENHANCED_BANNER)
    console.print(Panel(ENHANCED_HELP.strip(), border_style="gray50", box=box.ROUNDED))

    # Setup input with intelligent completion
    completer = create_completer(agent.knowledge_db)
    
    if PromptSession:
        session = PromptSession(
            history=FileHistory(HISTORY_FILE),
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer
        )
        get_input = lambda: session.prompt("[bold cyan]🤖 [/bold cyan]")
    else:
        get_input = lambda: input("🤖 ")

    # Main loop
    try:
        while True:
            try:
                text = get_input().strip()
            except (EOFError, KeyboardInterrupt):
                console.print("\n[dim]Goodbye![/dim]")
                break

            if not text:
                continue

            # Meta commands
            if text == ":help":
                console.print(Panel(ENHANCED_HELP.strip(), border_style="gray50", box=box.ROUNDED))
                continue

            elif text.startswith(":safe"):
                _, *rest = text.split()
                if rest and rest[0].lower() == "off":
                    state["safe_mode"] = False
                else:
                    state["safe_mode"] = True
                save_state(state)
                console.print(f"[green]Safe mode: {'ON' if state['safe_mode'] else 'OFF'}[/green]")
                continue

            elif text.startswith(":autoinstall"):
                _, *rest = text.split()
                if rest and rest[0].lower() == "on":
                    state["auto_install"] = True
                else:
                    state["auto_install"] = False
                save_state(state)
                console.print(f"[green]Auto-install: {'ON' if state['auto_install'] else 'OFF'}[/green]")
                continue

            elif text.startswith(":model"):
                _, *rest = text.split(maxsplit=1)
                if rest:
                    state["model"] = rest[0].strip()
                    save_state(state)
                    console.print(f"[green]Model set to {state['model']}. Restart recommended.[/green]")
                else:
                    console.print(f"Current model: {state['model']}")
                continue

            elif text.startswith(":toolhelp"):
                _, *rest = text.split(maxsplit=1)
                if rest:
                    tool_name = rest[0].strip()
                    tools_info = agent.knowledge_db.get("tools", {})
                    if tool_name in tools_info:
                        info = tools_info[tool_name]
                        console.print(Panel(
                            info["intelligent_help"], 
                            title=f"Help for {tool_name}",
                            border_style="green"
                        ))
                    else:
                        console.print(f"[yellow]No information about '{tool_name}'. Try 'learn_tool {tool_name}' first.[/yellow]")
                else:
                    console.print("Usage: :toolhelp <tool_name>")
                continue

            elif text == ":toollist":
                tools_info = agent.knowledge_db.get("tools", {})
                if tools_info:
                    table = Table(title="Learned Tools", box=box.MINIMAL_DOUBLE_HEAD)
                    table.add_column("Tool", style="cyan")
                    table.add_column("Usage Count", justify="right", style="green")
                    table.add_column("Learned", style="yellow")
                    
                    for tool_name, info in tools_info.items():
                        learned_at = info.get("learned_at", 0)
                        learned_str = time.strftime("%Y-%m-%d", time.localtime(learned_at)) if learned_at else "Unknown"
                        table.add_row(
                            tool_name, 
                            str(info.get("usage_count", 0)),
                            learned_str
                        )
                    console.print(table)
                else:
                    console.print("[yellow]No tools learned yet. Try 'learn about <tool>' commands.[/yellow]")
                continue

            elif text == ":history":
                table = Table(title="Recent Memory", box=box.MINIMAL_DOUBLE_HEAD)
                table.add_column("#", justify="right", width=3)
                table.add_column("User", overflow="fold", max_width=40)
                table.add_column("AI", overflow="fold", max_width=40)
                
                for i, item in enumerate(state.get("memory", [])[-15:], 1):
                    table.add_row(
                        str(i), 
                        item.get("user", "")[:80],
                        item.get("ai", "")[:80]
                    )
                console.print(table)
                continue

            elif text == ":platform":
                table = Table(title="Platform Information", box=box.MINIMAL_DOUBLE_HEAD)
                table.add_column("Property", style="cyan")
                table.add_column("Value", style="green")
                
                info_items = [
                    ("Operating System", PLATFORM_INFO['system'].title()),
                    ("Shell", PLATFORM_INFO['shell_executable']),
                    ("Package Manager", PLATFORM_INFO['package_manager']),
                    ("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"),
                    ("Installed Tools", len(state.get("installed_tools", set()))),
                    ("Learned Tools", len(agent.knowledge_db.get("tools", {}))),
                    ("Vector Store", "Enabled" if vstore.enabled else "Disabled"),
                ]
                
                for prop, value in info_items:
                    table.add_row(prop, str(value))
                console.print(table)
                continue

            elif text == ":clear":
                console.clear()
                continue

            elif text in (":quit", ":exit"):
                break

            # Shell shortcuts
            elif text.startswith("!"):
                cmd = text[1:].strip()
                if looks_dangerous(cmd):
                    console.print("[red]Blocked: Command flagged as dangerous.[/red]")
                    continue
                    
                if state.get("safe_mode", True):
                    if not Confirm.ask(f"Run: [cyan]{cmd}[/cyan] ?", default=False):
                        console.print("[yellow]Canceled.[/yellow]")
                        continue
                
                with console.status("[cyan]Executing...[/cyan]"):
                    output = run_subprocess(cmd)
                console.print(Panel(output or "[dim]no output[/dim]", title=f"$ {cmd}", border_style="green"))
                continue

            elif text.startswith("?"):
                cmd = text[1:].strip()
                with console.status("[cyan]Analyzing command...[/cyan]"):
                    explanation = ExplainTool()._run(cmd)
                console.print(Panel(explanation or "[dim]no explanation available[/dim]", 
                                  title=f"Explain: {cmd}", border_style="yellow"))
                continue

            # AI Agent processing
            with console.status("[cyan]AI thinking...[/cyan]"):
                reply = agent.ask(text)
            
            console.print(Panel(reply or "[dim]no response[/dim]", border_style="magenta"))

            # Update memory
            state.setdefault("memory", []).append({
                "user": text, 
                "ai": reply, 
                "ts": time.time()
            })
            
            # Trim memory
            if len(state["memory"]) > 200:
                state["memory"] = state["memory"][-200:]
            
            save_state(state)

            # Add to vector store
            if vstore.enabled:
                vstore.add(f"User: {text}\nAI: {reply}", {"type": "conversation"})

    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted. Goodbye![/dim]")
    except Exception as e:
        console.print(f"\n[red]Unexpected error: {e}[/red]")
    finally:
        # Save final state
        save_state(state)
        save_tools_knowledge(agent.knowledge_db)
        console.print("[dim]Session saved.[/dim]")

if __name__ == "__main__":
    main()
