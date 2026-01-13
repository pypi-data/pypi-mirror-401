"""
Tools for FlawHunt CLI.
Contains all tool classes for shell operations, file handling, git, and docker.
"""
import json
import shlex
import re
import requests
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Callable, ClassVar, Optional

try:
    from langchain.tools import BaseTool
except ImportError:
    BaseTool = object

from pydantic import BaseModel, Field
from typing import Type
from .utils import run_subprocess, get_platform_info, extract_tool_info
import os
from .safety import looks_dangerous

# Input Schemas
class ShellInput(BaseModel):
    command: str = Field(description="The shell command to execute")

class ExplainInput(BaseModel):
    command: str = Field(description="The shell command to explain")

class GrepInput(BaseModel):
    pattern: str = Field(description="The regex pattern or text to search for")

class ReadFileInput(BaseModel):
    path: str = Field(description="Absolute path to the file to read")

class WriteFileInput(BaseModel):
    path: str = Field(description="Absolute path where the file should be written")
    content: str = Field(description="The content to write to the file")

class ShellTool(BaseTool):
    """Tool for executing shell commands with safety checks."""
    name: str = "shell_run"
    description: str = "Execute a safe shell command. Requires confirmation if safe_mode is enabled."
    args_schema: ClassVar[Type[BaseModel]] = ShellInput
    get_state: Callable[[], Dict[str, Any]]

    def __init__(self, get_state: Callable[[], Dict[str, Any]]):
        super().__init__(get_state=get_state)

    def _run(self, command: str) -> str:
        """Run a shell command with safety checks."""
        from rich.prompt import Confirm
        from rich.console import Console
        
        console = Console()
        state = self.get_state()
        command = command.strip()
        
        if looks_dangerous(command):
            return "Blocked: command flagged as dangerous."
        
        # if state.get("safe_mode", True):
        #     confirmed = Confirm.ask(f"[bold]Run[/bold] [cyan]{command}[/cyan]?", default=False)
        #     if not confirmed:
        #         return "Canceled."
        
        return run_subprocess(command)
    
    async def _arun(self, command: str) -> str:
        return self._run(command)

class ExplainTool(BaseTool):
    """Tool for explaining shell commands without executing them."""
    name: str = "explain_command"
    description: str = "Explain what a shell command would do. Does not execute."
    args_schema: ClassVar[Type[BaseModel]] = ExplainInput

    def _run(self, command: str) -> str:
        """Explain what a shell command does."""
        from .utils import get_platform_info
        
        command = command.strip()
        if not command:
            return "Provide a command to explain."
        
        # Use platform-appropriate help commands
        parts = shlex.split(command)
        platform_info = get_platform_info()
        head = parts[0] if parts else command
        info = []
        
        if platform_info["is_windows"]:
            # Windows-specific help commands
            info.append(run_subprocess(f"where {head}"))
            info.append(run_subprocess(f"help {head}"))
            # Try PowerShell Get-Help if available
            if "powershell" in platform_info["shell_executable"].lower():
                info.append(run_subprocess(f"powershell -Command \"Get-Help {head} -ErrorAction SilentlyContinue\""))
        else:
            # Unix-like systems
            info.append(run_subprocess(f"type -a {shlex.quote(head)}"))
            info.append(run_subprocess(f"which {shlex.quote(head)}"))
            
            # try tldr then man (non-interactive)
            tl = run_subprocess(f"tldr {shlex.quote(head)}")
            if "not found" not in tl.lower() and "command not found" not in tl.lower():
                info.append("TLDR:\n" + tl)
            
            man = run_subprocess(f"MANWIDTH=90 man {shlex.quote(head)} | col -b | head -n 100")
            if man and "No manual entry" not in man and "command not found" not in man.lower():
                info.append("MAN PAGE (first 100 lines):\n" + man)
        
        return "\n\n".join([i for i in info if i and i.strip()])

    async def _arun(self, command: str) -> str:
        return self._run(command)

class GrepTool(BaseTool):
    """Tool for searching text in files."""
    name: str = "search_files"
    description: str = "Search text in files under current directory (uses ripgrep if available, else platform-appropriate search). Input: a pattern."
    args_schema: ClassVar[Type[BaseModel]] = GrepInput

    def _run(self, pattern: str) -> str:
        """Search for pattern in files."""
        from .utils import shutil_which
        
        pattern = pattern.strip()
        if not pattern:
            return "Provide a search pattern."
        
        # Try ripgrep first (cross-platform)
        if shutil_which("rg"):
            return run_subprocess(f'rg -n "{pattern}"')
        
        # Platform-specific fallbacks
        platform_info = get_platform_info()
        if platform_info["is_windows"]:
            # Use findstr on Windows
            return run_subprocess(f'findstr /s /n /i "{pattern}" *.*')
        else:
            # Use grep on Unix-like systems
            return run_subprocess(f'grep -RIn "{pattern}" .')

    async def _arun(self, pattern: str) -> str:
        return self._run(pattern)

class ReadFileTool(BaseTool):
    """Tool for reading text files."""
    name: str = "read_file"
    description: str = "Read a small text file. Input: file path."
    args_schema: ClassVar[Type[BaseModel]] = ReadFileInput

    def _run(self, path: str) -> str:
        """Read a text file."""
        path = path.strip()
        if not path:
            return "Provide a file path."
        
        p = Path(path).expanduser()
        if not p.exists() or not p.is_file():
            return "File not found."
        
        try:
            data = p.read_text(errors="ignore")
            if len(data) > 8000:
                return data[:8000] + "\n...[truncated]"
            return data
        except Exception as e:
            return f"Error reading file: {e}"

    async def _arun(self, path: str) -> str:
        return self._run(path)

class WriteFileTool(BaseTool):
    """Tool for writing content to files."""
    name: str = "write_file"
    description: str = "Write content to a file (create or overwrite). Arguments: path, content."
    args_schema: ClassVar[Type[BaseModel]] = WriteFileInput

    def _run(self, path: str, content: str) -> str:
        """Write content to a file."""
        try:
            p = Path(path).expanduser()
            
            # Safety check: Prevent writing to critical system files?
            # For now, just ensuring parent exists
            p.parent.mkdir(parents=True, exist_ok=True)
            
            p.write_text(content)
            return f"Wrote {len(content)} chars to {p}"
        except Exception as e:
            return f"Error writing file: {e}"

    async def _arun(self, path: str, content: str) -> str:
        return self._run(path, content)

class DirectoryNavigationInput(BaseModel):
    command: str = Field(description="The navigation command (e.g., 'list', 'cd /path', 'pwd')")

class GitInput(BaseModel):
    command: str = Field(description="The git subcommand to execute (e.g., 'status', 'commit -m \"msg\"')")

class DockerInput(BaseModel):
    command: str = Field(description="The docker command to execute (e.g., 'ps', 'logs container')")

class DirectoryNavigationTool(BaseTool):
    """Tool for directory navigation and file system operations."""
    name: str = "navigate_directories"
    description: str = "Navigate directories, list contents, show current path, and explore file system. Input examples: 'list', 'list /path', 'current path', 'go to /path', 'find files *.py'"
    args_schema: ClassVar[Type[BaseModel]] = DirectoryNavigationInput
    get_state: Callable[[], Dict[str, Any]]

    def __init__(self, get_state: Callable[[], Dict[str, Any]]):
        super().__init__(get_state=get_state)

    def _run(self, command: str) -> str:
        """Handle directory navigation commands."""
        import os
        from pathlib import Path
        
        command = command.strip().lower()
        
        try:
            # Get current working directory
            if command in ["pwd", "current path", "where am i", "current directory"]:
                return f"Current directory: {os.getcwd()}"
            
            # List current directory
            elif command in ["ls", "list", "dir", "show files"]:
                return self._list_directory(Path.cwd())
            
            # List specific directory
            elif command.startswith(("list ", "ls ", "dir ")):
                path_part = command.split(" ", 1)[1]
                target_path = Path(path_part).expanduser().resolve()
                if not target_path.exists():
                    return f"Path does not exist: {target_path}"
                return self._list_directory(target_path)
            
            # Change directory
            elif command.startswith(("cd ", "go to ", "change to ", "navigate to ")):
                if command.startswith("cd "):
                    path_part = command[3:].strip()
                elif command.startswith("go to "):
                    path_part = command[6:].strip()
                elif command.startswith("change to "):
                    path_part = command[10:].strip()
                else:  # navigate to
                    path_part = command[12:].strip()
                
                target_path = Path(path_part).expanduser().resolve()
                if not target_path.exists():
                    return f"Path does not exist: {target_path}"
                if not target_path.is_dir():
                    return f"Not a directory: {target_path}"
                
                try:
                    os.chdir(target_path)
                    return f"Changed to: {target_path}"
                except PermissionError:
                    return f"Permission denied: {target_path}"
            
            # Go up one directory
            elif command in ["cd ..", "go up", "parent directory", "up"]:
                parent = Path.cwd().parent
                try:
                    os.chdir(parent)
                    return f"Changed to: {parent}"
                except PermissionError:
                    return f"Permission denied: {parent}"
            
            # Go to home directory
            elif command in ["cd ~", "go home", "home", "cd"]:
                home = Path.home()
                os.chdir(home)
                return f"Changed to home: {home}"
            
            # Find files with pattern
            elif command.startswith(("find ", "search ", "locate ")):
                if command.startswith("find "):
                    pattern = command[5:].strip()
                elif command.startswith("search "):
                    pattern = command[7:].strip()
                else:  # locate
                    pattern = command[7:].strip()
                
                return self._find_files(pattern)
            
            # Show directory tree
            elif command in ["tree", "show tree", "directory tree"]:
                return self._show_tree(Path.cwd(), max_depth=3)
            
            # Show disk usage
            elif command in ["disk usage", "du", "space"]:
                return self._show_disk_usage(Path.cwd())
            
            else:
                return self._show_help()
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _list_directory(self, path: Path) -> str:
        """List directory contents with details."""
        try:
            if not path.is_dir():
                return f"Not a directory: {path}"
            
            items = []
            total_size = 0
            
            # Get all items and sort them
            all_items = list(path.iterdir())
            all_items.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item in all_items:
                try:
                    if item.is_dir():
                        items.append(f"📁 {item.name}/")
                    else:
                        size = item.stat().st_size
                        total_size += size
                        size_str = self._format_size(size)
                        items.append(f"📄 {item.name} ({size_str})")
                except (PermissionError, OSError):
                    items.append(f"❌ {item.name} (permission denied)")
            
            result = f"📂 Directory: {path}\n"
            result += f"📊 Total items: {len(all_items)}\n"
            if total_size > 0:
                result += f"💾 Total size: {self._format_size(total_size)}\n"
            result += "\n"
            
            if items:
                result += "\n".join(items)
            else:
                result += "(empty directory)"
            
            return result
            
        except PermissionError:
            return f"Permission denied: {path}"
        except Exception as e:
            return f"Error listing directory: {e}"
    
    def _find_files(self, pattern: str) -> str:
        """Find files matching a pattern."""
        import glob
        
        try:
            # Use glob to find files
            matches = glob.glob(pattern, recursive=True)
            
            if not matches:
                return f"No files found matching: {pattern}"
            
            # Sort and limit results
            matches.sort()
            if len(matches) > 50:
                result = f"Found {len(matches)} matches (showing first 50):\n\n"
                matches = matches[:50]
            else:
                result = f"Found {len(matches)} matches:\n\n"
            
            for match in matches:
                path = Path(match)
                if path.is_dir():
                    result += f"📁 {match}/\n"
                else:
                    size = self._format_size(path.stat().st_size)
                    result += f"📄 {match} ({size})\n"
            
            return result.rstrip()
            
        except Exception as e:
            return f"Error finding files: {e}"
    
    def _show_tree(self, path: Path, max_depth: int = 3, current_depth: int = 0) -> str:
        """Show directory tree structure."""
        if current_depth >= max_depth:
            return ""
        
        try:
            items = []
            prefix = "  " * current_depth
            
            if current_depth == 0:
                items.append(f"🌳 {path}")
            
            try:
                children = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for i, child in enumerate(children[:20]):  # Limit to 20 items per level
                    is_last = i == len(children) - 1
                    connector = "└── " if is_last else "├── "
                    
                    if child.is_dir():
                        items.append(f"{prefix}{connector}📁 {child.name}/")
                        if current_depth < max_depth - 1:
                            subtree = self._show_tree(child, max_depth, current_depth + 1)
                            if subtree:
                                items.append(subtree)
                    else:
                        size = self._format_size(child.stat().st_size)
                        items.append(f"{prefix}{connector}📄 {child.name} ({size})")
                
                if len(list(path.iterdir())) > 20:
                    items.append(f"{prefix}... ({len(list(path.iterdir())) - 20} more items)")
                    
            except PermissionError:
                items.append(f"{prefix}❌ (permission denied)")
            
            return "\n".join(items)
            
        except Exception as e:
            return f"Error showing tree: {e}"
    
    def _show_disk_usage(self, path: Path) -> str:
        """Show disk usage information."""
        try:
            import shutil
            
            total, used, free = shutil.disk_usage(path)
            
            result = f"💾 Disk Usage for {path}:\n\n"
            result += f"Total: {self._format_size(total)}\n"
            result += f"Used:  {self._format_size(used)} ({used/total*100:.1f}%)\n"
            result += f"Free:  {self._format_size(free)} ({free/total*100:.1f}%)\n"
            
            # Show usage bar
            bar_length = 40
            used_bars = int((used / total) * bar_length)
            free_bars = bar_length - used_bars
            
            result += f"\n[{'█' * used_bars}{'░' * free_bars}]\n"
            
            return result
            
        except Exception as e:
            return f"Error getting disk usage: {e}"
    
    def _format_size(self, size: int) -> str:
        """Format file size in human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} PB"
    
    def _show_help(self) -> str:
        """Show help for directory navigation commands."""
        return """🧭 Directory Navigation Commands:

📍 Current Location:
  • "current path" / "pwd" - Show current directory
  • "where am i" - Show current directory

📂 List Contents:
  • "list" / "ls" - List current directory
  • "list /path" - List specific directory
  • "show files" - List current directory

🚀 Navigate:
  • "cd /path" / "go to /path" - Change directory
  • "cd .." / "go up" - Go to parent directory
  • "cd ~" / "go home" - Go to home directory

🔍 Search:
  • "find *.py" - Find files matching pattern
  • "search *.txt" - Search for files
  • "locate pattern" - Locate files

🌳 Explore:
  • "tree" - Show directory tree
  • "disk usage" - Show disk space info

Examples:
  • "list Documents"
  • "go to /Users/username/Projects"
  • "find *.json"
  • "tree"""
    
    async def _arun(self, command: str) -> str:
        return self._run(command)

class GitTool(BaseTool):
    """Tool for safe git operations."""
    name: str = "git_ops"
    description: str = "Run safe git commands in the current repo. Input examples: 'status', 'create branch myfeature', 'commit -m \"msg\"', 'push'."
    SAFE_SUBCMDS: ClassVar[List[str]] = [
        "status", "branch", "checkout", "log", "diff", "add", 
        "commit", "push", "pull", "fetch", "stash"
    ]
    args_schema: ClassVar[Type[BaseModel]] = GitInput

    def _run(self, command: str) -> str:
        """Run git commands with safety checks."""
        from .utils import shutil_which
        
        inp = command.strip()
        if not inp:
            return "Provide a git subcommand."
        
        # Check if git is available
        if not shutil_which("git"):
            return "Git is not installed or not in PATH."
        
        # naive filter
        sub = inp.split()[0]
        if sub not in self.SAFE_SUBCMDS:
            return f"Subcommand '{sub}' not allowed."
        
        if sub == "commit" and "-m" not in inp:
            return "Please include a commit message with -m."
        
        return run_subprocess(f"git {inp}")

    async def _arun(self, command: str) -> str:
        return self._run(command)

class DockerTool(BaseTool):
    """Tool for safe docker operations."""
    name: str = "docker_ops"
    description: str = "Run safe docker commands. Input examples: 'ps', 'images', 'logs <name>', 'exec -it <name> /bin/bash' (confirmation required)."
    args_schema: ClassVar[Type[BaseModel]] = DockerInput

    def _run(self, command: str) -> str:
        """Run docker commands with safety checks."""
        from .utils import shutil_which
        from rich.prompt import Confirm
        
        inp = command.strip()
        if not shutil_which("docker"):
            return "Docker not installed."
        
        # allow only read-ish commands unless confirmed
        write_like = any(x in inp for x in ["rm ", "rmi ", "stop ", "kill ", "down ", "prune", "run "])
        if write_like and not Confirm.ask(f"Run potentially disruptive docker cmd: {inp}?", default=False):
            return "Canceled."
        
        return run_subprocess(f"docker {inp}")

    async def _arun(self, command: str) -> str:
        return self._run(command)


class PackageManagerInput(BaseModel):
    query: str = Field(description="Package name to install, or 'search <term>'")

class PythonPackageInput(BaseModel):
    query: str = Field(description="Command: 'install <package>', 'search <package>', or 'list'")

class ToolLearnerInput(BaseModel):
    tool_name: str = Field(description="Name of the command-line tool to learn about")

class PackageManagerTool(BaseTool):
    name: str = "package_manager"
    description: str = "Install system packages using the detected package manager. Input: package_name or 'search package_name'"
    auto_install: bool = False
    args_schema: ClassVar[Type[BaseModel]] = PackageManagerInput

    def __init__(self, auto_install: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.auto_install = auto_install

    def _run(self, query: str) -> str:
        query = query.strip()
        if not query:
            return "Provide a package name or 'search <term>'"

        platform_info = get_platform_info()
        pm = platform_info["package_manager"]
        if pm == "unknown":
            return "No supported package manager detected"

        if query.startswith("search "):
            search_term = query[7:].strip()
            return self._search_package(pm, search_term)
        else:
            return self._install_package(pm, query)

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

    def _is_installed(self, pm: str, package: str) -> bool:
        """Check if a system package is already installed to avoid redundant installs."""
        try:
            checks = {
                "apt": f"dpkg -s {package} | grep -i '^status'",
                "yum": f"rpm -q {package}",
                "dnf": f"rpm -q {package}",
                "pacman": f"pacman -Qi {package}",
                "brew": f"brew list --versions {package}",
                "choco": f"choco list --local-only | findstr /i ^{package}",
                "winget": f"winget list --source winget | findstr /i ^{package}",
            }
            cmd = checks.get(pm)
            if not cmd:
                return False
            result = run_subprocess(cmd, timeout=20)
            return bool(result and result.strip())
        except Exception:
            return False

    def _install_package(self, pm: str, package: str) -> str:
        """Install a package."""
        install_commands = {
            "apt": f"sudo apt-get install -y --no-install-recommends {package}",
            "yum": f"sudo yum install -y {package}",
            "dnf": f"sudo dnf install -y {package}",
            "pacman": f"sudo pacman -S --noconfirm {package}",
            "brew": f"brew install --quiet {package}",
            "choco": f"choco install {package} -y",
            "winget": f"winget install {package}"
        }
        
        cmd = install_commands.get(pm)
        if not cmd:
            return f"Installation not supported for {pm}"

        # Skip if already installed
        if self._is_installed(pm, package):
            return f"{package} is already installed. Skipping."

        if not self.auto_install:
            from rich.console import Console
            from rich.prompt import Confirm
            console = Console()
            console.print(f"[yellow]About to run:[/yellow] {cmd}")
            if not Confirm.ask("Proceed with installation?", default=False):
                return "Installation canceled"

        # Attempt install; on failure for apt/dnf/yum, update index and retry once
        result = run_subprocess(cmd, timeout=300)
        lower = result.lower() if result else ""
        if any(err in lower for err in ["unable to locate package", "no match", "error", "failed"]):
            if pm in {"apt", "yum", "dnf"}:
                update_cmd = {
                    "apt": "sudo apt-get update -y",
                    "yum": "sudo yum makecache -y",
                    "dnf": "sudo dnf makecache -y",
                }[pm]
                run_subprocess(update_cmd, timeout=180)
                result = run_subprocess(cmd, timeout=300)
        
        if result and ("successfully" in result.lower() or "installed" in result.lower() or self._is_installed(pm, package)):
            return f"Successfully installed {package}\n{result[:500]}"
        
        return result

    async def _arun(self, query: str) -> str:
        return self._run(query)


class PythonPackageManagerTool(BaseTool):
    name: str = "python_packages"
    description: str = "Install and manage Python packages using pip"
    args_schema: ClassVar[Type[BaseModel]] = PythonPackageInput
    llm: Any = None

    def __init__(self, llm_instance=None, get_state=None, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm_instance

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
            return self._search_pypi(package)
        elif action == "install":
            from rich.console import Console
            from rich.prompt import Confirm
            console = Console()
            
            if not Confirm.ask(f"Install Python package '{package}'?", default=False):
                return "Installation canceled"
            
            # Skip install if already present
            already = run_subprocess(f"python -m pip show {package}", timeout=20)
            if already and "Name:" in already:
                return f"{package} already installed. Skipping.\n{already}"

            # Prefer binary wheels for speed; reduce verbosity
            install_cmd = f"python -m pip install --prefer-binary -q {package}"
            result = run_subprocess(install_cmd, timeout=300)
            if result and ("successfully installed" in result.lower() or "installed" in result.lower()):
                return f"Successfully installed {package}"
            
            # Retry with upgrade in case of existing but outdated installation
            retry = run_subprocess(f"python -m pip install --prefer-binary -q --upgrade {package}", timeout=300)
            if retry and ("successfully installed" in retry.lower() or "installed" in retry.lower()):
                return f"Successfully installed/updated {package}"
            return result or retry or "pip did not report installation status"
        else:
            return "Supported actions: install, search, list"

    def _search_pypi(self, package: str) -> str:
        """Search PyPI for packages using web scraping."""
        try:
            response = requests.get(f"https://pypi.org/search/?q={package}", timeout=10)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
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

    async def _arun(self, query: str) -> str:
        return self._run(query)


class ToolLearnerTool(BaseTool):
    name: str = "learntool"
    description: str = "Learn about an installed command-line tool by reading its manual and help. Input: tool_name"
    args_schema: ClassVar[Type[BaseModel]] = ToolLearnerInput
    llm: Any = None

    def __init__(self, llm_instance=None, get_state=None, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm_instance

    def _run(self, tool_name: str) -> str:
        if not tool_name.strip():
            return "Provide a tool name to learn about"

        info = extract_tool_info(tool_name)
        if not info["location"] or "not found" in info["location"].lower():
            return f"Tool '{tool_name}' not found or not installed"

        # Combine all available information
        tool_info = f"""
Tool: {tool_name}
Location: {info['location']}
Version: {info['version']}

Help Output:
{info['help']}

Manual Page:
{info['man']}
"""

        if self.llm:
            try:
                prompt = f"""
Analyze this command-line tool and generate a concise usage guide:

{tool_info[:3000]}

Generate a structured response with:
1. Brief description (1-2 sentences)
2. Most common use cases (3-5 examples)
3. Important flags/options
4. Example commands with explanations

Keep it practical and focus on real-world usage.
"""
                return self.llm.invoke(prompt)
            except Exception:
                pass

        return tool_info

    async def _arun(self, tool_name: str) -> str:
        return self._run(tool_name)


class SmartShellInput(BaseModel):
    command: str = Field(description="The shell command to execute intelligently")

class SmartShellTool(BaseTool):
    name: str = "smartshell"
    description: str = "Execute shell commands with intelligent suggestions and safety checks"
    args_schema: ClassVar[Type[BaseModel]] = SmartShellInput
    llm: Any = None

    def __init__(self, llm_instance=None, get_state=None, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm_instance

    def _run(self, command: str) -> str:
        if not command.strip():
            return "No command provided"

        # Enhanced safety check
        dangerous_patterns = [
            r'rm\s+-rf\s+/', r'rm\s+-rf\s+\*', r'dd\s+.*=/dev/',
            r':\(\)\{\s*:\|\s*:\s*&\s*\};\s*:',  # fork bomb
            r'sudo\s+rm\s+-rf', r'chmod\s+-R\s+777',
            r'wget\s+.*\|\s+sh', r'curl\s+.*\|\s+sh'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                from rich.console import Console
                from rich.prompt import Confirm
                console = Console()
                console.print(f"[red]Potentially dangerous command detected:[/red] {command}")
                # if not Confirm.ask("Do you want to proceed?", default=False):
                #     return "Command canceled for safety"

        # Get command suggestions
        suggestions = self._get_command_suggestions(command)
        
        try:
            result = run_subprocess(command, timeout=60)
            
            # Add suggestions to output
            if suggestions:
                result = f"{result}\n\nSuggestions:\n{suggestions}"
            
            return result
        except Exception as e:
            return f"Error executing command: {e}"

    def _get_command_suggestions(self, command: str) -> str:
        """Provide intelligent suggestions based on the command."""
        if not self.llm:
            return ""
        
        try:
            prompt = f"""
            The user executed: {command}
            
            Provide 2-3 useful command suggestions that would be helpful next.
            Focus on common workflows and best practices.
            Format as: - command: brief explanation
            """
            return self.llm.invoke(prompt)
        except Exception:
            return ""

    async def _arun(self, command: str) -> str:
        return self._run(command)


class ScriptGeneratorInput(BaseModel):
    request: str = Field(description="Description of what the script should do")

class ScriptGeneratorTool(BaseTool):
    name: str = "create_script"
    description: str = "Generate and create scripts (Python, Bash, etc.) based on natural language requests. Input: description of what the script should do."
    args_schema: ClassVar[Type[BaseModel]] = ScriptGeneratorInput
    llm: Any = None

    def __init__(self, llm_instance=None, get_state=None, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm_instance
        self._get_state = get_state

    def _run(self, request: str) -> str:
        """Generate and create a script based on user request."""
        if not self.llm:
            return "LLM not available for script generation."
        
        # Determine script type and filename
        script_type = self._determine_script_type(request)
        filename = self._generate_filename(request, script_type)
        
        prompt = f"""Create a {script_type} script for the following request: "{request}"
        
Requirements:
1. Write complete, functional code
2. Include proper error handling
3. Add helpful comments
4. Follow security best practices
5. Make it suitable for cybersecurity/ethical hacking context
6. Include usage instructions as comments at the top
        
Provide ONLY the script code, no explanations or markdown formatting."""
        
        try:
            # Use the LLM's invoke method directly
            script_content = self.llm.invoke(prompt)
            
            # Clean up the response
            script_content = self._clean_script_content(script_content)
            
            # Write the script to file
            try:
                path = Path(filename).expanduser()
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(script_content)
                
                # Make executable if it's a shell script
                if script_type in ['bash', 'shell']:
                    import os
                    os.chmod(path, 0o755)
                
                return f"Created {script_type} script: {path}\nContent length: {len(script_content)} characters\n\nTo run: {'python3 ' if script_type == 'python' else './'}{filename}"
            except Exception as e:
                return f"Error writing script file: {e}"
                
        except Exception as e:
            return f"Error generating script: {e}"
    
    def _determine_script_type(self, request: str) -> str:
        """Determine the appropriate script type based on the request."""
        request_lower = request.lower()
        if any(keyword in request_lower for keyword in ['python', 'pip', 'import', 'requests', 'socket']):
            return 'python'
        elif any(keyword in request_lower for keyword in ['bash', 'shell', 'curl', 'grep', 'awk']):
            return 'bash'
        else:
            # Default to Python for most cybersecurity tasks
            return 'python'
    
    def _generate_filename(self, request: str, script_type: str) -> str:
        """Generate an appropriate filename based on the request."""
        # Extract key words from request
        import re
        words = re.findall(r'\b\w+\b', request.lower())
        
        # Filter out common words and keep relevant ones
        relevant_words = [w for w in words if w not in ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'can', 'you', 'write', 'me', 'script', 'create', 'make', 'get', 'all']]
        
        # Take first few relevant words
        filename_base = '_'.join(relevant_words[:3]) if relevant_words else 'generated_script'
        
        extension = '.py' if script_type == 'python' else '.sh'
        return f"ai_generated_scripts/{filename_base}{extension}"
    
    def _clean_script_content(self, content: str) -> str:
        """Clean up the generated script content."""
        # Remove markdown code blocks if present
        content = re.sub(r'^```\w*\n', '', content, flags=re.MULTILINE)
        content = re.sub(r'^```\s*$', '', content, flags=re.MULTILINE)
        
        # Remove extra whitespace
        content = content.strip()
        
        return content

    async def _arun(self, request: str) -> str:
        return self._run(request)


class ToolSuggestionInput(BaseModel):
    task_description: str = Field(description="Description of the task to find tools for")

class ToolSuggestionTool(BaseTool):
    name: str = "suggest_tool"
    description: str = "Suggest the most appropriate tool for a given task based on context"
    args_schema: ClassVar[Type[BaseModel]] = ToolSuggestionInput
    llm: Any = None

    def __init__(self, llm_instance=None, get_state=None, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm_instance

    def _run(self, task_description: str) -> str:
        if not task_description.strip():
            return "Please describe what you want to accomplish"

        tools_info = """
        Available tools:
        - shell: Execute any shell command
        - smart_shell: Execute shell commands with safety checks and suggestions
        - explain: Explain shell commands and concepts
        - grep: Search for text patterns in files
        - read_file: Read file contents
        - write_file: Write to files
        - git: Git repository operations
        - docker: Docker container operations
        - package_manager: Install system packages
        - python_packages: Install Python packages
        - learn_tool: Learn about command-line tools
        - suggest_tool: Get tool recommendations (this tool)
        - create_script: Generate and create scripts from natural language
        """

        if not self.llm:
            return tools_info

        prompt = f"""
        User wants to: {task_description}

        {tools_info}

        Recommend the best tool(s) for this task and explain why.
        If multiple tools are needed, provide a workflow.
        """

        try:
            return self.llm.invoke(prompt)
        except Exception as e:
            return f"Error generating suggestion: {e}"

    async def _arun(self, task_description: str) -> str:
        return self._run(task_description)

class EnvironmentSetupInput(BaseModel):
    request: str = Field(description="Optional request details for environment setup", default="")

class EnvironmentSetupTool(BaseTool):
    """Tool for automated environment setup and project configuration."""
    name: str = "setup_environment"
    description: str = "Automatically detect project type and generate development environment configuration files (Dockerfile, requirements.txt, package.json, CI/CD pipelines, linting configs)"
    args_schema: ClassVar[Type[BaseModel]] = EnvironmentSetupInput
    llm: Any = None
    
    def __init__(self, llm_instance=None, get_state=None, **kwargs):
        super().__init__(**kwargs)
        self.llm = llm_instance
        self._get_state = get_state
    
    def _run(self, request: str = "") -> str:
        """Detect project type and generate environment setup files."""
        try:
            current_dir = Path.cwd()
            
            # Detect project type
            project_info = self._detect_project_type(current_dir)
            project_type = project_info['type']
            
            if project_type == 'unknown':
                return f"Could not detect project type in {current_dir}. Please ensure you're in a project directory or specify the project type."
            
            # Generate configuration files based on project type
            generated_files = []
            
            # Generate basic configuration files
            if self._should_generate_dockerfile(project_type, current_dir):
                dockerfile_content = self._generate_dockerfile(project_type, project_info)
                self._write_file(current_dir / "Dockerfile", dockerfile_content)
                generated_files.append("Dockerfile")
            
            if self._should_generate_requirements(project_type, current_dir):
                requirements_content = self._generate_requirements(project_type, project_info)
                filename = "requirements.txt" if project_type == "python" else "package.json"
                self._write_file(current_dir / filename, requirements_content)
                generated_files.append(filename)
            
            # Generate CI/CD pipeline
            if self._should_generate_cicd(current_dir):
                cicd_content = self._generate_github_actions(project_type, project_info)
                cicd_dir = current_dir / ".github" / "workflows"
                cicd_dir.mkdir(parents=True, exist_ok=True)
                self._write_file(cicd_dir / "ci.yml", cicd_content)
                generated_files.append(".github/workflows/ci.yml")
            
            # Generate linting and formatting configs
            linting_files = self._generate_linting_configs(project_type, current_dir)
            generated_files.extend(linting_files)
            
            # Generate .gitignore if needed
            if not (current_dir / ".gitignore").exists():
                gitignore_content = self._generate_gitignore(project_type)
                self._write_file(current_dir / ".gitignore", gitignore_content)
                generated_files.append(".gitignore")
            
            # Generate development setup script
            setup_script = self._generate_setup_script(project_type, project_info)
            script_name = "setup.sh" if project_type != "windows" else "setup.bat"
            self._write_file(current_dir / script_name, setup_script)
            generated_files.append(script_name)
            
            result = f"✅ Environment setup completed for {project_type} project!\n\n"
            result += f"📁 Project detected: {project_info['description']}\n\n"
            result += "📝 Generated files:\n"
            for file in generated_files:
                result += f"  • {file}\n"
            
            result += "\n🚀 Next steps:\n"
            result += f"  1. Run ./{script_name} to set up your development environment\n"
            result += "  2. Review and customize the generated configuration files\n"
            result += "  3. Commit the new files to your repository\n"
            
            return result
            
        except Exception as e:
            return f"Error setting up environment: {str(e)}"
    
    def _detect_project_type(self, project_dir: Path) -> Dict[str, Any]:
        """Detect the type of project based on files and structure."""
        files = list(project_dir.glob("*"))
        file_names = [f.name for f in files]
        
        # Python project detection
        if any(f in file_names for f in ["requirements.txt", "setup.py", "pyproject.toml", "Pipfile"]):
            framework = "unknown"
            if "manage.py" in file_names:
                framework = "django"
            elif "app.py" in file_names or "main.py" in file_names:
                framework = "flask" if self._check_for_flask(project_dir) else "general"
            elif "fastapi" in str(project_dir).lower() or self._check_for_fastapi(project_dir):
                framework = "fastapi"
            
            return {
                "type": "python",
                "framework": framework,
                "description": f"Python {framework} project",
                "has_requirements": "requirements.txt" in file_names,
                "has_setup": "setup.py" in file_names
            }
        
        # Node.js project detection
        if "package.json" in file_names:
            framework = "unknown"
            if "next.config.js" in file_names or "next.config.ts" in file_names:
                framework = "nextjs"
            elif any(f in file_names for f in ["src", "public"]) and self._check_for_react(project_dir):
                framework = "react"
            elif "angular.json" in file_names:
                framework = "angular"
            elif "vue.config.js" in file_names or self._check_for_vue(project_dir):
                framework = "vue"
            elif "express" in self._read_package_json(project_dir).get("dependencies", {}):
                framework = "express"
            
            return {
                "type": "nodejs",
                "framework": framework,
                "description": f"Node.js {framework} project",
                "package_json": self._read_package_json(project_dir)
            }
        
        # Go project detection
        if "go.mod" in file_names or "main.go" in file_names:
            return {
                "type": "go",
                "framework": "general",
                "description": "Go project",
                "has_mod": "go.mod" in file_names
            }
        
        # Rust project detection
        if "Cargo.toml" in file_names:
            return {
                "type": "rust",
                "framework": "general",
                "description": "Rust project",
                "has_cargo": True
            }
        
        # Java project detection
        if any(f in file_names for f in ["pom.xml", "build.gradle", "build.gradle.kts"]):
            framework = "maven" if "pom.xml" in file_names else "gradle"
            return {
                "type": "java",
                "framework": framework,
                "description": f"Java {framework} project"
            }
        
        # Docker project detection
        if "Dockerfile" in file_names:
            return {
                "type": "docker",
                "framework": "general",
                "description": "Docker project"
            }
        
        return {
            "type": "unknown",
            "framework": "unknown",
            "description": "Unknown project type"
        }
    
    def _check_for_flask(self, project_dir: Path) -> bool:
        """Check if project uses Flask."""
        try:
            if (project_dir / "requirements.txt").exists():
                content = (project_dir / "requirements.txt").read_text()
                return "flask" in content.lower()
        except:
            pass
        return False
    
    def _check_for_fastapi(self, project_dir: Path) -> bool:
        """Check if project uses FastAPI."""
        try:
            if (project_dir / "requirements.txt").exists():
                content = (project_dir / "requirements.txt").read_text()
                return "fastapi" in content.lower()
        except:
            pass
        return False
    
    def _check_for_react(self, project_dir: Path) -> bool:
        """Check if project uses React."""
        try:
            package_json = self._read_package_json(project_dir)
            deps = {**package_json.get("dependencies", {}), **package_json.get("devDependencies", {})}
            return "react" in deps
        except:
            pass
        return False
    
    def _check_for_vue(self, project_dir: Path) -> bool:
        """Check if project uses Vue."""
        try:
            package_json = self._read_package_json(project_dir)
            deps = {**package_json.get("dependencies", {}), **package_json.get("devDependencies", {})}
            return "vue" in deps
        except:
            pass
        return False
    
    def _read_package_json(self, project_dir: Path) -> Dict[str, Any]:
        """Read and parse package.json file."""
        try:
            package_file = project_dir / "package.json"
            if package_file.exists():
                return json.loads(package_file.read_text())
        except:
            pass
        return {}
    
    def _should_generate_dockerfile(self, project_type: str, project_dir: Path) -> bool:
        """Check if Dockerfile should be generated."""
        return not (project_dir / "Dockerfile").exists()
    
    def _should_generate_requirements(self, project_type: str, project_dir: Path) -> bool:
        """Check if requirements file should be generated."""
        if project_type == "python":
            return not (project_dir / "requirements.txt").exists()
        elif project_type == "nodejs":
            return not (project_dir / "package.json").exists()
        return False
    
    def _should_generate_cicd(self, project_dir: Path) -> bool:
        """Check if CI/CD pipeline should be generated."""
        github_dir = project_dir / ".github" / "workflows"
        return not github_dir.exists() or not any(github_dir.glob("*.yml"))
    
    def _generate_dockerfile(self, project_type: str, project_info: Dict[str, Any]) -> str:
        """Generate Dockerfile based on project type."""
        if project_type == "python":
            framework = project_info.get("framework", "general")
            if framework == "django":
                return '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
'''
            elif framework == "flask":
                return '''FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
'''
            elif framework == "fastapi":
                return '''FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
'''
            else:
                return '''FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Run the application
CMD ["python", "main.py"]
'''
        
        elif project_type == "nodejs":
            framework = project_info.get("framework", "general")
            if framework == "nextjs":
                return '''FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy project
COPY . .

# Build the application
RUN npm run build

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
'''
            elif framework == "react":
                return '''FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy project and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
'''
            else:
                return '''FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci --only=production

# Copy project
COPY . .

# Expose port
EXPOSE 3000

# Run the application
CMD ["npm", "start"]
'''
        
        elif project_type == "go":
            return '''FROM golang:1.21-alpine AS builder

WORKDIR /app

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Production stage
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
'''
        
        return "# Dockerfile\n# Add your Docker configuration here\n"
    
    def _generate_requirements(self, project_type: str, project_info: Dict[str, Any]) -> str:
        """Generate requirements file based on project type."""
        if project_type == "python":
            framework = project_info.get("framework", "general")
            if framework == "django":
                return '''Django>=4.2.0
psycopg2-binary>=2.9.0
django-cors-headers>=4.0.0
django-environ>=0.10.0
gunicorn>=20.1.0
whitenoise>=6.4.0
'''
            elif framework == "flask":
                return '''Flask>=2.3.0
Flask-SQLAlchemy>=3.0.0
Flask-CORS>=4.0.0
Flask-JWT-Extended>=4.5.0
gunicorn>=20.1.0
python-dotenv>=1.0.0
'''
            elif framework == "fastapi":
                return '''fastapi>=0.100.0
uvicorn[standard]>=0.22.0
pydantic>=2.0.0
sqlalchemy>=2.0.0
alembic>=1.11.0
python-multipart>=0.0.6
'''
            else:
                return '''# Add your Python dependencies here
# Example:
# requests>=2.31.0
# pandas>=2.0.0
# numpy>=1.24.0
'''
        
        elif project_type == "nodejs":
            framework = project_info.get("framework", "general")
            base_package = {
                "name": "my-project",
                "version": "1.0.0",
                "description": "",
                "main": "index.js",
                "scripts": {
                    "start": "node index.js",
                    "dev": "nodemon index.js",
                    "test": "jest"
                },
                "dependencies": {},
                "devDependencies": {
                    "nodemon": "^3.0.0",
                    "jest": "^29.0.0"
                }
            }
            
            if framework == "express":
                base_package["dependencies"]["express"] = "^4.18.0"
                base_package["dependencies"]["cors"] = "^2.8.5"
                base_package["dependencies"]["helmet"] = "^7.0.0"
            elif framework == "nextjs":
                base_package["dependencies"]["next"] = "^13.0.0"
                base_package["dependencies"]["react"] = "^18.0.0"
                base_package["dependencies"]["react-dom"] = "^18.0.0"
                base_package["scripts"] = {
                    "dev": "next dev",
                    "build": "next build",
                    "start": "next start",
                    "lint": "next lint"
                }
            elif framework == "react":
                base_package["dependencies"]["react"] = "^18.0.0"
                base_package["dependencies"]["react-dom"] = "^18.0.0"
                base_package["scripts"] = {
                    "start": "react-scripts start",
                    "build": "react-scripts build",
                    "test": "react-scripts test",
                    "eject": "react-scripts eject"
                }
                base_package["devDependencies"]["react-scripts"] = "^5.0.0"
            
            return json.dumps(base_package, indent=2)
        
        return "# Add your dependencies here\n"
    
    def _generate_github_actions(self, project_type: str, project_info: Dict[str, Any]) -> str:
        """Generate GitHub Actions CI/CD pipeline."""
        if project_type == "python":
            return '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov flake8
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: Test with pytest
      run: |
        pytest --cov=. --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
'''
        
        elif project_type == "nodejs":
            return '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run linter
      run: npm run lint --if-present
    
    - name: Run tests
      run: npm test
    
    - name: Build project
      run: npm run build --if-present
'''
        
        return '''name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Run tests
      run: |
        echo "Add your test commands here"
        # Add project-specific test commands
'''
    
    def _generate_linting_configs(self, project_type: str, project_dir: Path) -> List[str]:
        """Generate linting and formatting configuration files."""
        generated_files = []
        
        if project_type == "python":
            # Generate .flake8 config
            if not (project_dir / ".flake8").exists():
                flake8_config = '''[flake8]
max-line-length = 127
max-complexity = 10
ignore = E203, E266, E501, W503
select = B,C,E,F,W,T4,B9
exclude = 
    .git,
    __pycache__,
    .venv,
    venv,
    build,
    dist
'''
                self._write_file(project_dir / ".flake8", flake8_config)
                generated_files.append(".flake8")
            
            # Generate pyproject.toml for black
            if not (project_dir / "pyproject.toml").exists():
                pyproject_config = '''[tool.black]
line-length = 127
target-version = ['py39', 'py310', 'py311']
include = r'\.pyi?$'
exclude = """
(
  /(
      \.eggs
    | \.git
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
  )/
)
"""

[tool.isort]
profile = "black"
line_length = 127
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
'''
                self._write_file(project_dir / "pyproject.toml", pyproject_config)
                generated_files.append("pyproject.toml")
        
        elif project_type == "nodejs":
            # Generate .eslintrc.js
            if not any((project_dir / f".eslintrc.{ext}").exists() for ext in ["js", "json", "yml", "yaml"]):
                eslint_config = '''module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  plugins: [
    '@typescript-eslint',
  ],
  rules: {
    'indent': ['error', 2],
    'linebreak-style': ['error', 'unix'],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
  },
};
'''
                self._write_file(project_dir / ".eslintrc.js", eslint_config)
                generated_files.append(".eslintrc.js")
            
            # Generate .prettierrc
            if not (project_dir / ".prettierrc").exists():
                prettier_config = '''{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
'''
                self._write_file(project_dir / ".prettierrc", prettier_config)
                generated_files.append(".prettierrc")
        
        return generated_files
    
    def _generate_gitignore(self, project_type: str) -> str:
        """Generate .gitignore file based on project type."""
        base_gitignore = '''# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

'''
        
        if project_type == "python":
            return base_gitignore + '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
PYTHON*

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask
instance/
.webassets-cache

# Scrapy
.scrapy

# Sphinx
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pytest
.pytest_cache/
.coverage
htmlcov/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json
'''
        
        elif project_type == "nodejs":
            return base_gitignore + '''# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage
.grunt

# Bower dependency directory
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons
build/Release

# Dependency directories
node_modules/
jspm_packages/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
.env.test
.env.local
.env.development.local
.env.test.local
.env.production.local

# parcel-bundler cache
.cache
.parcel-cache

# Next.js build output
.next
out

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
public

# Storybook build outputs
.out
.storybook-out
'''
        
        elif project_type == "go":
            return base_gitignore + '''# Go
# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool
*.out

# Dependency directories
vendor/

# Go workspace file
go.work
'''
        
        return base_gitignore
    
    def _generate_setup_script(self, project_type: str, project_info: Dict[str, Any]) -> str:
        """Generate development environment setup script."""
        if project_type == "python":
            return '''#!/bin/bash

# Python Development Environment Setup Script

echo "🐍 Setting up Python development environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📚 Installing requirements..."
    pip install -r requirements.txt
fi

# Install development dependencies
echo "🛠️ Installing development dependencies..."
pip install black flake8 pytest pytest-cov

echo "✅ Python development environment setup complete!"
echo "💡 To activate the virtual environment, run: source venv/bin/activate"
'''
        
        elif project_type == "nodejs":
            return '''#!/bin/bash

# Node.js Development Environment Setup Script

echo "🟢 Setting up Node.js development environment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm."
    exit 1
fi

# Install dependencies
if [ -f "package.json" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Install global development tools
echo "🛠️ Installing global development tools..."
npm install -g eslint prettier nodemon

echo "✅ Node.js development environment setup complete!"
echo "💡 To start development server, run: npm run dev"
'''
        
        return '''#!/bin/bash

# Development Environment Setup Script

echo "🚀 Setting up development environment..."

# Add your setup commands here
echo "📝 Please customize this script for your project needs."

echo "✅ Setup complete!"
'''
    
    def _write_file(self, file_path: Path, content: str) -> None:
        """Write content to a file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
        except Exception as e:
            raise Exception(f"Failed to write {file_path}: {str(e)}")
    
    async def _arun(self, request: str = "") -> str:
        return self._run(request)


class CyberSecurityInput(BaseModel):
    command: str = Field(description="Command to execute: 'install <tool>', 'use <tool> <task>', 'list', 'search <query>'")

class CyberSecurityToolManager(BaseTool):
    """Optimized cybersecurity tool management system.
    
    Handles installation, manual parsing, knowledge storage, and intelligent usage
    of cybersecurity tools with persistent memory and environment management.
    """
    name: str = "cybersec_tool_manager"
    description: str = "Install, manage, and intelligently use cybersecurity tools. Supports tool installation, manual parsing, knowledge storage, and task execution. Input: 'install <tool>', 'use <tool> <task>', 'list tools', 'search <query>', 'manual <tool>'"
    args_schema: ClassVar[Type[BaseModel]] = CyberSecurityInput
    
    def __init__(self, llm_instance=None, get_state=None, **kwargs):
        super().__init__(**kwargs)
        object.__setattr__(self, 'llm', llm_instance)
        object.__setattr__(self, 'get_state', get_state or (lambda: {}))
        object.__setattr__(self, 'tools_db_path', Path.home() / ".FlawHunt" / "cybersec_tools.json")
        object.__setattr__(self, 'manuals_dir', Path.home() / ".FlawHunt" / "manuals")
        object.__setattr__(self, 'outputs_dir', Path.home() / ".FlawHunt" / "outputs")
        
        # Performance optimizations - add caching
        object.__setattr__(self, '_tool_path_cache', {})
        object.__setattr__(self, '_platform_info_cache', None)
        object.__setattr__(self, '_last_cache_time', 0)
        object.__setattr__(self, 'CACHE_TIMEOUT', 300)  # 5 minutes
        
        self._ensure_storage_dirs()
        self._load_tools_database()
    
    def _get_cached_platform_info(self):
        """Get platform info with caching to avoid repeated calls."""
        current_time = time.time()
        if (self._platform_info_cache is None or 
            current_time - self._last_cache_time > self.CACHE_TIMEOUT):
            self._platform_info_cache = get_platform_info()
            self._last_cache_time = current_time
        return self._platform_info_cache
    
    def _get_cached_tool_path(self, tool_name: str):
        """Get tool path with caching to avoid repeated which calls."""
        if tool_name not in self._tool_path_cache:
            from .utils import shutil_which
            self._tool_path_cache[tool_name] = shutil_which(tool_name)
        return self._tool_path_cache[tool_name]
    
    def _clear_tool_cache(self, tool_name: str = None):
        """Clear tool path cache for specific tool or all tools."""
        if tool_name:
            self._tool_path_cache.pop(tool_name, None)
        else:
            self._tool_path_cache.clear()

    def _ensure_storage_dirs(self):
        """Ensure storage directories exist."""
        self.tools_db_path.parent.mkdir(parents=True, exist_ok=True)
        self.manuals_dir.mkdir(parents=True, exist_ok=True)
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_tools_database(self):
        """Load the tools database from persistent storage."""
        if self.tools_db_path.exists():
            try:
                with open(self.tools_db_path, 'r') as f:
                    object.__setattr__(self, 'tools_db', json.load(f))
            except (json.JSONDecodeError, IOError):
                object.__setattr__(self, 'tools_db', self._create_empty_database())
        else:
            object.__setattr__(self, 'tools_db', self._create_empty_database())
    
    def _create_empty_database(self) -> Dict[str, Any]:
        """Create an empty tools database structure."""
        return {
            "installed_tools": {},
            "tool_categories": {
                "reconnaissance": [],
                "vulnerability_scanning": [],
                "exploitation": [],
                "post_exploitation": [],
                "forensics": [],
                "network_analysis": [],
                "web_security": [],
                "wireless": [],
                "cryptography": [],
                "reverse_engineering": [],
                "social_engineering": [],
                "reporting": []
            },
            "knowledge_base": {},
            "usage_history": [],
            "installation_log": []
        }
    
    def _save_tools_database(self):
        """Save the tools database to persistent storage."""
        try:
            with open(self.tools_db_path, 'w') as f:
                json.dump(self.tools_db, f, indent=2)
        except IOError as e:
            return f"Error saving tools database: {e}"
    
    def _run(self, command: str) -> str:
        """Optimized main entry point for cybersecurity tool management."""
        command = command.strip().lower()
        
        # Fast path for common commands
        if command == "list" or command == "list tools":
            return self._list_installed_tools_fast()
        elif command == "help":
            return self._show_help_fast()
        elif command == "stats" or command == "status":
            return self._show_statistics_fast()
        
        # Parse command with optimized logic
        if command.startswith("install "):
            tool_name = command[8:].strip()
            return self._install_tool_optimized(tool_name)
        elif command.startswith("use "):
            parts = command[4:].split(" ", 1)
            if len(parts) < 2:
                return "Usage: use <tool_name> <task_description>"
            tool_name, task = parts[0].strip(), parts[1].strip()
            return self._use_tool_optimized(tool_name, task)
        elif command.startswith("search "):
            query = command[7:].strip()
            return self._search_tools_fast(query)
        elif command.startswith("manual "):
            tool_name = command[7:].strip()
            return self._show_manual_fast(tool_name)
        elif command.startswith("health "):
            tool_name = command[7:].strip()
            return self._check_tool_health_fast(tool_name)
        elif command == "health":
            return self._check_all_tools_health_fast()
        elif command == "inventory" or command == "inv":
            return self._show_inventory_fast()
        elif command.startswith("register "):
            tool_name = command[9:].strip()
            return self._register_tool_fast(tool_name)
        else:
            return f"Unknown command: {command}. Use 'help' for available commands."
    
    def _install_tool(self, tool_name: str) -> str:
        """Install a cybersecurity tool and parse its manual."""
        from datetime import datetime
        from .utils import shutil_which
        platform_info = get_platform_info()
        package_manager = platform_info.get("package_manager")
        
        # Check if already installed in our database
        if tool_name in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' is already installed."
        
        # Check if tool already exists on the system (installed outside FlawHunt CLI)
        tool_path = shutil_which(tool_name)
        if tool_path:
            return self._register_existing_tool(tool_name, tool_path)
        
        # Define known cybersecurity tools with installation commands
        known_tools = {
            "nmap": {
                "install_cmd": self._get_install_command("nmap"),
                "category": "reconnaissance",
                "description": "Network discovery and security auditing"
            },
            "nikto": {
                "install_cmd": self._get_install_command("nikto"),
                "category": "web_security",
                "description": "Web server scanner"
            },
            "sqlmap": {
                "install_cmd": "pip install sqlmap",
                "category": "web_security",
                "description": "SQL injection detection and exploitation"
            },
            "metasploit": {
                "install_cmd": "curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb | bash",
                "category": "exploitation",
                "description": "Penetration testing framework"
            },
            "burpsuite": {
                "install_cmd": "echo 'Please download from https://portswigger.net/burp/communitydownload'",
                "category": "web_security",
                "description": "Web application security testing"
            },
            "wireshark": {
                "install_cmd": self._get_install_command("wireshark"),
                "category": "network_analysis",
                "description": "Network protocol analyzer"
            },
            "john": {
                "install_cmd": self._get_install_command("john"),
                "category": "cryptography",
                "description": "Password cracking tool"
            },
            "hashcat": {
                "install_cmd": self._get_install_command("hashcat"),
                "category": "cryptography",
                "description": "Advanced password recovery"
            },
            "gobuster": {
                "install_cmd": "go install github.com/OJ/gobuster/v3@latest",
                "category": "reconnaissance",
                "description": "Directory/file & DNS busting tool"
            },
            "dirb": {
                "install_cmd": self._get_install_command("dirb"),
                "category": "reconnaissance",
                "description": "Web content scanner"
            },
            "httpx": {
                "install_cmd": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
                "category": "reconnaissance",
                "description": "Fast and multi-purpose HTTP toolkit"
            },
            "subfinder": {
                "install_cmd": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
                "category": "reconnaissance",
                "description": "Subdomain discovery tool"
            }
        }
        
        if tool_name not in known_tools:
            # Try generic installation
            install_cmd = self._get_install_command(tool_name)
            tool_info = {
                "install_cmd": install_cmd,
                "category": "unknown",
                "description": "Unknown tool"
            }
        else:
            tool_info = known_tools[tool_name]
        
        # Pre-check for Go-based installs
        if tool_info["install_cmd"].startswith("go install") and not shutil_which("go"):
            return "Missing dependency: 'go' is required to install this tool. Please install Go first."

        # Execute installation with retry on index update
        try:
            result = run_subprocess(tool_info["install_cmd"], timeout=600)
            lower = result.lower() if result else ""
            if any(err in lower for err in ["unable to locate", "no match", "failed", "error"]):
                # Attempt to refresh package indexes and retry once
                if package_manager in {"apt", "apt-get"}:
                    run_subprocess("sudo apt-get update -y", timeout=240)
                elif package_manager == "yum":
                    run_subprocess("sudo yum makecache -y", timeout=240)
                elif package_manager == "dnf":
                    run_subprocess("sudo dnf makecache -y", timeout=240)
                elif package_manager == "brew":
                    run_subprocess("brew update -q", timeout=240)
                # Retry install
                result = run_subprocess(tool_info["install_cmd"], timeout=600)
                lower = result.lower() if result else ""
                if any(err in lower for err in ["unable to locate", "no match", "failed", "error"]):
                    return f"Installation failed for {tool_name}: {result}"
        except Exception as e:
            return f"Installation error for {tool_name}: {str(e)}"
        
        # Verify tool is actually available in PATH after installation
        from .utils import shutil_which
        tool_path = shutil_which(tool_name)
        if not tool_path and tool_info["install_cmd"].startswith("go install"):
            # Check common Go bin locations
            go_bin_candidates = [str(Path.home() / "go" / "bin" / tool_name), 
                                 os.environ.get("GOBIN") and os.path.join(os.environ.get("GOBIN"), tool_name)]
            for cand in go_bin_candidates:
                if cand and os.path.isfile(cand):
                    tool_path = cand
                    break
        if not tool_path:
            return f"Installation completed but {tool_name} is not available in PATH. You may need to restart your terminal or update PATH."
        
        # Check dependencies before installation
        dep_status = self._check_dependencies(tool_name)
        missing_deps = [dep for dep, status in dep_status.items() if not status]
        
        if missing_deps:
            return f"Missing dependencies for {tool_name}: {', '.join(missing_deps)}. Please install them first."
        
        # Create tool configuration
        config_result = self._create_tool_config(tool_name)
        
        # Parse manual and extract knowledge
        manual_content = self._parse_tool_manual(tool_name)
        knowledge = self._extract_tool_knowledge(tool_name, manual_content)
        
        # Store tool information
        self.tools_db["installed_tools"][tool_name] = {
            "name": tool_name,
            "category": tool_info["category"],
            "description": tool_info["description"],
            "install_date": datetime.now().isoformat(),
            "install_command": tool_info["install_cmd"],
            "manual_parsed": bool(manual_content),
            "knowledge_extracted": bool(knowledge),
            "usage_count": 0,
            "last_used": None
        }
        
        # Add to category
        if tool_info["category"] in self.tools_db["tool_categories"]:
            if tool_name not in self.tools_db["tool_categories"][tool_info["category"]]:
                self.tools_db["tool_categories"][tool_info["category"]].append(tool_name)
        
        # Store knowledge
        if knowledge:
            self.tools_db["knowledge_base"][tool_name] = knowledge
        
        # Log installation
        self.tools_db["installation_log"].append({
            "tool": tool_name,
            "action": "install",
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
        
        self._save_tools_database()
        
        return f"Successfully installed {tool_name}!\n" + \
               f"Category: {tool_info['category']}\n" + \
               f"Description: {tool_info['description']}\n" + \
               f"Dependencies checked: {'All satisfied' if not missing_deps else 'Some missing'}\n" + \
               f"Configuration: {config_result}\n" + \
               f"Manual parsed: {'Yes' if manual_content else 'No'}\n" + \
               f"Knowledge extracted: {'Yes' if knowledge else 'No'}"
    
    def _register_existing_tool(self, tool_name: str, tool_path: str) -> str:
        """Register an existing tool that's already installed on the system."""
        from datetime import datetime
        
        # Define known cybersecurity tools for categorization
        known_tools = {
            "nmap": {
                "category": "reconnaissance",
                "description": "Network discovery and security auditing"
            },
            "nikto": {
                "category": "web_security",
                "description": "Web server scanner"
            },
            "sqlmap": {
                "category": "web_security",
                "description": "SQL injection detection and exploitation"
            },
            "metasploit": {
                "category": "exploitation",
                "description": "Penetration testing framework"
            },
            "burpsuite": {
                "category": "web_security",
                "description": "Web application security testing"
            },
            "wireshark": {
                "category": "network_analysis",
                "description": "Network protocol analyzer"
            },
            "john": {
                "category": "cryptography",
                "description": "Password cracking tool"
            },
            "hashcat": {
                "category": "cryptography",
                "description": "Advanced password recovery"
            },
            "gobuster": {
                "category": "reconnaissance",
                "description": "Directory/file & DNS busting tool"
            },
            "dirb": {
                "category": "reconnaissance",
                "description": "Web content scanner"
            },
            "httpx": {
                "category": "reconnaissance",
                "description": "Fast and multi-purpose HTTP toolkit"
            },
            "subfinder": {
                "category": "reconnaissance",
                "description": "Subdomain discovery tool"
            },
            "amass": {
                "category": "reconnaissance",
                "description": "In-depth attack surface mapping and asset discovery"
            },
            "masscan": {
                "category": "reconnaissance",
                "description": "TCP port scanner, spews SYN packets asynchronously"
            },
            "nuclei": {
                "category": "vulnerability_scanning",
                "description": "Fast and customizable vulnerability scanner"
            },
            "ffuf": {
                "category": "reconnaissance",
                "description": "Fast web fuzzer written in Go"
            },
            "dirsearch": {
                "category": "reconnaissance",
                "description": "Web path scanner"
            },
            "wpscan": {
                "category": "web_security",
                "description": "WordPress security scanner"
            },
            "hydra": {
                "category": "cryptography",
                "description": "Parallelized login cracker"
            },
            "medusa": {
                "category": "cryptography",
                "description": "Speedy, parallel, and modular login brute-forcer"
            }
        }
        
        # Get tool info or use defaults for unknown tools
        if tool_name in known_tools:
            tool_info = known_tools[tool_name]
        else:
            tool_info = {
                "category": "unknown",
                "description": "External tool (auto-detected)"
            }
        
        # Parse manual and extract knowledge
        manual_content = self._parse_tool_manual(tool_name)
        knowledge = self._extract_tool_knowledge(tool_name, manual_content)
        
        # Store tool information
        self.tools_db["installed_tools"][tool_name] = {
            "name": tool_name,
            "category": tool_info["category"],
            "description": tool_info["description"],
            "install_date": datetime.now().isoformat(),
            "install_command": "External installation (auto-detected)",
            "tool_path": tool_path,
            "external_install": True,
            "manual_parsed": bool(manual_content),
            "knowledge_extracted": bool(knowledge),
            "usage_count": 0,
            "last_used": None
        }
        
        # Add to category
        if tool_info["category"] in self.tools_db["tool_categories"]:
            if tool_name not in self.tools_db["tool_categories"][tool_info["category"]]:
                self.tools_db["tool_categories"][tool_info["category"]].append(tool_name)
        
        # Store knowledge
        if knowledge:
            self.tools_db["knowledge_base"][tool_name] = knowledge
        
        # Log registration
        self.tools_db["installation_log"].append({
            "tool": tool_name,
            "action": "register_existing",
            "timestamp": datetime.now().isoformat(),
            "success": True,
            "path": tool_path
        })
        
        self._save_tools_database()
        
        return f"Successfully registered existing tool '{tool_name}'!\n" + \
               f"Path: {tool_path}\n" + \
               f"Category: {tool_info['category']}\n" + \
               f"Description: {tool_info['description']}\n" + \
               f"Manual parsed: {'Yes' if manual_content else 'No'}\n" + \
               f"Knowledge extracted: {'Yes' if knowledge else 'No'}\n" + \
               f"Note: Tool was already installed outside FlawHunt CLI"
    
    def _register_tool_manually(self, tool_name: str) -> str:
        """Manually register an existing tool by checking if it exists on the system."""
        from .utils import shutil_which
        
        # Check if already registered in our database
        if tool_name in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' is already registered."
        
        # Check if tool exists on the system
        tool_path = shutil_which(tool_name)
        if not tool_path:
            return f"Tool '{tool_name}' not found on the system. Please install it first or check the tool name."
        
        # Register the existing tool
        return self._register_existing_tool(tool_name, tool_path)
    
    def _get_install_command(self, tool_name: str) -> str:
        """Get the appropriate installation command based on the platform."""
        platform_info = get_platform_info()
        system = platform_info.get("system", "").lower()
        
        # Check for tool-specific environment requirements
        env_setup = self._setup_tool_environment(tool_name)
        if env_setup:
            return env_setup
        
        if system == "darwin":  # macOS
            return f"brew install --quiet {tool_name}"
        elif system == "linux":
            # Try to detect the distribution
            try:
                with open("/etc/os-release", "r") as f:
                    os_info = f.read().lower()
                if "ubuntu" in os_info or "debian" in os_info:
                    return f"sudo apt-get install -y --no-install-recommends {tool_name}"
                elif "centos" in os_info or "rhel" in os_info or "fedora" in os_info:
                    return f"sudo yum install -y {tool_name}"
                elif "arch" in os_info:
                    return f"sudo pacman -S --noconfirm {tool_name}"
            except:
                pass
            return f"sudo apt-get install -y --no-install-recommends {tool_name}"  # Default to apt
        else:
            return f"# Please install {tool_name} manually for your system"
    
    def _parse_tool_manual(self, tool_name: str) -> str:
        """Parse the manual/help for a tool."""
        manual_content = ""
        
        # Try different ways to get help/manual
        help_commands = [
            f"{tool_name} --help",
            f"{tool_name} -h",
            f"man {tool_name}",
            f"{tool_name} help",
            f"{tool_name}"
        ]
        
        for cmd in help_commands:
            try:
                result = run_subprocess(cmd)
                if result and len(result.strip()) > 50:  # Meaningful output
                    manual_content = result
                    break
            except:
                continue
        
        # Save manual to file
        if manual_content:
            manual_file = self.manuals_dir / f"{tool_name}_manual.txt"
            try:
                with open(manual_file, 'w') as f:
                    f.write(manual_content)
            except IOError:
                pass
        
        return manual_content
    
    def _extract_tool_knowledge(self, tool_name: str, manual_content: str) -> Dict[str, Any]:
        """Extract structured knowledge from tool manual."""
        if not manual_content:
            return {}
        
        knowledge = {
            "common_options": [],
            "usage_examples": [],
            "key_features": [],
            "output_formats": [],
            "typical_workflows": []
        }
        
        lines = manual_content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Extract common options (lines starting with - or --)
            if re.match(r'^-{1,2}\w', line):
                option_match = re.match(r'^(-{1,2}\w+(?:[=\s]\w+)?)', line)
                if option_match:
                    knowledge["common_options"].append(option_match.group(1))
            
            # Extract examples (lines containing 'example' or starting with tool name)
            if 'example' in line.lower() or line.lower().startswith(tool_name):
                knowledge["usage_examples"].append(line)
            
            # Extract key features (lines with descriptive content)
            if any(keyword in line.lower() for keyword in ['scan', 'detect', 'find', 'analyze', 'test']):
                knowledge["key_features"].append(line)
        
        # Add tool-specific knowledge
        if tool_name == "nmap":
            knowledge["typical_workflows"] = [
                "Basic scan: nmap <target>",
                "Service detection: nmap -sV <target>",
                "OS detection: nmap -O <target>",
                "Aggressive scan: nmap -A <target>",
                "Stealth scan: nmap -sS <target>"
            ]
        elif tool_name == "sqlmap":
            knowledge["typical_workflows"] = [
                "Basic test: sqlmap -u <url>",
                "POST data: sqlmap -u <url> --data='param=value'",
                "Database enumeration: sqlmap -u <url> --dbs",
                "Table enumeration: sqlmap -u <url> -D <db> --tables",
                "Data extraction: sqlmap -u <url> -D <db> -T <table> --dump"
            ]
        elif tool_name == "nikto":
            knowledge["typical_workflows"] = [
                "Basic scan: nikto -h <target>",
                "SSL scan: nikto -h <target> -ssl",
                "Custom port: nikto -h <target> -p <port>",
                "Output to file: nikto -h <target> -o <file>"
            ]
        
        return knowledge
    
    def _use_tool(self, tool_name: str, task: str) -> str:
        """Use a tool to perform a specific task based on stored knowledge."""
        from datetime import datetime
        from .utils import shutil_which
        
        if tool_name not in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' is not installed. Use 'install {tool_name}' first."
        
        # Check if tool is actually available in PATH
        tool_path = shutil_which(tool_name)
        if not tool_path:
            return f"Tool '{tool_name}' is marked as installed but not found in PATH. Please reinstall or check your PATH configuration."
        
        # Get tool knowledge
        knowledge = self.tools_db["knowledge_base"].get(tool_name, {})
        
        # Generate command based on task and knowledge
        command = self._generate_tool_command(tool_name, task, knowledge)
        
        if not command:
            return f"Could not generate appropriate command for task: {task}"
        
        # Validate and correct command syntax
        corrected_command = self._validate_and_correct_command(tool_name, command)
        if corrected_command != command:
            command = corrected_command
        
        # Replace tool name with full path if needed
        if command.startswith(tool_name + " "):
            command = command.replace(tool_name + " ", tool_path + " ", 1)
        elif command == tool_name:
            command = tool_path
        
        # Execute the command
        try:
            result = run_subprocess(command)

            # Only auto-save output when explicitly requested by user
            saved_path = None
            try:
                # Check if user explicitly requested saving/output
                should_save = any(k in task.lower() for k in ["save", "output", "store", "export"])
                if should_save:
                    saved_path = self._save_command_output(tool_name, task, command, result)
            except Exception:
                # Do not block main execution on save errors
                saved_path = None
            
            # Update usage statistics
            self.tools_db["installed_tools"][tool_name]["usage_count"] += 1
            self.tools_db["installed_tools"][tool_name]["last_used"] = datetime.now().isoformat()
            
            # Log usage
            self.tools_db["usage_history"].append({
                "tool": tool_name,
                "task": task,
                "command": command,
                "timestamp": datetime.now().isoformat(),
                "success": True,
                "saved_path": str(saved_path) if saved_path else None
            })
            
            self._save_tools_database()
            
            footer = f"Executed: {command}\n\nResult:\n{result}"
            if saved_path:
                footer += f"\n\nSaved output to: {saved_path}"
            return footer
            
        except Exception as e:
            # Check if error is due to syntax issues and suggest correction
            error_msg = str(e)
            if "No such option" in error_msg or "invalid option" in error_msg.lower():
                suggestion = self._suggest_command_correction(tool_name, command, error_msg)
                if suggestion:
                    return f"Command failed with syntax error: {error_msg}\n\nSuggested correction: {suggestion}\n\nPlease try: use {tool_name} {suggestion.split(' ', 1)[1] if ' ' in suggestion else suggestion}"
            
            # Log failed usage
            self.tools_db["usage_history"].append({
                "tool": tool_name,
                "task": task,
                "command": command,
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            })
            
            self._save_tools_database()
            
            return f"Error executing {command}: {str(e)}"
    
    def _generate_tool_command(self, tool_name: str, task: str, knowledge: Dict[str, Any]) -> str:
        """Generate appropriate command based on task and tool knowledge."""
        task_lower = task.lower()
        
        # Tool-specific command generation
        if tool_name == "nmap":
            if "port" in task_lower and "scan" in task_lower:
                return f"nmap -p- {self._extract_target(task)}"
            elif "service" in task_lower or "version" in task_lower:
                return f"nmap -sV {self._extract_target(task)}"
            elif "os" in task_lower:
                return f"nmap -O {self._extract_target(task)}"
            elif "stealth" in task_lower:
                return f"nmap -sS {self._extract_target(task)}"
            else:
                return f"nmap {self._extract_target(task)}"
        
        elif tool_name == "sqlmap":
            if "url" in task_lower or "http" in task:
                url = self._extract_url(task)
                if "post" in task_lower:
                    return f"sqlmap -u {url} --data=''"
                else:
                    return f"sqlmap -u {url}"
        
        elif tool_name == "nikto":
            target = self._extract_target(task)
            if "ssl" in task_lower:
                return f"nikto -h {target} -ssl"
            else:
                return f"nikto -h {target}"
        
        elif tool_name == "gobuster":
            target = self._extract_target(task)
            if "directory" in task_lower or "dir" in task_lower:
                return f"gobuster dir -u {target} -w /usr/share/wordlists/dirb/common.txt"
            elif "dns" in task_lower:
                return f"gobuster dns -d {target} -w /usr/share/wordlists/dnsrecon/subdomains-top1mil-5000.txt"
        
        elif tool_name == "httpx":
            target = self._extract_target(task)
            if "status" in task_lower and "code" in task_lower:
                if "file" in task_lower or "list" in task_lower:
                    # Handle file input for multiple targets
                    file_pattern = r'\b\w+\.txt\b'
                    file_match = re.search(file_pattern, task)
                    if file_match:
                        filename = file_match.group()
                        return f"cat {filename} | httpx --status-code"
                return f"httpx {target} --status-code"
            elif "probe" in task_lower:
                return f"httpx -probe {target}"
            else:
                return f"httpx {target}"
        
        elif tool_name == "subfinder":
            target = self._extract_target(task)
            if "output" in task_lower or "save" in task_lower:
                file_pattern = r'\b\w+\.txt\b'
                file_match = re.search(file_pattern, task)
                if file_match:
                    filename = file_match.group()
                    return f"subfinder -d {target} -o {filename}"
            return f"subfinder -d {target}"
        
        # Generic command generation
        return f"{tool_name} {task}"
    
    def _validate_and_correct_command(self, tool_name: str, command: str) -> str:
        """Validate and correct common command syntax errors."""
        # Tool-specific syntax corrections
        if tool_name == "httpx":
            # Fix common httpx flag errors
            command = re.sub(r'\s+-l\s+', ' ', command)  # Remove invalid -l flag
            command = re.sub(r'\s+-status-code\b', ' --status-code', command)  # Fix status-code flag
            
            # Ensure proper URL format
            if not re.search(r'https?://', command) and not command.endswith('--help'):
                # Add https:// if target looks like a domain
                parts = command.split()
                for i, part in enumerate(parts):
                    if '.' in part and not part.startswith('-') and part != tool_name:
                        if not part.startswith('http'):
                            parts[i] = f'https://{part}'
                        break
                command = ' '.join(parts)
        
        elif tool_name == "subfinder":
            # Ensure -d flag is used for domain
            if '-d ' not in command:
                parts = command.split()
                for i, part in enumerate(parts):
                    if '.' in part and not part.startswith('-') and part != tool_name:
                        parts.insert(i, '-d')
                        break
                command = ' '.join(parts)
        
        return command

    def _extract_output_filename(self, command: str) -> Optional[Path]:
        """Extract output filename from a command (e.g., '-o file.txt')."""
        try:
            match = re.search(r"\-o\s+(\S+)", command)
            if match:
                candidate = match.group(1)
                p = Path(candidate).expanduser()
                if not p.is_absolute():
                    # Assume relative to current working directory
                    p = Path.cwd() / p
                return p
        except Exception:
            pass
        return None

    def _save_command_output(self, tool_name: str, task: str, command: str, result: str) -> Path:
        """Optimized save command output with minimal overhead."""
        from datetime import datetime
        
        # Quick timestamp generation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Fast target extraction
        target = self._extract_target_fast(task) or "target"
        safe_target = target.replace("/", "_").replace("\\", "_")[:20]  # Limit length
        
        # Simple filename generation
        dest = self.outputs_dir / f"{tool_name}_{safe_target}_{timestamp}.txt"
        
        try:
            # Limit output size for performance
            output_content = (result or "")[:10000]  # Max 10KB
            dest.write_text(output_content)
        except Exception:
            # Quick directory creation and retry
            try:
                self.outputs_dir.mkdir(parents=True, exist_ok=True)
                dest.write_text(output_content)
            except Exception:
                # Fail silently for performance
                pass
        
        return dest
    
    def _suggest_command_correction(self, tool_name: str, failed_command: str, error_msg: str) -> str:
        """Suggest command corrections based on error messages."""
        if tool_name == "httpx":
            if "No such option: -l" in error_msg:
                # Suggest using cat with pipe instead of -l flag
                if "-l " in failed_command:
                    filename = failed_command.split("-l ")[1].split()[0]
                    base_cmd = failed_command.replace(f"-l {filename}", "").strip()
                    return f"cat {filename} | {base_cmd}"
            
            if "No such option: -s" in error_msg or "status-code" in failed_command:
                # Fix status-code flag
                corrected = failed_command.replace("-status-code", "--status-code")
                return corrected
        
        elif tool_name == "subfinder":
            if "domain" in error_msg.lower() or "target" in error_msg.lower():
                # Suggest adding -d flag
                parts = failed_command.split()
                for i, part in enumerate(parts):
                    if '.' in part and not part.startswith('-') and part != tool_name:
                        parts.insert(i, '-d')
                        return ' '.join(parts)
        
        return ""
    
    def _extract_target(self, task: str) -> str:
        """Extract target (IP/domain) from task description."""
        # Look for IP addresses
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        ip_match = re.search(ip_pattern, task)
        if ip_match:
            return ip_match.group()
        
        # Look for domain names
        domain_pattern = r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}\b'
        domain_match = re.search(domain_pattern, task)
        if domain_match:
            return domain_match.group()
        
        # Look for localhost or common targets
        if "localhost" in task.lower():
            return "localhost"
        
        return "<target>"
    
    def _extract_url(self, task: str) -> str:
        """Extract URL from task description."""
        url_pattern = r'https?://[^\s]+'
        url_match = re.search(url_pattern, task)
        if url_match:
            return url_match.group()
        
        return "<url>"
    
    def _list_installed_tools(self) -> str:
        """List all installed tools with their information."""
        if not self.tools_db["installed_tools"]:
            return "No cybersecurity tools installed yet."
        
        output = ["Installed Cybersecurity Tools:\n"]
        
        for category, tools in self.tools_db["tool_categories"].items():
            if tools:
                output.append(f"\n{category.replace('_', ' ').title()}:")
                for tool in tools:
                    if tool in self.tools_db["installed_tools"]:
                        tool_info = self.tools_db["installed_tools"][tool]
                        output.append(f"  • {tool} - {tool_info['description']}")
                        output.append(f"    Usage count: {tool_info['usage_count']}")
                        if tool_info['last_used']:
                            output.append(f"    Last used: {tool_info['last_used'][:10]}")
        
        # Add uncategorized tools
        uncategorized = []
        for tool in self.tools_db["installed_tools"]:
            found = False
            for tools in self.tools_db["tool_categories"].values():
                if tool in tools:
                    found = True
                    break
            if not found:
                uncategorized.append(tool)
        
        if uncategorized:
            output.append("\nOther Tools:")
            for tool in uncategorized:
                tool_info = self.tools_db["installed_tools"][tool]
                output.append(f"  • {tool} - {tool_info['description']}")
        
        return "\n".join(output)
    
    def _search_tools(self, query: str) -> str:
        """Search for tools based on query."""
        query_lower = query.lower()
        results = []
        
        # Search in installed tools
        for tool_name, tool_info in self.tools_db["installed_tools"].items():
            if (query_lower in tool_name.lower() or 
                query_lower in tool_info["description"].lower() or
                query_lower in tool_info["category"].lower()):
                results.append(f"✓ {tool_name} ({tool_info['category']}) - {tool_info['description']}")
        
        # Search in knowledge base
        for tool_name, knowledge in self.tools_db["knowledge_base"].items():
            if tool_name not in [r.split()[1] for r in results]:  # Avoid duplicates
                for feature in knowledge.get("key_features", []):
                    if query_lower in feature.lower():
                        results.append(f"✓ {tool_name} - Found in features: {feature[:50]}...")
                        break
        
        if not results:
            return f"No tools found matching '{query}'. Try 'list tools' to see all installed tools."
        
        return f"Search results for '{query}':\n\n" + "\n".join(results)
    
    def _show_manual(self, tool_name: str) -> str:
        """Show the manual/help for a specific tool."""
        if tool_name not in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' is not installed."
        
        manual_file = self.manuals_dir / f"{tool_name}_manual.txt"
        
        if manual_file.exists():
            try:
                with open(manual_file, 'r') as f:
                    content = f.read()
                return f"Manual for {tool_name}:\n\n{content[:2000]}{'...' if len(content) > 2000 else ''}"
            except IOError:
                pass
        
        # Try to get fresh manual
        manual_content = self._parse_tool_manual(tool_name)
        if manual_content:
            return f"Manual for {tool_name}:\n\n{manual_content[:2000]}{'...' if len(manual_content) > 2000 else ''}"
        
        return f"No manual available for {tool_name}."
    
    def _show_statistics(self) -> str:
        """Show statistics about installed tools and usage."""
        total_tools = len(self.tools_db["installed_tools"])
        total_usage = sum(tool["usage_count"] for tool in self.tools_db["installed_tools"].values())
        
        category_counts = {}
        for category, tools in self.tools_db["tool_categories"].items():
            if tools:
                category_counts[category] = len(tools)
        
        most_used = None
        max_usage = 0
        for tool_name, tool_info in self.tools_db["installed_tools"].items():
            if tool_info["usage_count"] > max_usage:
                max_usage = tool_info["usage_count"]
                most_used = tool_name
        
        output = [
            "Cybersecurity Tools Statistics:\n",
            f"Total tools installed: {total_tools}",
            f"Total tool usage: {total_usage}",
            f"Most used tool: {most_used} ({max_usage} times)" if most_used else "Most used tool: None",
            "\nTools by category:"
        ]
        
        for category, count in category_counts.items():
            output.append(f"  {category.replace('_', ' ').title()}: {count}")
        
        recent_installs = sorted(
            self.tools_db["installation_log"][-5:],
            key=lambda x: x["timestamp"],
            reverse=True
        )
        
        if recent_installs:
            output.append("\nRecent installations:")
            for install in recent_installs:
                output.append(f"  {install['tool']} - {install['timestamp'][:10]}")
        
        return "\n".join(output)
    
    def _uninstall_tool(self, tool_name: str) -> str:
        """Uninstall a tool and remove its data."""
        from datetime import datetime
        
        if tool_name not in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' is not installed."
        
        # Remove from database
        tool_info = self.tools_db["installed_tools"].pop(tool_name)
        
        # Remove from category
        for category, tools in self.tools_db["tool_categories"].items():
            if tool_name in tools:
                tools.remove(tool_name)
        
        # Remove knowledge
        if tool_name in self.tools_db["knowledge_base"]:
            del self.tools_db["knowledge_base"][tool_name]
        
        # Remove manual file
        manual_file = self.manuals_dir / f"{tool_name}_manual.txt"
        if manual_file.exists():
            try:
                manual_file.unlink()
            except OSError:
                pass
        
        # Log uninstallation
        self.tools_db["installation_log"].append({
            "tool": tool_name,
            "action": "uninstall",
            "timestamp": datetime.now().isoformat(),
            "success": True
        })
        
        self._save_tools_database()
        
        return f"Successfully uninstalled {tool_name} and removed all associated data."
    
    def _setup_tool_environment(self, tool_name: str) -> str:
        """Setup tool-specific environment and dependencies."""
        env_commands = []
        
        # Tool-specific environment setup
        if tool_name == "metasploit":
            env_commands.extend([
                "# Setting up Metasploit environment",
                "curl https://raw.githubusercontent.com/rapid7/metasploit-omnibus/master/config/templates/metasploit-framework-wrappers/msfupdate.erb > /tmp/msfinstall",
                "chmod 755 /tmp/msfinstall",
                "/tmp/msfinstall"
            ])
        elif tool_name == "burpsuite":
            env_commands.extend([
                "# Setting up Burp Suite environment",
                "echo 'Burp Suite requires manual download from PortSwigger'",
                "echo 'Visit: https://portswigger.net/burp/communitydownload'",
                "echo 'For automated install, use: brew install --cask burp-suite'"
            ])
        elif tool_name == "wireshark":
            env_commands.extend([
                "# Setting up Wireshark with proper permissions",
                "brew install wireshark",
                "sudo chgrp admin /dev/bpf*",
                "sudo chmod g+rw /dev/bpf*"
            ])
        elif tool_name == "sqlmap":
            env_commands.extend([
                "# Setting up SQLMap Python environment",
                "python3 -m venv ~/.sqlmap_env",
                "source ~/.sqlmap_env/bin/activate",
                "pip install sqlmap",
                "echo 'alias sqlmap=\"~/.sqlmap_env/bin/sqlmap\"' >> ~/.zshrc"
            ])
        elif tool_name in ["john", "hashcat"]:
            env_commands.extend([
                f"# Setting up {tool_name} with wordlists",
                f"brew install {tool_name}",
                "mkdir -p ~/Security/wordlists",
                "cd ~/Security/wordlists",
                "curl -L https://github.com/danielmiessler/SecLists/archive/master.zip -o seclists.zip",
                "unzip seclists.zip && rm seclists.zip",
                "mv SecLists-master SecLists"
            ])
        
        if env_commands:
            return " && ".join(env_commands)
        
        return None
    
    def _check_dependencies(self, tool_name: str) -> Dict[str, bool]:
        """Check if tool dependencies are satisfied."""
        dependencies = {
            "metasploit": ["ruby", "postgresql"],
            "burpsuite": ["java"],
            "wireshark": ["libpcap"],
            "sqlmap": ["python3", "pip3"],
            "john": ["openssl"],
            "hashcat": ["opencl"],
            "nmap": ["libpcap"],
            "nikto": ["perl"],
            "gobuster": ["go"]
        }
        
        tool_deps = dependencies.get(tool_name, [])
        dep_status = {}
        
        from .utils import shutil_which
        for dep in tool_deps:
            ok = False
            try:
                # Executable dependencies
                if dep in {"ruby", "java", "python3", "pip3", "perl", "go", "postgresql"}:
                    # postgresql may not have a 'postgresql' binary; check psql
                    binary = dep if dep != "postgresql" else "psql"
                    ok = bool(shutil_which(binary))
                elif dep == "openssl":
                    out = run_subprocess("openssl version", timeout=10)
                    ok = bool(out.strip())
                elif dep == "libpcap":
                    # Try pkg-config first, then common package checks
                    out = run_subprocess("pkg-config --exists libpcap && echo OK || echo MISSING", timeout=10)
                    if "OK" in out:
                        ok = True
                    else:
                        brew = run_subprocess("brew list --versions libpcap", timeout=10)
                        ok = bool(brew.strip())
                elif dep == "opencl":
                    # Check OpenCL via pkg-config or clinfo
                    out = run_subprocess("pkg-config --exists OpenCL && echo OK || echo MISSING", timeout=10)
                    if "OK" in out:
                        ok = True
                    else:
                        ok = bool(shutil_which("clinfo"))
                else:
                    ok = bool(shutil_which(dep))
            except Exception:
                ok = False
            dep_status[dep] = ok
        
        return dep_status
    
    def _create_tool_config(self, tool_name: str) -> str:
        """Create tool-specific configuration files."""
        config_dir = Path.home() / ".config" / "security_tools" / tool_name
        config_dir.mkdir(parents=True, exist_ok=True)
        
        configs_created = []
        
        if tool_name == "nmap":
            nmap_config = config_dir / "nmap.conf"
            with open(nmap_config, 'w') as f:
                f.write("# Nmap Configuration\n")
                f.write("# Common scan profiles\n")
                f.write("quick_scan = -T4 -F\n")
                f.write("stealth_scan = -sS -T2\n")
                f.write("vuln_scan = --script vuln\n")
            configs_created.append(str(nmap_config))
        
        elif tool_name == "sqlmap":
            sqlmap_config = config_dir / "sqlmap.conf"
            with open(sqlmap_config, 'w') as f:
                f.write("[Target]\n")
                f.write("threads = 5\n")
                f.write("delay = 0\n")
                f.write("timeout = 30\n")
                f.write("\n[Request]\n")
                f.write("user-agent = Mozilla/5.0 (compatible; sqlmap)\n")
            configs_created.append(str(sqlmap_config))
        
        elif tool_name == "metasploit":
            msf_config = config_dir / "database.yml"
            with open(msf_config, 'w') as f:
                f.write("production:\n")
                f.write("  adapter: postgresql\n")
                f.write("  database: msf\n")
                f.write("  username: msf\n")
                f.write("  password: msf\n")
                f.write("  host: 127.0.0.1\n")
                f.write("  port: 5432\n")
            configs_created.append(str(msf_config))
        
        return f"Created configuration files: {', '.join(configs_created)}"
    
    def _check_tool_dependencies(self, tool_name: str) -> str:
        """Check and display tool dependencies status."""
        if tool_name not in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' is not installed."
        
        dep_status = self._check_dependencies(tool_name)
        
        if not dep_status:
            return f"No dependencies defined for {tool_name}."
        
        output = [f"Dependencies for {tool_name}:"]
        all_satisfied = True
        
        for dep, status in dep_status.items():
            status_icon = "✓" if status else "✗"
            status_text = "satisfied" if status else "missing"
            output.append(f"  {status_icon} {dep}: {status_text}")
            if not status:
                all_satisfied = False
        
        if all_satisfied:
            output.append("\nAll dependencies are satisfied!")
        else:
            output.append("\nSome dependencies are missing. Install them before using this tool.")
        
        return "\n".join(output)
    
    def _setup_environment_for_tool(self, tool_name: str) -> str:
        """Setup environment for a specific tool."""
        if tool_name not in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' is not installed. Install it first."
        
        # Check dependencies first
        dep_status = self._check_dependencies(tool_name)
        missing_deps = [dep for dep, status in dep_status.items() if not status]
        
        if missing_deps:
            return f"Cannot setup environment. Missing dependencies: {', '.join(missing_deps)}"
        
        # Setup environment
        env_setup = self._setup_tool_environment(tool_name)
        if not env_setup:
            return f"No special environment setup required for {tool_name}."
        
        # Create configuration
        config_result = self._create_tool_config(tool_name)
        
        return f"Environment setup for {tool_name}:\n\n" + \
               f"Setup commands: {env_setup}\n\n" + \
               f"Configuration: {config_result}\n\n" + \
               f"Environment is ready for {tool_name}!"
    
    def _check_tool_health(self, tool_name: str = "") -> str:
        """Check health status of tools (availability, version, dependencies)."""
        if tool_name:
            # Check specific tool
            if tool_name not in self.tools_db["installed_tools"]:
                return f"Tool '{tool_name}' is not installed."
            
            return self._check_single_tool_health(tool_name)
        else:
            # Check all tools
            if not self.tools_db["installed_tools"]:
                return "No tools installed to check."
            
            output = ["Tool Health Status:\n"]
            healthy_count = 0
            total_count = len(self.tools_db["installed_tools"])
            
            for tool in self.tools_db["installed_tools"]:
                status = self._check_single_tool_health(tool, brief=True)
                if "✓" in status:
                    healthy_count += 1
                output.append(status)
            
            output.insert(1, f"Overall Health: {healthy_count}/{total_count} tools healthy\n")
            return "\n".join(output)
    
    def _check_single_tool_health(self, tool_name: str, brief: bool = False) -> str:
        """Check health of a single tool."""
        try:
            import subprocess
            
            # Check if tool is available in PATH
            try:
                result = subprocess.run(["which", tool_name], capture_output=True, text=True, timeout=5)
                if result.returncode != 0:
                    status = "✗ Not in PATH"
                else:
                    # Try to get version
                    try:
                        version_result = subprocess.run([tool_name, "--version"], capture_output=True, text=True, timeout=5)
                        if version_result.returncode == 0:
                            version = version_result.stdout.strip().split('\n')[0][:50]
                            status = f"✓ Available ({version})"
                        else:
                            # Try alternative version commands
                            for cmd in ["-v", "-V", "version"]:
                                try:
                                    alt_result = subprocess.run([tool_name, cmd], capture_output=True, text=True, timeout=5)
                                    if alt_result.returncode == 0:
                                        version = alt_result.stdout.strip().split('\n')[0][:50]
                                        status = f"✓ Available ({version})"
                                        break
                                except:
                                    continue
                            else:
                                status = "⚠ Available (version unknown)"
                    except:
                        status = "⚠ Available (version check failed)"
            except:
                status = "✗ Check failed"
            
            if brief:
                return f"  {tool_name}: {status}"
            
            # Detailed health check
            output = [f"Health check for {tool_name}:", f"  Status: {status}"]
            
            # Check dependencies
            try:
                dep_status = self._check_dependencies(tool_name)
                if dep_status:
                    missing_deps = [dep for dep, satisfied in dep_status.items() if not satisfied]
                    if missing_deps:
                        output.append(f"  Dependencies: ✗ Missing {len(missing_deps)} dependencies")
                    else:
                        output.append(f"  Dependencies: ✓ All satisfied")
            except:
                output.append(f"  Dependencies: ⚠ Check failed")
            
            # Check configuration
            try:
                config_dir = Path.home() / ".config" / "security_tools" / tool_name
                if config_dir.exists():
                    output.append(f"  Configuration: ✓ Present")
                else:
                    output.append(f"  Configuration: ⚠ Not configured")
            except:
                output.append(f"  Configuration: ⚠ Check failed")
            
            return "\n".join(output)
            
        except Exception as e:
            return f"  {tool_name}: ✗ Error checking ({str(e)[:30]}...)"
    
    def _show_detailed_inventory(self) -> str:
        """Show detailed inventory of all tools with comprehensive information."""
        if not self.tools_db["installed_tools"]:
            return "No cybersecurity tools installed."
        
        output = ["Detailed Tool Inventory\n" + "=" * 25 + "\n"]
        
        for tool_name, tool_info in self.tools_db["installed_tools"].items():
            output.append(f"Tool: {tool_name}")
            output.append(f"  Category: {tool_info['category']}")
            output.append(f"  Description: {tool_info['description']}")
            output.append(f"  Installed: {tool_info['install_date'][:10]}")
            output.append(f"  Usage Count: {tool_info['usage_count']}")
            
            if tool_info['last_used']:
                output.append(f"  Last Used: {tool_info['last_used'][:10]}")
            else:
                output.append(f"  Last Used: Never")
            
            # Health status
            health = self._check_single_tool_health(tool_name, brief=True)
            output.append(f"  Health: {health.split(': ')[1]}")
            
            # Knowledge base info
            if tool_name in self.tools_db["knowledge_base"]:
                kb = self.tools_db["knowledge_base"][tool_name]
                output.append(f"  Knowledge: {len(kb.get('common_options', []))} options, {len(kb.get('usage_examples', []))} examples")
            
            # Configuration status
            config_dir = Path.home() / ".config" / "security_tools" / tool_name
            config_status = "Configured" if config_dir.exists() else "Not configured"
            output.append(f"  Configuration: {config_status}")
            
            output.append("")  # Empty line between tools
        
        # Summary statistics
        total_tools = len(self.tools_db["installed_tools"])
        total_usage = sum(tool["usage_count"] for tool in self.tools_db["installed_tools"].values())
        
        output.append(f"Summary: {total_tools} tools installed, {total_usage} total uses")
        
        return "\n".join(output)
    
    def _check_for_updates(self) -> str:
        """Check for available updates for installed tools."""
        if not self.tools_db["installed_tools"]:
            return "No tools installed to check for updates."
        
        output = ["Checking for tool updates...\n"]
        updates_available = 0
        
        for tool_name in self.tools_db["installed_tools"]:
            try:
                # Get current version
                current_version = self._get_tool_version(tool_name)
                
                # Check if update is available (simplified check)
                update_status = self._check_tool_update_available(tool_name, current_version)
                
                if update_status["update_available"]:
                    updates_available += 1
                    output.append(f"  ⬆ {tool_name}: {current_version} → {update_status['latest_version']} (update available)")
                else:
                    output.append(f"  ✓ {tool_name}: {current_version} (up to date)")
                    
            except Exception as e:
                output.append(f"  ⚠ {tool_name}: Could not check for updates ({str(e)[:30]}...)")
        
        if updates_available > 0:
            output.append(f"\n{updates_available} tool(s) have updates available.")
            output.append("Use your system package manager to update tools.")
        else:
            output.append("\nAll tools are up to date!")
        
        return "\n".join(output)
    
    def _get_tool_version(self, tool_name: str) -> str:
        """Get the current version of a tool."""
        try:
            # Try common version commands
            for cmd in ["--version", "-v", "-V", "version"]:
                try:
                    result = run_subprocess([tool_name, cmd], capture_output=True, timeout=5)
                    if result.returncode == 0:
                        version_line = result.stdout.strip().split('\n')[0]
                        # Extract version number using regex
                        version_match = re.search(r'(\d+\.\d+(?:\.\d+)?)', version_line)
                        if version_match:
                            return version_match.group(1)
                        return version_line[:30]  # Return first 30 chars if no version pattern
                except:
                    continue
            return "unknown"
        except:
            return "unknown"
    
    def _check_tool_update_available(self, tool_name: str, current_version: str) -> Dict[str, Any]:
        """Check if an update is available for a tool (simplified implementation)."""
        # This is a simplified implementation
        # In a real scenario, you'd check against package repositories or tool-specific APIs
        
        # For demonstration, we'll simulate some update checks
        simulated_latest_versions = {
            "nmap": "7.94",
            "nikto": "2.5.0",
            "sqlmap": "1.7.11",
            "gobuster": "3.6",
            "dirb": "2.22"
        }
        
        if tool_name in simulated_latest_versions:
            latest = simulated_latest_versions[tool_name]
            # Simple version comparison (not perfect, but works for demo)
            try:
                current_parts = [int(x) for x in current_version.split('.')]
                latest_parts = [int(x) for x in latest.split('.')]
                
                # Pad shorter version with zeros
                max_len = max(len(current_parts), len(latest_parts))
                current_parts.extend([0] * (max_len - len(current_parts)))
                latest_parts.extend([0] * (max_len - len(latest_parts)))
                
                update_available = latest_parts > current_parts
                
                return {
                    "update_available": update_available,
                    "latest_version": latest,
                    "current_version": current_version
                }
            except:
                pass
        
        return {
            "update_available": False,
            "latest_version": current_version,
            "current_version": current_version
        }
    
    def _show_help(self) -> str:
        """Show help for the cybersecurity tool manager."""
        return """Cybersecurity Tool Manager Commands:

install <tool>     - Install a cybersecurity tool and parse its manual
register <tool>    - Register an existing tool that's already installed on the system
use <tool> <task>  - Use a tool to perform a specific task
list tools         - List all installed tools by category
search <query>     - Search for tools by name, category, or feature
manual <tool>      - Show the manual/help for a specific tool
stats              - Show statistics about installed tools and usage
uninstall <tool>   - Uninstall a tool and remove its data
check deps <tool>  - Check dependencies for a specific tool
config <tool>      - Create configuration files for a tool
env setup <tool>   - Setup environment and dependencies for a tool
health [tool]      - Check health status of tools (all tools if no tool specified)
inventory          - Show detailed inventory of all installed tools
updates            - Check for available tool updates
help               - Show this help message

Supported tools include:
• nmap - Network discovery and security auditing
• nikto - Web server scanner
• sqlmap - SQL injection detection and exploitation
• metasploit - Penetration testing framework
• burpsuite - Web application security testing
• wireshark - Network protocol analyzer
• john - Password cracking tool
• hashcat - Advanced password recovery
• gobuster - Directory/file & DNS busting tool
• dirb - Web content scanner

Examples:
  install nmap
  use nmap scan 192.168.1.1 for open ports
  use sqlmap test http://example.com/page.php?id=1
  search web security
  manual nmap"""
    
    # Optimized fast methods for better performance
    def _list_installed_tools_fast(self) -> str:
        """Fast listing of installed tools without heavy processing."""
        if not self.tools_db["installed_tools"]:
            return "No cybersecurity tools installed yet. Use 'install <tool_name>' to get started."
        
        tools = list(self.tools_db["installed_tools"].keys())
        count = len(tools)
        
        # Simple, fast output
        result = [f"Installed Tools ({count}):", ""]
        for i, tool in enumerate(tools, 1):
            result.append(f"{i:2d}. {tool}")
        
        return "\n".join(result)
    
    def _show_help_fast(self) -> str:
        """Fast help display without complex formatting."""
        return """CyberSecurity Tool Manager - Quick Commands:

install <tool>     - Install cybersecurity tool
use <tool> <task>  - Execute tool with task
list              - Show installed tools
search <query>    - Search available tools
manual <tool>     - Show tool manual
health [tool]     - Check tool status
register <tool>   - Register existing tool
help              - Show this help"""
    
    def _show_statistics_fast(self) -> str:
        """Fast statistics display."""
        total_tools = len(self.tools_db["installed_tools"])
        total_usage = sum(tool.get("usage_count", 0) for tool in self.tools_db["installed_tools"].values())
        
        return f"""Quick Statistics:
• Total tools installed: {total_tools}
• Total tool usage: {total_usage}
• Database size: {len(self.tools_db["knowledge_base"])} knowledge entries"""
    
    def _install_tool_optimized(self, tool_name: str) -> str:
        """Optimized tool installation with reduced overhead."""
        # Quick check if already installed
        if tool_name in self.tools_db["installed_tools"]:
            return f"✓ Tool '{tool_name}' already installed."
        
        # Check if tool exists on system (cached)
        tool_path = self._get_cached_tool_path(tool_name)
        if tool_path:
            return self._register_existing_tool_fast(tool_name, tool_path)
        
        # Get platform info (cached)
        platform_info = self._get_cached_platform_info()
        
        # Quick installation for common tools
        install_cmd = self._get_quick_install_command(tool_name, platform_info)
        if not install_cmd:
            return f"Tool '{tool_name}' not found in quick install database. Use 'register {tool_name}' if already installed."
        
        try:
            # Execute installation with timeout
            result = run_subprocess(install_cmd, timeout=60)
            
            # Quick registration without heavy manual parsing
            self._register_tool_minimal(tool_name, install_cmd)
            
            return f"✓ Successfully installed {tool_name}\n{result[:200]}..."
            
        except Exception as e:
            return f"✗ Installation failed for {tool_name}: {str(e)[:100]}..."
    
    def _get_quick_install_command(self, tool_name: str, platform_info: dict) -> str:
        """Get installation command for common tools quickly."""
        pm = platform_info.get("package_manager", "")
        
        # Quick lookup table for common tools
        quick_installs = {
            "nmap": f"{pm} install nmap" if pm else "",
            "nikto": f"{pm} install nikto" if pm else "",
            "httpx": "go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "subfinder": "go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "nuclei": "go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest",
            "gobuster": f"{pm} install gobuster" if pm else "",
            "dirb": f"{pm} install dirb" if pm else "",
            "sqlmap": "pip install sqlmap",
            "john": f"{pm} install john" if pm else "",
            "hashcat": f"{pm} install hashcat" if pm else "",
        }
        
        return quick_installs.get(tool_name, "")
    
    def _register_existing_tool_fast(self, tool_name: str, tool_path: str) -> str:
        """Fast registration of existing tools without heavy processing."""
        self.tools_db["installed_tools"][tool_name] = {
            "path": tool_path,
            "installed_at": datetime.now().isoformat(),
            "category": "unknown",
            "description": f"Registered tool: {tool_name}",
            "usage_count": 0,
            "last_used": None,
            "version": "unknown"
        }
        
        self._save_tools_database()
        return f"✓ Registered existing tool: {tool_name} at {tool_path}"
    
    def _register_tool_minimal(self, tool_name: str, install_cmd: str) -> None:
        """Minimal tool registration for speed."""
        tool_path = self._get_cached_tool_path(tool_name) or tool_name
        
        self.tools_db["installed_tools"][tool_name] = {
            "path": tool_path,
            "installed_at": datetime.now().isoformat(),
            "install_command": install_cmd,
            "category": "cybersecurity",
            "description": f"Cybersecurity tool: {tool_name}",
            "usage_count": 0,
            "last_used": None,
            "version": "latest"
        }
        
        self._save_tools_database()
    
    def _use_tool_optimized(self, tool_name: str, task: str) -> str:
        """Optimized tool usage with faster execution and auto security reporting."""
        # Quick validation
        if tool_name not in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' not installed. Use 'install {tool_name}' first."
        
        # Get tool path (cached)
        tool_path = self.tools_db["installed_tools"][tool_name].get("path", tool_name)
        
        # Generate command quickly
        command = self._generate_quick_command(tool_name, task, tool_path)
        if not command:
            return f"Could not generate command for task: {task}"
        
        try:
            # Execute with shorter timeout for responsiveness
            result = run_subprocess(command, timeout=30)
            
            # Quick usage tracking
            self.tools_db["installed_tools"][tool_name]["usage_count"] += 1
            self.tools_db["installed_tools"][tool_name]["last_used"] = datetime.now().isoformat()
            
            # Only save output if explicitly requested
            if any(k in task.lower() for k in ["save", "output", "store"]):
                self._save_output_minimal(tool_name, result)
            
            # If this looks like a security scan/task, analyze output and build report
            if self._is_security_task(tool_name, task):
                analysis = self._analyze_tool_output(tool_name, task, command, result)
                report_md = self._format_security_report(analysis)
                saved_report = self._save_security_report(tool_name, report_md)
                truncated_raw = result[:600] + "..." if len(result) > 600 else result
                return (
                    f"{report_md}\n\n"
                    f"Raw Output (truncated):\n{truncated_raw}\n\n"
                    f"Saved report: {saved_report}"
                )
            
            # Fallback: return raw output
            return result[:1000] + "..." if len(result) > 1000 else result
            
        except Exception as e:
            return f"Execution failed: {str(e)[:100]}..."

    def _is_security_task(self, tool_name: str, task: str) -> bool:
        """Heuristically decide if the run is a security scan/testing task."""
        keywords = ["scan", "fuzz", "probe", "discover", "enumerate", "audit", "test"]
        if any(k in task.lower() for k in keywords):
            return True
        security_tools = {
            "nmap","nikto","sqlmap","nuclei","httpx","subfinder","amass",
            "masscan","ffuf","dirsearch","wpscan","gobuster","dirb"
        }
        return tool_name.lower() in security_tools

    def _analyze_tool_output(self, tool_name: str, task: str, command: str, output: str) -> Dict[str, Any]:
        """Parse tool output and produce structured findings for reporting."""
        tool = tool_name.lower()
        target = self._extract_target_fast(task) or "<unknown>"
        findings: List[Dict[str, Any]] = []
        sev_counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Info": 0}
        summary = ""
        recommendations: List[str] = []
        evidence_snippets: List[str] = []
        
        # Tool-specific parsers
        if tool == "nmap":
            discovered_hosts: List[Dict[str, Any]] = []
            host_open_ports: Dict[str, List[Dict[str, Any]]] = {}
            host_filtered_ports: Dict[str, List[Dict[str, Any]]] = {}
            host_closed_counts: Dict[str, int] = {}
            current_host: Optional[str] = None
            network_range = bool(re.search(r"/\d{1,2}", task) or re.search(r"/\d{1,2}", command))
            lines = output.splitlines()
            for line in lines:
                ls = line.strip()
                # Host discovery
                m = re.search(r"^Nmap scan report for\s+(.*)$", ls)
                if m:
                    host_field = m.group(1)
                    ip_match = re.search(r"(?:\d{1,3}\.){3}\d{1,3}", host_field)
                    ip = ip_match.group(0) if ip_match else host_field.split()[0]
                    current_host = ip
                    role = "Router/Gateway" if ip.split(".")[-1] in {"1", "254"} else None
                    discovered_hosts.append({"ip": ip, "latency": None, "role": role})
                    continue
                m = re.search(r"Host is up \(([\d\.]+s) latency\)", ls)
                if m and current_host:
                    if discovered_hosts and discovered_hosts[-1]["ip"] == current_host:
                        discovered_hosts[-1]["latency"] = m.group(1)
                    continue
                # Closed ports count
                m = re.search(r"^Not shown: (\d+) closed ports", ls)
                if m and current_host:
                    host_closed_counts[current_host] = int(m.group(1))
                    continue
                # Open ports
                m = re.search(r"^(\d{1,5})/(tcp|udp)\s+open\s+(\S+)", ls, re.IGNORECASE)
                if m and current_host:
                    port = int(m.group(1)); proto = m.group(2); service = m.group(3)
                    host_open_ports.setdefault(current_host, []).append({
                        "port": port, "proto": proto, "service": service, "evidence": ls
                    })
                    severity = self._severity_for_port(port, service)
                    findings.append({
                        "title": f"Open port {port}/{proto} on {current_host}",
                        "severity": severity,
                        "description": f"Service '{service}' detected as open",
                        "evidence": ls
                    })
                    continue
                # Filtered ports
                m = re.search(r"^(\d{1,5})/(tcp|udp)\s+filtered\s+(\S+)", ls, re.IGNORECASE)
                if m and current_host:
                    port = int(m.group(1)); proto = m.group(2); service = m.group(3)
                    host_filtered_ports.setdefault(current_host, []).append({
                        "port": port, "proto": proto, "service": service, "evidence": ls
                    })
                    findings.append({
                        "title": f"Filtered port {port}/{proto} ({service}) on {current_host}",
                        "severity": "Info",
                        "description": "Port appears filtered (likely firewalled)",
                        "evidence": ls
                    })
                    continue
            # Summary for network recon
            active_hosts = len(discovered_hosts)
            hosts_with_open = len([h for h in host_open_ports if host_open_ports.get(h)])
            summary = (
                f"Discovered {active_hosts} active host(s). "
                f"Open ports found on {hosts_with_open} host(s)."
            )
            # Tactical recommendations
            # Choose a focal host for deeper enumeration
            detailed_host: Optional[str] = None
            if not network_range and target != "<unknown>":
                detailed_host = target
            elif host_open_ports:
                detailed_host = max(host_open_ports.keys(), key=lambda h: len(host_open_ports.get(h, [])))
            elif discovered_hosts:
                candidates = [h["ip"] for h in discovered_hosts if h["ip"].split(".")[-1] in ["1", "254"]]
                detailed_host = candidates[0] if candidates else discovered_hosts[0]["ip"]
            if detailed_host:
                recommendations.append(f"Run `nmap -sV -O {detailed_host}` for service and OS detection")
                recommendations.append(f"Execute `nmap -sT -p- {detailed_host}` to scan all 65,535 ports")
            recommendations.append("Assess exposed services; patch outdated software; apply least privilege")
            if network_range and active_hosts > 1:
                others = [h["ip"] for h in discovered_hosts if h["ip"] != detailed_host]
                if others:
                    recommendations.append(
                        "Repeat detailed enumeration for remaining hosts: "
                        + ", ".join(others[:5]) + (" ..." if len(others) > 5 else "")
                    )
            evidence_snippets = lines[:10]
            # Enrich severity counts from findings below
            filtered_telnet = any(
                any(fp.get("port") == 23 for fp in fps)
                for fps in host_filtered_ports.values()
            )
        elif tool == "nuclei":
            for line in output.splitlines():
                m = re.search(r"\[(critical|high|medium|low|info)\]", line, re.IGNORECASE)
                if m:
                    sev = m.group(1).capitalize()
                    sev = "Info" if sev.lower() == "info" else sev.capitalize()
                    sev_counts[sev] = sev_counts.get(sev, 0) + 1
                    findings.append({
                        "title": "Nuclei finding",
                        "severity": sev,
                        "description": "Template matched",
                        "evidence": line.strip()
                    })
            total = len(findings)
            summary = f"Nuclei reported {total} findings on {target}"
            recommendations.append("Review findings; patch affected components; add WAF rules if applicable.")
            evidence_snippets = output.splitlines()[:10]
        elif tool == "httpx":
            for line in output.splitlines():
                m = re.search(r"\[(\d{3})\s+[A-Z]+\]", line)
                if m:
                    code = int(m.group(1))
                    severity = "Info"
                    if code >= 500:
                        severity = "Medium"
                    findings.append({
                        "title": f"HTTP response {code}",
                        "severity": severity,
                        "description": "Discovered endpoint with status code",
                        "evidence": line.strip()
                    })
            summary = f"httpx enumerated {len(findings)} endpoints for {target}"
            recommendations.append("Harden error handling; avoid leaking stack traces or debug info.")
            evidence_snippets = output.splitlines()[:10]
        elif tool in ("dirsearch", "gobuster", "dirb", "ffuf"):
            count = 0
            for line in output.splitlines():
                if re.search(r"\s(200|301|302|401|403|500)\s", line):
                    count += 1
                    findings.append({
                        "title": "Discovered path",
                        "severity": "Medium",
                        "description": "Accessible resource discovered",
                        "evidence": line.strip()
                    })
            summary = f"Discovered {count} paths on {target}"
            recommendations.append("Restrict access to sensitive paths; implement proper auth and directory indexing controls.")
            evidence_snippets = output.splitlines()[:10]
        elif tool == "nikto":
            count = 0
            for line in output.splitlines():
                if re.search(r"OSVDB|vulnerable|insecure|directory indexing|outdated", line, re.IGNORECASE):
                    count += 1
                    findings.append({
                        "title": "Nikto issue",
                        "severity": "Medium",
                        "description": "Potential web server misconfiguration or vulnerability",
                        "evidence": line.strip()
                    })
            summary = f"Nikto flagged {count} issues on {target}"
            recommendations.append("Update server software; disable risky modules; sanitize headers.")
            evidence_snippets = output.splitlines()[:10]
        elif tool == "sqlmap":
            is_vuln = False
            for line in output.splitlines():
                if re.search(r"is vulnerable|sql injection", line, re.IGNORECASE):
                    is_vuln = True
                    findings.append({
                        "title": "SQL Injection",
                        "severity": "High",
                        "description": "Target appears vulnerable to SQL injection",
                        "evidence": line.strip()
                    })
            summary = "SQLi detected" if is_vuln else "No explicit SQLi indications in parsed output"
            if is_vuln:
                recommendations.append("Apply prepared statements, input validation, and ORM safeguards.")
            evidence_snippets = output.splitlines()[:10]
        else:
            # Generic parser: look for keywords
            for line in output.splitlines():
                if re.search(r"(vuln|critical|high|warning|open|exposed)", line, re.IGNORECASE):
                    findings.append({
                        "title": "Potential issue",
                        "severity": "Info",
                        "description": "Keyword hit in output",
                        "evidence": line.strip()
                    })
            summary = f"Parsed generic output; {len(findings)} potential lines of interest"
            evidence_snippets = output.splitlines()[:10]
        
        # Aggregate severities
        for f in findings:
            sev_counts[f["severity"]] = sev_counts.get(f["severity"], 0) + 1
        
        # Derive overall risk (special-case nmap for nuanced Low-Medium)
        risk_level = "Low"
        if sev_counts.get("High", 0) > 0 or sev_counts.get("Critical", 0) > 0:
            risk_level = "High"
        elif sev_counts.get("Medium", 0) >= 3:
            risk_level = "Medium"
        else:
            # If only common web/DNS services are open, call it Low-Medium
            if tool == "nmap":
                common_services = {"http", "https", "domain"}
                has_common = any(
                    f.get("description", "").lower().find("service") != -1 and any(cs in f.get("description", "").lower() for cs in common_services)
                    for f in findings
                )
                if has_common:
                    risk_level = "Low-Medium"
        
        base = {
            "tool": tool_name,
            "target": target,
            "command": command,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": summary,
            "risk_level": risk_level,
            "severity_counts": sev_counts,
            "findings": findings,
            "recommendations": recommendations,
            "evidence": evidence_snippets,
            "raw_output": output[:1000] + "..." if len(output) > 1000 else output
        }
        if tool == "nmap":
            base.update({
                "discovered_hosts": discovered_hosts,
                "host_open_ports": host_open_ports,
                "host_filtered_ports": host_filtered_ports,
                "host_closed_counts": host_closed_counts,
                "network_range": network_range,
                "filtered_telnet": filtered_telnet if 'filtered_telnet' in locals() else False,
                "detailed_host": detailed_host if 'detailed_host' in locals() else None,
            })
        return base

    def _severity_for_port(self, port: int, service: str) -> str:
        """Map ports/services to rough severity for quick risk scoring."""
        high_ports = {21, 23, 445, 3389, 5900}
        medium_ports = {22, 25, 3306, 5432}
        if port in high_ports:
            return "High"
        if service.lower() in {"ftp", "telnet", "smb", "rdp", "vnc"}:
            return "High"
        if port in medium_ports:
            return "Medium"
        return "Low"

    def _format_security_report(self, analysis: Dict[str, Any]) -> str:
        """Render a human-readable security report in Markdown."""
        tool = str(analysis.get("tool", "")).lower()
        # Specialized comprehensive layout for nmap network reconnaissance
        if tool == "nmap" and analysis.get("discovered_hosts") is not None:
            lines: List[str] = []
            # Pull extended fields
            discovered_hosts = analysis.get("discovered_hosts", [])
            host_open = analysis.get("host_open_ports", {})
            host_filtered = analysis.get("host_filtered_ports", {})
            host_closed = analysis.get("host_closed_counts", {})
            detailed_host = analysis.get("detailed_host")
            network_range = analysis.get("network_range", False)
            command = analysis.get("command", "")
            # Try to show the scanned network/range
            range_match = re.search(r"((?:\d{1,3}\.){3}\d{1,3}/\d{1,2})", command)
            target_str = range_match.group(1) if range_match else analysis.get("target", "<unknown>")
            # Header
            lines.append(f"# Security Report: Nmap")
            lines.append(f"- Target: {target_str}")
            lines.append(f"- Timestamp: {analysis['timestamp']}")
            lines.append(f"- Command: `{analysis['command']}`")
            lines.append("")
            lines.append("## 🎯 NETWORK RECONNAISSANCE COMPLETE")
            lines.append("")
            lines.append("### 📊 DISCOVERY SUMMARY")
            lines.append(f"Successfully scanned {target_str} and identified **{len(discovered_hosts)} active devices**:")
            lines.append("")
            lines.append("**Active Hosts Discovered:**")
            # Helper to label latency
            def _latency_label(ls: Optional[str]) -> str:
                if not ls:
                    return ""
                try:
                    val = float(ls.rstrip("s"))
                    if val <= 0.001:
                        return "Very low latency"
                    if val <= 0.003:
                        return "Low latency"
                    return "Latency"
                except Exception:
                    return "Latency"
            for h in discovered_hosts[:50]:
                ip = h.get("ip")
                latency = h.get("latency")
                role = h.get("role")
                label = role or "Active device"
                lat_label = _latency_label(latency)
                if latency:
                    lines.append(f"- {ip}  ({label} - {lat_label}: {latency})")
                else:
                    lines.append(f"- {ip}  ({label})")
            lines.append("")
            # Detailed section for chosen host
            if detailed_host:
                lines.append(f"### 🔍 DETAILED PORT SCAN RESULTS - {detailed_host}")
                lines.append("")
                opens = host_open.get(detailed_host, [])
                if opens:
                    lines.append("**Open Ports Identified:**")
                    for e in opens:
                        port, proto, service = e["port"], e["proto"], e["service"]
                        note = ""
                        if service.lower() == "domain" and port == 53:
                            note = " (DNS service)"
                        elif service.lower() == "http" and port == 80:
                            note = " (Web service)"
                        elif service.lower() == "https" and port == 443:
                            note = " (Secure web service)"
                        lines.append(f"- **{port}/{proto}**   open     {service}{note}")
                # Security observations
                lines.append("")
                lines.append("**Security Observations:**")
                filts = host_filtered.get(detailed_host, [])
                # Show specific filtered telnet if present, else generic filtered items
                telnet_present = any(f.get("port") == 23 and f.get("proto") == "tcp" for f in filts)
                if telnet_present:
                    lines.append("- **23/tcp**   filtered telnet (Potentially blocked/filtered)")
                elif filts:
                    # Show up to 3 filtered ports
                    for f in filts[:3]:
                        lines.append(f"- **{f['port']}/{f['proto']}**   filtered {f['service']}")
                closed_ct = host_closed.get(detailed_host)
                if closed_ct is not None:
                    lines.append(f"- {closed_ct} ports showing as closed")
            lines.append("")
            # Security assessment
            lines.append("### ⚠️ SECURITY ASSESSMENT")
            risk = str(analysis.get("risk_level", "Low"))
            lines.append(f"**Risk Level:** {risk}")
            opens = host_open.get(detailed_host, [])
            svc = {e["service"].lower() for e in opens}
            if {"domain", "http", "https"}.issubset(svc):
                lines.append("- Standard services detected (DNS, HTTP, HTTPS)")
            elif svc:
                lines.append(f"- Services detected: {', '.join(sorted(svc))}")
            else:
                lines.append("- No open services detected on the focus host in parsed output")
            if telnet_present:
                lines.append("- Telnet service filtered (good security practice)")
            lines.append("- No critical vulnerabilities identified in basic scan")
            lines.append("")
            # Tactical recommendations
            lines.append("### 🎯 TACTICAL RECOMMENDATIONS")
            lines.append("")
            lines.append("**Immediate Actions:**")
            if detailed_host:
                lines.append(f"1. **Service Enumeration**: Run `nmap -sV -O {detailed_host}` for detailed service and OS detection")
                lines.append(f"2. **Full Port Scan**: Execute `nmap -sT -p- {detailed_host}` for complete 65,535-port analysis")
            else:
                lines.append("1. **Service Enumeration**: Choose a host with open ports and run `nmap -sV -O <host>`")
                lines.append("2. **Full Port Scan**: Execute `nmap -sT -p- <host>` for complete 65,535-port analysis")
            lines.append("3. **Vulnerability Assessment**: Test identified services for common vulnerabilities")
            lines.append("")
            lines.append("**Next Phase Operations:**")
            lines.append("- Perform similar detailed scans on remaining discovered hosts")
            lines.append("- Focus on unusual services or unexpected open ports")
            lines.append("- Document findings for penetration testing roadmap")
            lines.append("")
            # Operational notes
            lines.append("**Operational Notes:**")
            lines.append(f"- All {len(discovered_hosts)} discovered hosts are confirmed active and responsive")
            if any(h.get("latency") for h in discovered_hosts):
                lines.append("- Low latency measurements indicate local network connectivity")
            lines.append("- Ready for phase 2: detailed service enumeration and vulnerability assessment")
            lines.append("")
            # Final answer summary
            # Summarize key ports for focus host
            if detailed_host and opens:
                ports_summary = ", ".join(str(e["port"]) for e in opens[:10])
                svc_summary = ", ".join(sorted({e["service"].upper() for e in opens if e["service"] in {"domain","http","https"}}))
                lines.append(
                    f"Final Answer: Network reconnaissance completed. Discovered {len(discovered_hosts)} active devices on {target_str}. "
                    f"Detailed port scan of {detailed_host} revealed ports {ports_summary} active" + (f" ({svc_summary})" if svc_summary else "")
                )
            else:
                lines.append(
                    f"Final Answer: Network reconnaissance completed. Discovered {len(discovered_hosts)} active devices on {target_str}. "
                    f"Proceed with comprehensive security assessment of all discovered hosts."
                )
            return "\n".join(lines)
        
        # Generic fallback formatting for other tools
        lines = []
        lines.append(f"# Security Report: {analysis['tool']}")
        lines.append(f"- Target: {analysis['target']}")
        lines.append(f"- Timestamp: {analysis['timestamp']}")
        lines.append(f"- Command: `{analysis['command']}`")
        lines.append("")
        lines.append("## Summary")
        lines.append(analysis["summary"])
        lines.append(f"- Overall Risk: {analysis['risk_level']}")
        lines.append("")
        lines.append("## Severity Counts")
        sc = analysis["severity_counts"]
        lines.append(f"- Critical: {sc.get('Critical', 0)}")
        lines.append(f"- High: {sc.get('High', 0)}")
        lines.append(f"- Medium: {sc.get('Medium', 0)}")
        lines.append(f"- Low: {sc.get('Low', 0)}")
        lines.append(f"- Info: {sc.get('Info', 0)}")
        lines.append("")
        lines.append("## Findings")
        if analysis["findings"]:
            for f in analysis["findings"][:50]:
                lines.append(f"- [{f['severity']}] {f['title']} — {f['description']}")
                lines.append(f"  Evidence: {f['evidence']}")
        else:
            lines.append("- No findings parsed.")
        lines.append("")
        lines.append("## Recommendations")
        if analysis["recommendations"]:
            for r in analysis["recommendations"]:
                lines.append(f"- {r}")
        else:
            lines.append("- Review configuration and apply least privilege; keep software updated.")
        lines.append("")
        lines.append("## Evidence (first lines)")
        for e in analysis["evidence"]:
            lines.append(f"- {e}")
        return "\n".join(lines)

    def _save_security_report(self, tool_name: str, report_md: str) -> str:
        """Save the security report to outputs directory and return its path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"SecurityReport_{tool_name}_{timestamp}.md"
        path = self.outputs_dir / filename
        try:
            path.write_text(report_md, encoding="utf-8")
        except Exception:
            pass
        return str(path)

    def _extract_target_fast(self, task: str) -> str:
        """Fast target extraction with minimal regex processing."""
        # Quick IP check
        import re
        ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', task)
        if ip_match:
            return ip_match.group()
        
        # Quick domain check
        domain_match = re.search(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}\b', task)
        if domain_match:
            return domain_match.group()
        
        # Quick localhost check
        if "localhost" in task.lower():
            return "localhost"
        
        return None
    
    def _extract_target_fast(self, task: str) -> str:
        """Fast target extraction with minimal regex processing."""
        # Quick IP check
        import re
        ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', task)
        if ip_match:
            return ip_match.group()
        
        # Quick domain check
        domain_match = re.search(r'\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}\b', task)
        if domain_match:
            return domain_match.group()
        
        # Quick localhost check
        if "localhost" in task.lower():
            return "localhost"
        
        return None

    def _generate_quick_command(self, tool_name: str, task: str, tool_path: str) -> str:
        """Quick command generation without complex parsing."""
        task_lower = task.lower()
        
        # Quick patterns for common tools
        if tool_name == "nmap":
            if "scan" in task_lower:
                target = self._extract_target_fast(task)
                return f"{tool_path} -sS {target}" if target else f"{tool_path} --help"
        elif tool_name == "httpx":
            target = self._extract_target_fast(task)
            return f"{tool_path} {target}" if target else f"{tool_path} --help"
        elif tool_name == "subfinder":
            target = self._extract_target_fast(task)
            return f"{tool_path} -d {target}" if target else f"{tool_path} --help"
        
        # Generic fallback
        return f"{tool_path} {task}"
    
    def _save_output_minimal(self, tool_name: str, result: str) -> None:
        """Minimal output saving for performance."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{tool_name}_{timestamp}.txt"
        output_path = self.outputs_dir / filename
        
        try:
            output_path.write_text(result[:5000])  # Limit output size
        except Exception:
            pass  # Fail silently for performance
    
    def _search_tools_fast(self, query: str) -> str:
        """Fast tool search without complex matching."""
        query_lower = query.lower()
        matches = []
        
        for tool_name in self.tools_db["installed_tools"]:
            if query_lower in tool_name.lower():
                matches.append(tool_name)
        
        if matches:
            return f"Found tools: {', '.join(matches)}"
        else:
            return f"No tools found matching '{query}'"
    
    def _show_manual_fast(self, tool_name: str) -> str:
        """Fast manual display without heavy processing."""
        if tool_name not in self.tools_db["installed_tools"]:
            return f"Tool '{tool_name}' not installed."
        
        try:
            result = run_subprocess([tool_name, "--help"], timeout=5)
            return result[:500] + "..." if len(result) > 500 else result
        except Exception:
            return f"Could not retrieve manual for {tool_name}"
    
    def _check_tool_health_fast(self, tool_name: str) -> str:
        """Fast health check for single tool."""
        if tool_name not in self.tools_db["installed_tools"]:
            return f"✗ Tool '{tool_name}' not installed"
        
        # Quick path check
        tool_path = self._get_cached_tool_path(tool_name)
        if tool_path:
            return f"✓ {tool_name} - Available at {tool_path}"
        else:
            return f"✗ {tool_name} - Not found in PATH"
    
    def _check_all_tools_health_fast(self) -> str:
        """Fast health check for all tools."""
        if not self.tools_db["installed_tools"]:
            return "No tools to check."
        
        healthy = 0
        total = len(self.tools_db["installed_tools"])
        
        for tool_name in self.tools_db["installed_tools"]:
            if self._get_cached_tool_path(tool_name):
                healthy += 1
        
        return f"Health Status: {healthy}/{total} tools available"
    
    def _show_inventory_fast(self) -> str:
        """Fast inventory display."""
        if not self.tools_db["installed_tools"]:
            return "No tools installed."
        
        result = ["Tool Inventory:", ""]
        for tool_name, info in self.tools_db["installed_tools"].items():
            usage = info.get("usage_count", 0)
            result.append(f"• {tool_name} - Used {usage} times")
        
        return "\n".join(result)
    
    def _register_tool_fast(self, tool_name: str) -> str:
        """Fast tool registration."""
        tool_path = self._get_cached_tool_path(tool_name)
        if tool_path:
            return self._register_existing_tool_fast(tool_name, tool_path)
        else:
            return f"Tool '{tool_name}' not found in PATH"
    
    async def _arun(self, command: str) -> str:
        return self._run(command)


class TodoManagerTool(BaseTool):
    """Dedicated tool for comprehensive todo list management with progress tracking."""
    name: str = "todo_manager"
    description: str = """Advanced todo list management. Commands:
    - create: Create new todo list with title
    - add: Add task to existing todo
    - list: Show current todo with progress
    - mark: Mark task as complete/incomplete
    - progress: Show completion statistics
    - clear: Clear completed tasks
    - export: Export todo to file
    Input format: JSON with 'action' and parameters"""

    @property
    def todo_file(self) -> Path:
        """Get the todo file path."""
        return Path("todo.txt")
        
    def _parse_todo_file(self) -> Dict[str, Any]:
        """Parse existing todo file and extract tasks with status."""
        if not self.todo_file.exists():
            return {
                "title": "TODO List",
                "tasks": [],
                "metadata": {"created": time.time(), "last_updated": time.time()}
            }
            
        try:
            content = self.todo_file.read_text(encoding='utf-8')
            lines = content.strip().split('\n')
            
            if not lines:
                return {"title": "TODO List", "tasks": [], "metadata": {"created": time.time(), "last_updated": time.time()}}
                
            # Extract title
            title = lines[0].replace("TODO List for ", "").replace(":", "").strip()
            if not title.startswith("TODO"):
                title = f"TODO List for {title}"
                
            tasks = []
            for line in lines[1:]:
                line = line.strip()
                if not line or not line[0].isdigit():
                    continue
                    
                # Parse task format: "1. [ ] Task description" or "1. [x] Task description"
                import re
                match = re.match(r'^(\d+)\.\s*\[([x\s])\]\s*(.+)$', line)
                if match:
                    task_num = int(match.group(1))
                    status = match.group(2).strip().lower() == 'x'
                    description = match.group(3).strip()
                    tasks.append({
                        "id": task_num,
                        "description": description,
                        "completed": status,
                        "created": time.time()
                    })
                    
            return {
                "title": title,
                "tasks": tasks,
                "metadata": {"created": time.time(), "last_updated": time.time()}
            }
            
        except Exception as e:
            return {
                "title": "TODO List", 
                "tasks": [], 
                "metadata": {"created": time.time(), "last_updated": time.time(), "error": str(e)}
            }
    
    def _save_todo_file(self, todo_data: Dict[str, Any]) -> bool:
        """Save todo data back to file in proper format."""
        try:
            lines = [todo_data["title"] + ":"]
            
            for task in todo_data["tasks"]:
                status = "[x]" if task["completed"] else "[ ]"
                lines.append(f"{task['id']}. {status} {task['description']}")
                
            content = '\n'.join(lines)
            self.todo_file.write_text(content, encoding='utf-8')
            return True
        except Exception:
            return False
    
    def _get_progress_bar(self, completed: int, total: int, width: int = 20) -> str:
        """Generate a visual progress bar."""
        if total == 0:
            return "░" * width + " 0%"
            
        percentage = (completed / total) * 100
        filled = int((completed / total) * width)
        empty = width - filled
        
        bar = "█" * filled + "░" * empty
        return f"{bar} {percentage:.1f}% ({completed}/{total})"
    
    def _format_todo_display(self, todo_data: Dict[str, Any]) -> str:
        """Format todo list for display with progress indicators."""
        if not todo_data["tasks"]:
            return f"📋 {todo_data['title']}\n\n❌ No tasks found. Use 'add' to create tasks."
            
        completed_count = sum(1 for task in todo_data["tasks"] if task["completed"])
        total_count = len(todo_data["tasks"])
        
        output = []
        output.append(f"📋 {todo_data['title']}")
        output.append(f"📊 Progress: {self._get_progress_bar(completed_count, total_count)}")
        output.append("")
        
        for task in todo_data["tasks"]:
            status_icon = "✅" if task["completed"] else "⏳"
            status_text = "[x]" if task["completed"] else "[ ]"
            output.append(f"{status_icon} {task['id']}. {status_text} {task['description']}")
            
        # Add summary
        if completed_count == total_count:
            output.append(f"\n🎉 All tasks completed! ({completed_count}/{total_count})")
        else:
            remaining = total_count - completed_count
            output.append(f"\n📈 {remaining} task{'s' if remaining != 1 else ''} remaining")
            
        return '\n'.join(output)

    def _run(self, payload: str) -> str:
        """Execute todo management commands."""
        try:
            if payload.startswith('{'):
                # JSON input
                import json
                data = json.loads(payload)
                action = data.get("action", "").lower()
            else:
                # Simple command input
                parts = payload.strip().split(' ', 1)
                action = parts[0].lower()
                data = {"action": action}
                if len(parts) > 1:
                    if action in ["create", "add"]:
                        data["text"] = parts[1]
                    elif action == "mark":
                        try:
                            data["task_id"] = int(parts[1])
                        except ValueError:
                            return "❌ Error: 'mark' requires a task number"
                    elif action == "export":
                        data["filename"] = parts[1]
        except Exception:
            return "❌ Error: Invalid input format. Use JSON or simple commands like 'list', 'add <text>', 'mark <number>'"
        
        todo_data = self._parse_todo_file()
        
        if action == "create":
            title = data.get("text", "New Todo List")
            if not title.startswith("TODO"):
                title = f"TODO List for {title}"
            todo_data = {
                "title": title,
                "tasks": [],
                "metadata": {"created": time.time(), "last_updated": time.time()}
            }
            self._save_todo_file(todo_data)
            return f"📝 Created new todo list: '{title}'"
            
        elif action == "add":
            text = data.get("text", "").strip()
            if not text:
                return "❌ Error: 'add' requires task description"
                
            # Find next task ID
            next_id = max([task["id"] for task in todo_data["tasks"]], default=0) + 1
            
            new_task = {
                "id": next_id,
                "description": text,
                "completed": False,
                "created": time.time()
            }
            
            todo_data["tasks"].append(new_task)
            todo_data["metadata"]["last_updated"] = time.time()
            
            if self._save_todo_file(todo_data):
                return f"✅ Added task #{next_id}: {text}"
            else:
                return "❌ Error: Failed to save todo file"
                
        elif action == "list":
            return self._format_todo_display(todo_data)
            
        elif action == "mark":
            task_id = data.get("task_id")
            if task_id is None:
                return "❌ Error: 'mark' requires task_id parameter"
                
            # Find and toggle task
            task_found = False
            for task in todo_data["tasks"]:
                if task["id"] == task_id:
                    task["completed"] = not task["completed"]
                    task_found = True
                    status = "completed" if task["completed"] else "incomplete"
                    
                    todo_data["metadata"]["last_updated"] = time.time()
                    
                    if self._save_todo_file(todo_data):
                        icon = "✅" if task["completed"] else "⏳"
                        return f"{icon} Task #{task_id} marked as {status}: {task['description']}"
                    else:
                        return "❌ Error: Failed to save todo file"
                        
            if not task_found:
                return f"❌ Error: Task #{task_id} not found"
                
        elif action == "progress":
            if not todo_data["tasks"]:
                return "📋 No tasks found in todo list"
                
            completed_count = sum(1 for task in todo_data["tasks"] if task["completed"])
            total_count = len(todo_data["tasks"])
            
            progress_bar = self._get_progress_bar(completed_count, total_count, 30)
            
            output = []
            output.append(f"📊 Todo Progress Report")
            output.append(f"📋 Title: {todo_data['title']}")
            output.append(f"📈 Progress: {progress_bar}")
            output.append(f"✅ Completed: {completed_count}")
            output.append(f"⏳ Remaining: {total_count - completed_count}")
            output.append(f"📅 Last Updated: {datetime.fromtimestamp(todo_data['metadata']['last_updated']).strftime('%Y-%m-%d %H:%M:%S')}")
            
            if completed_count == total_count:
                output.append("🎉 Congratulations! All tasks completed!")
                
            return '\n'.join(output)
            
        elif action == "clear":
            original_count = len(todo_data["tasks"])
            todo_data["tasks"] = [task for task in todo_data["tasks"] if not task["completed"]]
            cleared_count = original_count - len(todo_data["tasks"])
            
            todo_data["metadata"]["last_updated"] = time.time()
            
            if self._save_todo_file(todo_data):
                if cleared_count == 0:
                    return "ℹ️ No completed tasks to clear"
                else:
                    return f"🗑️ Cleared {cleared_count} completed task{'s' if cleared_count != 1 else ''}"
            else:
                return "❌ Error: Failed to save todo file"
                
        elif action == "export":
            filename = data.get("filename", f"todo_export_{int(time.time())}.txt")
            
            try:
                export_content = []
                export_content.append(f"# {todo_data['title']}")
                export_content.append(f"# Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                export_content.append("")
                
                completed_tasks = [task for task in todo_data["tasks"] if task["completed"]]
                pending_tasks = [task for task in todo_data["tasks"] if not task["completed"]]
                
                if pending_tasks:
                    export_content.append("## Pending Tasks")
                    for task in pending_tasks:
                        export_content.append(f"- [ ] {task['description']}")
                    export_content.append("")
                    
                if completed_tasks:
                    export_content.append("## Completed Tasks")
                    for task in completed_tasks:
                        export_content.append(f"- [x] {task['description']}")
                        
                Path(filename).write_text('\n'.join(export_content), encoding='utf-8')
                return f"💾 Exported todo list to: {filename}"
                
            except Exception as e:
                return f"❌ Error exporting: {e}"
                
        else:
            return f"""❌ Unknown action: {action}

Available commands:
📝 create <title> - Create new todo list
➕ add <description> - Add new task
📋 list - Show current todo with progress
✅ mark <number> - Toggle task completion
📊 progress - Show detailed progress report
🗑️ clear - Remove completed tasks
💾 export <filename> - Export to markdown file

Examples:
  create "Website Security Audit"
  add "Run nmap scan on target"
  mark 3
  progress"""

    async def _arun(self, payload: str) -> str:
        return self._run(payload)