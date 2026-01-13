"""
Utility functions for FlawHunt CLI.
Contains platform detection and other helper functions.
"""
import platform
import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, Any
from shutil import which

def shutil_which(bin_name: str) -> Optional[str]:
    """Cross-platform which command."""
    return which(bin_name)

def get_shell_executable(system: str) -> Optional[str]:
    """Get the appropriate shell executable for the platform."""
    if system == "windows":
        # Try PowerShell first, then cmd
        for shell in ["powershell.exe", "cmd.exe"]:
            if shutil_which(shell):
                return shell
        return "cmd.exe"  # fallback
    else:
        # Unix-like systems (Linux, macOS)
        for shell in ["/bin/bash", "/bin/sh", "/bin/zsh"]:
            if Path(shell).exists():
                return shell
        return "/bin/sh"  # fallback

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

def get_platform_info() -> Dict[str, Any]:
    """Get platform-specific information."""
    system = platform.system().lower()
    return {
        "system": system,
        "is_windows": system == "windows",
        "is_linux": system == "linux",
        "is_darwin": system == "darwin",  # macOS
        "shell_executable": get_shell_executable(system),
        "path_separator": "\\" if system == "windows" else "/",
        "package_manager": get_package_manager(system),
    }

def run_subprocess(cmd: str, timeout: int = 60) -> str:
    """Run a shell command safely in a subprocess, capturing output."""
    try:
        platform_info = get_platform_info()
        # Detect if this command is executing a file/script and notify
        try:
            from .notifications import notify
            import shlex
            import os
            parts = shlex.split(cmd) if not platform_info["is_windows"] else cmd.split()
            head = parts[0] if parts else ""
            executed_file = None

            # Direct execution of a file (e.g., ./script.sh or /path/to/bin)
            if head and os.path.isfile(head):
                executed_file = head
            # Interpreter patterns (python, bash, sh, zsh) with script path next
            elif len(parts) >= 2:
                interpreters = ("python", "python3", "bash", "sh", "zsh")
                if any(head.endswith(interp) or head == interp for interp in interpreters):
                    candidate = parts[1]
                    if os.path.isfile(candidate):
                        executed_file = candidate

            if executed_file:
                notify("Executing File", f"{os.path.basename(executed_file)}")
        except Exception:
            # Non-blocking best-effort notification
            pass
        
        # Platform-specific shell configuration
        if platform_info["is_windows"]:
            # On Windows, use the default shell (cmd or PowerShell)
            p = subprocess.run(
                cmd,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
        else:
            # On Unix-like systems, explicitly use bash or sh
            p = subprocess.run(
                cmd,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                executable=platform_info["shell_executable"],
                encoding='utf-8',
                errors='replace'
            )
        output = p.stdout.strip() if p.stdout else ""
        return output if output else "(Command execution successful, but returned no output)"
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Error running command: {e}"

def extract_tool_info(tool_name: str) -> Dict[str, str]:
    """Extract comprehensive information about a tool."""
    info = {"name": tool_name, "help": "", "man": "", "version": "", "location": ""}
    
    # Get tool location
    if platform.system().lower() == "windows":
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
    if platform.system().lower() != "windows":
        man_text = run_subprocess(f"MANWIDTH=90 man {tool_name} | col -b | head -n 200", timeout=20)
        if man_text and "No manual entry" not in man_text:
            info["man"] = man_text[:3000]
    
    return info