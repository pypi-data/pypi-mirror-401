#!/usr/bin/env python3
"""
FlawHunt CLI - Main entry point.

Natural language to shell with explanations & confirmations.
Gemini + LangChain ReAct agent with custom tools.

Usage:
    python -m ai_terminal_pkg.main
    
Or after installation:
    ai-terminal
"""
import os
import sys
import time
from datetime import datetime

# Suppress tokenizer parallelism warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from pathlib import Path

try:
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
    from prompt_toolkit.completion import PathCompleter, WordCompleter, Completer, Completion
    from prompt_toolkit.completion.base import CompleteEvent
    from prompt_toolkit.document import Document
    from prompt_toolkit.key_binding import KeyBindings
except ImportError:
    PromptSession = None
    PathCompleter = None
    WordCompleter = None
    Completer = None
    Completion = None
    CompleteEvent = None
    Document = None
    KeyBindings = None

from ai_terminal import (
    LLM, AgentHarness, VectorStore, ConversationHistoryManager,
    load_state, save_state, get_platform_info,
    run_subprocess, looks_dangerous
)
from ai_terminal.conversation_history import ConversationSession
from ai_terminal.text_formatter import clean_ai_response
from ai_terminal.file_monitor import start_file_monitor

# Import theming and configuration modules
from ai_terminal.themes import ThemeManager
from ai_terminal.config import ConfigManager, get_config
from ai_terminal.animations import AnimationEngine
from ai_terminal.progress import ProgressBarManager

console = Console()

def handle_backup_command(conversation_history, parts):
    """Shared backup command handler for all modes"""
    # Check if user is a guest
    from ai_terminal.license import LicenseManager
    license_manager = LicenseManager()
    
    if license_manager.is_guest_user():
        console.print("[yellow]⚠️  Backup feature is not available for guest users.[/yellow]")
        console.print("[dim]Please purchase a license key to enable backup features.[/dim]")
        return
    
    if len(parts) == 1:
        # Perform backup
        console.print("[yellow]Creating chat backup...[/yellow]")
        
        try:
            # Get license and device information
            license_key = license_manager.load_license_key()
            device_info = license_manager.load_device_info()
            
            if not license_key or not device_info:
                console.print("[red]License information not found. Please ensure you're properly licensed.[/red]")
                return
            
            mac_address = device_info.get("mac_address")
            device_name = device_info.get("device_name")
            
            # Get conversation history
            all_conversations = conversation_history.get_all_conversations()
            sessions = conversation_history.get_all_sessions()
            
            # Prepare backup data
            backup_data = {
                "conversations": all_conversations,
                "sessions": sessions,
                "backup_timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
            
            # Calculate backup size and conversation count
            import json
            backup_json = json.dumps(backup_data)
            backup_size = len(backup_json.encode('utf-8'))
            conversation_count = len(all_conversations)
            
            # Prepare webhook payload
            webhook_payload = {
                "license_key": license_key,
                "device_name": device_name,
                "mac_address": mac_address,
                "chat_data": backup_data,
                "backup_size": backup_size,
                "conversation_count": conversation_count,
                "metadata": {
                    "cli_version": "1.0.0",
                    "platform": get_platform_info()['system'],
                    "backup_type": "manual"
                }
            }
            
            # Send to webhook
            import requests
            from ai_terminal.config import get_config
            
            # Get webhook URL from config
            config = get_config()
            webhook_url = config.backup.webhook_url
            
            headers = {
                "Content-Type": "application/json"
            }
            
            console.print("[yellow]Sending backup to server...[/yellow]")
            response = requests.post(
                webhook_url,
                json=webhook_payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                console.print(f"[green]✓ Backup completed successfully![/green]")
                console.print(f"[cyan]Backup ID: {result.get('backup_id', 'N/A')}[/cyan]")
                console.print(f"[cyan]Conversations backed up: {conversation_count}[/cyan]")
                console.print(f"[cyan]Backup size: {backup_size:,} bytes[/cyan]")
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                console.print(f"[red]✗ Backup failed: {error_data.get('error', 'Unknown error')}[/red]")
                
        except requests.exceptions.Timeout:
            console.print("[red]✗ Backup failed: Request timed out. Please check your internet connection.[/red]")
        except requests.exceptions.ConnectionError:
            console.print("[red]✗ Backup failed: Cannot connect to backup server. Please check your internet connection.[/red]")
        except Exception as e:
            console.print(f"[red]✗ Backup failed: {str(e)}[/red]")
            
    elif len(parts) > 1 and parts[1] == "help":
        console.print("[yellow]Backup commands:[/yellow]")
        console.print("  :backup - Create and upload chat backup")
        console.print("  :backup help - Show this help")
    else:
        console.print("[red]Unknown backup command. Use ':backup help' for available options.[/red]")

def handle_import_command(conversation_history, parts):
    """Shared import command handler for all modes"""
    # Check if user is a guest
    from ai_terminal.license import LicenseManager
    license_manager = LicenseManager()
    
    if license_manager.is_guest_user():
        console.print("[yellow]⚠️  Import feature is not available for guest users.[/yellow]")
        console.print("[dim]Please purchase a license key to enable import features.[/dim]")
        return
    
    if len(parts) == 1:
        # List available backups
        console.print("[yellow]Fetching available backups...[/yellow]")
        
        try:
            # Get license information
            license_key = license_manager.load_license_key()
            
            if not license_key:
                console.print("[red]License information not found. Please ensure you're properly licensed.[/red]")
                return
            
            # Send request to list backups
            import requests
            from ai_terminal.config import get_config
            
            config = get_config()
            webhook_url = config.backup.import_list_webhook_url
            
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "license_key": license_key
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                backups = result.get('backups', [])
                
                if not backups:
                    console.print("[yellow]No backups found for your user account.[/yellow]")
                    return
                
                console.print(f"[green]✓ Found {len(backups)} backup(s):[/green]")
                console.print()
                
                # Create a table to display backups
                from rich.table import Table
                table = Table(title="Available Backups", box=box.ROUNDED)
                table.add_column("Device Name", style="cyan", no_wrap=True)
                table.add_column("Backup Date", style="green")
                table.add_column("Conversations", style="yellow", justify="right")
                table.add_column("Size", style="magenta", justify="right")
                
                for backup in backups:
                    # Format backup size
                    size_bytes = backup.get('backup_size', 0)
                    if size_bytes > 1024 * 1024:
                        size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
                    elif size_bytes > 1024:
                        size_str = f"{size_bytes / 1024:.1f} KB"
                    else:
                        size_str = f"{size_bytes} B"
                    
                    # Format date
                    backup_date = backup.get('backup_timestamp', 'Unknown')
                    if backup_date != 'Unknown':
                        try:
                            from datetime import datetime
                            dt = datetime.fromisoformat(backup_date.replace('Z', '+00:00'))
                            backup_date = dt.strftime('%Y-%m-%d %H:%M')
                        except:
                            pass
                    
                    table.add_row(
                        backup.get('device_name', 'Unknown'),
                        backup_date,
                        str(backup.get('conversation_count', 0)),
                        size_str
                    )
                
                console.print(table)
                console.print()
                console.print("[dim]Use ':import <device_name>' to import a specific backup[/dim]")
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                console.print(f"[red]✗ Failed to fetch backups: {error_data.get('error', 'Unknown error')}[/red]")
                
        except requests.exceptions.Timeout:
            console.print("[red]✗ Request timed out. Please check your internet connection.[/red]")
        except requests.exceptions.ConnectionError:
            console.print("[red]✗ Cannot connect to import server. Please check your internet connection.[/red]")
        except Exception as e:
            console.print(f"[red]✗ Failed to fetch backups: {str(e)}[/red]")
            
    elif len(parts) >= 2:
        # Check if it's a help command
        if parts[1] == "help":
            console.print("[yellow]Import commands:[/yellow]")
            console.print("  :import - List available backups for your user")
            console.print("  :import <device_name> - Import backup from specific device")
            console.print("  :import help - Show this help")
            return
            
        # Import specific backup - join all parts after the first one to handle device names with spaces
        device_name = " ".join(parts[1:])
        console.print(f"[yellow]Importing backup from device: {device_name}...[/yellow]")
        
        try:
            # Get license information
            from ai_terminal.license import LicenseManager
            license_manager = LicenseManager()
            
            license_key = license_manager.load_license_key()
            
            if not license_key:
                console.print("[red]License information not found. Please ensure you're properly licensed.[/red]")
                return
            
            # Send request to import backup
            import requests
            from ai_terminal.config import get_config
            
            config = get_config()
            webhook_url = config.backup.import_webhook_url
            
            headers = {
                "Content-Type": "application/json"
            }
            
            payload = {
                "license_key": license_key,
                "device_name": device_name
            }
            
            response = requests.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                backup_data = result.get('chat_data')
                
                if not backup_data:
                    console.print("[red]✗ No backup data received from server.[/red]")
                    console.print("[yellow]Note: The server may still be processing your request. Please try again in a few moments.[/yellow]")
                    return
                
                # Import the backup data
                console.print("[yellow]Importing conversations and sessions...[/yellow]")
                
                # Clear existing data
                conversation_history.clear_history()
                
                # Import conversations
                conversations = backup_data.get('conversations', [])
                if not conversations:
                    # If no conversations array, check if there are any conversation-like data
                    console.print("[yellow]No conversations found in backup data.[/yellow]")
                
                for conv in conversations:
                    conversation_history.add_conversation(
                        user_input=conv.get('user_input', ''),
                        ai_response=conv.get('ai_response', ''),
                        metadata=conv.get('metadata', {})
                    )
                
                # Import sessions - handle sessions as dictionary
                sessions_data = backup_data.get('sessions', {})
                session_count = 0
                if isinstance(sessions_data, dict):
                    for session_id, session_info in sessions_data.items():
                        # Create session using the ConversationHistoryManager
                        session = ConversationSession(
                            id=session_info.get('id', session_id),
                            name=session_info.get('name', f'Imported Session {session_id[:8]}'),
                            created_at=session_info.get('created_at', time.time()),
                            last_activity=session_info.get('last_activity', time.time()),
                            metadata=session_info.get('metadata', {})
                        )
                        conversation_history.sessions[session_id] = session
                        session_count += 1
                elif isinstance(sessions_data, list):
                    session_count = len(sessions_data)
                
                # Save the imported sessions
                conversation_history.save_sessions()
                
                console.print(f"[green]✓ Import completed successfully![/green]")
                console.print(f"[cyan]Imported {len(conversations)} conversations[/cyan]")
                console.print(f"[cyan]Imported {session_count} sessions[/cyan]")
                console.print(f"[cyan]Backup date: {backup_data.get('backup_timestamp', 'Unknown')}[/cyan]")
                console.print(f"[cyan]Backup version: {backup_data.get('version', 'Unknown')}[/cyan]")
                
            else:
                error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                console.print(f"[red]✗ Import failed: {error_data.get('error', 'Unknown error')}[/red]")
                
        except requests.exceptions.Timeout:
            console.print("[red]✗ Import failed: Request timed out. Please check your internet connection.[/red]")
        except requests.exceptions.ConnectionError:
            console.print("[red]✗ Import failed: Cannot connect to import server. Please check your internet connection.[/red]")
        except Exception as e:
            console.print(f"[red]✗ Import failed: {str(e)}[/red]")
            
    else:
        console.print("[red]Unknown import command. Use ':import help' for available options.[/red]")

def get_themed_input(prompt_text: str, mode: str = "default") -> str:
    """Get user input with proper Rich markup rendering."""
    # Render the themed prompt with Rich
    console.print(prompt_text, end=" ")
    
    try:
        if PromptSession:
            # Use prompt_toolkit for better input experience
            session = PromptSession(
                history=FileHistory(HISTORY_FILE),
                auto_suggest=AutoSuggestFromHistory(),
                completer=None,
                complete_while_typing=True
            )
            user_input = session.prompt("")
        else:
            user_input = input("")
        
        return user_input
    except (KeyboardInterrupt, EOFError):
        return ""

import threading
from rich.live import Live

def show_loading_animation_during_response(message: str = "AI is thinking"):
    """Show loading animation during AI response generation."""
    return animation_engine.cyber_loading_bar(message, duration=0.5)

def invoke_llm_with_animation(llm, prompt, message="🤖 SAGE is thinking"):
    """Invoke LLM with subtle thinking animation."""
    response = None
    animation_done = threading.Event()
    
    def run_animation():
        animation_engine.simple_thinking_animation(message, animation_done)
    
    def run_llm():
        nonlocal response
        response = llm.invoke(prompt)
        # Signal animation to stop
        animation_done.set()
    
    # Start animation in background
    animation_thread = threading.Thread(target=run_animation)
    animation_thread.daemon = True
    animation_thread.start()
    
    # Run LLM
    llm_thread = threading.Thread(target=run_llm)
    llm_thread.start()
    llm_thread.join()
    
    # Wait for animation to finish clearing
    animation_thread.join(timeout=0.5)
    
    return response

# Initialize theme manager and config
theme_manager = ThemeManager()
config_manager = ConfigManager()
animation_engine = AnimationEngine(theme_manager=theme_manager)
progress_manager = ProgressBarManager(theme_manager)

if Completer:
    class FlawHuntCLICompleter(Completer):
        """Custom completer for FlawHunt CLI with support for commands, paths, and meta commands."""
        
        def __init__(self):
            # Meta commands
            self.meta_commands = [
                ':help', ':safe', ':verbose', ':model', ':provider', ':history', 
                ':session', ':platform', ':stats', ':packages', ':learn', ':clear', ':quit', ':exit',
                ':todo', ':todo-list', ':todo-progress', ':todo-add', ':todo-mark', ':todo-clear'
            ]
            
            # Shell commands that get special handling
            self.shell_commands = [
                'cd', 'ls', 'pwd', 'mkdir', 'rmdir', 'cp', 'mv', 'rm', 'cat', 'grep',
                'find', 'chmod', 'chown', 'ps', 'kill', 'top', 'df', 'du', 'free',
                'git', 'docker', 'npm', 'pip', 'python', 'node', 'curl', 'wget'
            ]
            
            # Natural language starters
            self.nl_starters = [
                'list', 'show', 'find', 'search', 'create', 'generate', 'install',
                'setup', 'configure', 'build', 'run', 'execute', 'explain', 'help',
                'go to', 'navigate to', 'change to', 'move to'
            ]
            
            # Common question patterns and phrases
            self.common_phrases = [
                'what is in readme.md', 'what is in the readme', 'show me the readme',
                'what files are here', 'what is in this directory', 'list all files',
                'show current directory', 'where am i', 'what is my current path',
                'how do i', 'what does', 'explain how to', 'tell me about',
                'create a new', 'generate a', 'make a new', 'build a',
                'install the', 'setup the', 'configure the', 'initialize the',
                'check the status', 'show the status', 'what is the status',
                'run the tests', 'execute the', 'start the server', 'launch the'
            ]
            
            self.path_completer = PathCompleter() if PathCompleter else None
            
        def get_completions(self, document: Document, complete_event: CompleteEvent):
            if not document or not hasattr(document, 'text'):
                return
                
            text = document.text
            word_before_cursor = document.get_word_before_cursor()
            
            # Meta commands completion
            if text.startswith(':'):
                for cmd in self.meta_commands:
                    if cmd.startswith(text):
                        yield Completion(cmd, start_position=-len(text))
                return
            
            # Shell command completion with !
            if text.startswith('!'):
                cmd_part = text[1:]
                # Complete shell commands
                for cmd in self.shell_commands:
                    if cmd.startswith(cmd_part):
                        yield Completion('!' + cmd, start_position=-len(text))
                
                # Path completion for commands that need paths
                if any(text.startswith('!' + cmd + ' ') for cmd in ['cd', 'ls', 'cat', 'rm', 'cp', 'mv']):
                    if self.path_completer:
                        # Extract the path part after the command
                        parts = text.split(' ', 1)
                        if len(parts) > 1:
                            path_part = parts[1]
                            path_doc = Document(path_part, len(path_part))
                            for completion in self.path_completer.get_completions(path_doc, complete_event):
                                yield Completion(
                                    completion.text,
                                    start_position=completion.start_position,
                                    display=completion.display
                                )
                return
            
            # Explain command completion with ?
            if text.startswith('?'):
                cmd_part = text[1:]
                for cmd in self.shell_commands:
                    if cmd.startswith(cmd_part):
                        yield Completion('?' + cmd, start_position=-len(text))
                return
            
            # Natural language completion
            text_lower = text.lower()
            
            # Check for common phrases first (more specific matches)
            for phrase in self.common_phrases:
                if phrase.startswith(text_lower) and len(text) > 0:
                    yield Completion(phrase, start_position=-len(text))
            
            # Then check for basic starters
            for starter in self.nl_starters:
                if starter.startswith(word_before_cursor.lower()) and len(word_before_cursor) > 0:
                    yield Completion(starter, start_position=-len(word_before_cursor))
            
            # Path completion for natural language commands
            if any(phrase in text_lower for phrase in ['go to', 'navigate to', 'change to', 'cd']):
                if self.path_completer:
                    for completion in self.path_completer.get_completions(document, complete_event):
                        yield completion
else:
    FlawHuntCLICompleter = None

# Constants
HISTORY_FILE = str(Path.home() / ".ai_terminal" / "repl_history.txt")

BANNER = Panel.fit(
    f"[bold bright_green]╔════════════════════════════════════════════════════════════════════════╗[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green] [bold bright_green]███████╗██╗      █████╗ ██╗    ██╗██╗  ██╗██╗   ██╗███╗   ██╗████████╗[/bold bright_green] [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green] [bold bright_green]██╔════╝██║     ██╔══██╗██║    ██║██║  ██║██║   ██║████╗  ██║╚══██╔══╝[/bold bright_green] [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green] [bold bright_green]█████╗  ██║     ███████║██║ █╗ ██║███████║██║   ██║██╔██╗ ██║   ██║[/bold bright_green]    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green] [bold bright_green]██╔══╝  ██║     ██╔══██║██║███╗██║██╔══██║██║   ██║██║╚██╗██║   ██║[/bold bright_green]    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green] [bold bright_green]██║     ███████╗██║  ██║╚███╔███╔╝██║  ██║╚██████╔╝██║ ╚████║   ██║[/bold bright_green]    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green] [bold bright_green]╚═╝     ╚══════╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝[/bold bright_green]    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green]                 [bold bright_green] ██████╗██╗     ██╗[/bold bright_green]                                    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green]                 [bold bright_green]██╔════╝██║     ██║[/bold bright_green]                                    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green]                 [bold bright_green]██║     ██║     ██║[/bold bright_green]                                    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green]                 [bold bright_green]██║     ██║     ██║[/bold bright_green]                                    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green]                 [bold bright_green]╚██████╗███████╗██║[/bold bright_green]                                    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]║[/bold bright_green]                 [bold bright_green] ╚═════╝╚══════╝╚═╝[/bold bright_green]                                    [bold bright_green]║[/bold bright_green]\n"
    f"[bold bright_green]╚════════════════════════════════════════════════════════════════════════╝[/bold bright_green]\n\n"
    f"[bold cyan]FlawHunt CLI[/bold cyan] — the smart CLI for cyber security professionals and ethical hackers [bold yellow]by GAMKERS[/bold yellow]\n"
    f"[dim]Platform: {get_platform_info()['system'].title()} | Modes: ask • generate • agent | Safe mode ON by default | Type ':help' for commands.[/dim]",
    border_style="bright_green",
)

HELP = f""" Operating Modes:
• ask - Direct answers without tools
• generate - Generate commands with confirmation  
• agent - Full agent with tools (default)

Meta commands:
:help Show this help
:safe on|off Toggle safe mode (recommended for security operations)
:verbose on|off Toggle verbose mode (show agent reasoning steps)
:model NAME Switch AI model (e.g., gemini-1.5-flash, llama-3.3-70b-versatile)
:provider NAME Switch AI provider (gemini or groq)
:history Show recent conversation history
:backup Create and upload chat backup to secure cloud storage
:import List and import chat backups from other devices
:stats Show system statistics and security metrics
:packages List available package managers and security tools
:learn TOOL Learn about cybersecurity tools and commands
:theme [name] Switch themes or show theme options
:clear Clear screen
:quit Exit

Security shortcuts:
!<cmd> Execute raw shell command (security-checked)
?<cmd> Explain command and security implications


Platform: {get_platform_info()['system'].title()}
Shell: {get_platform_info()['shell_executable']}

[bold cyan]FlawHunt CLI[/bold cyan] - Empowering ethical hackers with AI-assisted command line operations."""

def setup_api_keys():
    """Setup API keys and provider selection on first run."""
    from pathlib import Path
    
    config_dir = Path.home() / ".ai_terminal"
    config_dir.mkdir(exist_ok=True)
    
    # Check existing configuration
    config_file = config_dir / "config.txt"
    gemini_key_file = config_dir / "gemini_api_key.txt"
    groq_key_file = config_dir / "groq_api_key.txt"
    
    # Load existing config if available
    provider = "groq"
    model = "moonshotai/kimi-k2-instruct-0905"
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                lines = f.read().strip().split('\n')
                for line in lines:
                    if line.startswith('provider='):
                        provider = line.split('=', 1)[1]
                    elif line.startswith('model='):
                        model = line.split('=', 1)[1]
        except:
            pass
    
    # Check for existing API keys
    gemini_key = os.getenv("GEMINI_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not gemini_key and gemini_key_file.exists():
        with open(gemini_key_file, 'r') as f:
            gemini_key = f.read().strip()
            if gemini_key:
                os.environ["GEMINI_API_KEY"] = gemini_key
    
    if not groq_key and groq_key_file.exists():
        with open(groq_key_file, 'r') as f:
            groq_key = f.read().strip()
            if groq_key:
                os.environ["GROQ_API_KEY"] = groq_key
    
    # Check if we need to prompt for missing API key
    need_setup = False
    if provider == "gemini" and not gemini_key:
        need_setup = True
        console.print(Panel(
            "Gemini API key not found!\n\n"
            "You can get your free API key at:\n"
            "[blue underline]https://aistudio.google.com/apikey[/blue underline]\n\n"
            "Please enter your API key below:",
            title="Gemini API Key Required",
            border_style="yellow"
        ))
        try:
            api_key = input("Gemini API Key: ").strip()
            if not api_key:
                console.print("[red]API key is required.[/red]")
                return None, None, None, None
            
            with open(gemini_key_file, 'w') as f:
                f.write(api_key)
            os.environ["GEMINI_API_KEY"] = api_key
            gemini_key = api_key
            console.print("[green]Gemini API key saved successfully![/green]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[red]Setup cancelled.[/red]")
            return None, None, None, None
    
    elif provider == "groq" and not groq_key:
        need_setup = True
        console.print(Panel(
            "Groq API key not found!\n\n"
            "You can get your free API key at:\n"
            "[blue underline]https://console.groq.com/keys[/blue underline]\n\n"
            "Please enter your API key below:",
            title="Groq API Key Required",
            border_style="yellow"
        ))
        try:
            api_key = input("Groq API Key: ").strip()
            if not api_key:
                console.print("[red]API key is required.[/red]")
                return None, None, None, None
            
            with open(groq_key_file, 'w') as f:
                f.write(api_key)
            os.environ["GROQ_API_KEY"] = api_key
            groq_key = api_key
            console.print("[green]Groq API key saved successfully![/green]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[red]Setup cancelled.[/red]")
            return None, None, None, None
    
    # If we have keys and config, return current setup
    if (provider == "gemini" and gemini_key) or (provider == "groq" and groq_key):
        return provider, model, gemini_key, groq_key
    
    # Handle case where user has saved config but missing API key for that provider
    if config_file.exists() and ((provider == "gemini" and not gemini_key) or (provider == "groq" and not groq_key)):
        console.print(Panel(
            f"Configuration found for {provider.title()} provider, but API key is missing.\n\n"
            f"Would you like to:\n"
            f"1. Enter {provider.title()} API key\n"
            f"2. Switch to a different provider",
            title="Missing API Key",
            border_style="yellow"
        ))
        
        try:
            choice = input("Choose option (1 or 2): ").strip()
            if choice == "2":
                # Reset to first-time setup
                pass
            else:
                # Prompt for the missing key of the current provider
                if provider == "groq":
                    api_key = input("Groq API Key: ").strip()
                    if not api_key:
                        console.print("[red]API key is required for Groq provider.[/red]")
                        return None, None, None, None
                    with open(groq_key_file, 'w') as f:
                        f.write(api_key)
                    os.environ["GROQ_API_KEY"] = api_key
                    groq_key = api_key
                    console.print("[green]Groq API key saved successfully![/green]")
                else:
                    api_key = input("Gemini API Key: ").strip()
                    if not api_key:
                        console.print("[red]API key is required for Gemini provider.[/red]")
                        return None, None, None, None
                    with open(gemini_key_file, 'w') as f:
                        f.write(api_key)
                    os.environ["GEMINI_API_KEY"] = api_key
                    gemini_key = api_key
                    console.print("[green]Gemini API key saved successfully![/green]")
                # Return with newly saved key
                return provider, model, gemini_key, groq_key
        except (KeyboardInterrupt, EOFError):
            console.print("\n[red]Setup cancelled.[/red]")
            return None, None, None, None
    
    # First time setup
    console.print(Panel(
        "Welcome to FlawHunt CLI!\n\n"
        "Choose your AI provider:\n"
        "1. Groq (recommended) - Get key at: [blue underline]https://console.groq.com/keys[/blue underline]\n"
        "2. Gemini (Google) - Get key at: [blue underline]https://aistudio.google.com/apikey[/blue underline]",
        title="First Time Setup",
        border_style="green"
    ))
    
    try:
        choice = input("Choose provider (1 for Groq, 2 for Gemini | default 1): ").strip() or "1"

        if choice == "1":
            provider = "groq"
            console.print("\n[cyan]Available Groq models:[/cyan]")
            console.print("1. llama-3.3-70b-versatile (fast)")
            console.print("2. moonshotai/kimi-k2-instruct-0905 (default)")
            console.print("3. meta-llama/llama-4-maverick-17b-128e-instruct (fallback)")
            console.print("4. mixtral-8x7b-32768")

            model_choice = input("Choose model (1-4, default 2): ").strip() or "2"
            models = [
                "llama-3.3-70b-versatile",
                "moonshotai/kimi-k2-instruct-0905",
                "meta-llama/llama-4-maverick-17b-128e-instruct",
                "mixtral-8x7b-32768",
            ]
            model = models[int(model_choice) - 1] if model_choice in ["1", "2", "3", "4"] else "moonshotai/kimi-k2-instruct-0905"

        elif choice == "2":
            provider = "gemini"
            console.print("\n[cyan]Available Gemini models:[/cyan]")
            console.print("1. gemini-1.5-flash (fast, recommended)")
            console.print("2. gemini-1.5-pro (more capable)")
            console.print("3. gemini-1.5-pro-002 (latest)")

            model_choice = input("Choose model (1-3, default 1): ").strip() or "1"
            models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.5-pro-002"]
            model = models[int(model_choice) - 1] if model_choice in ["1", "2", "3"] else "gemini-1.5-flash"
        else:
            console.print("[red]Invalid choice.[/red]")
            return None, None, None, None

        # Prompt for API keys (ask Groq first since it's default)
        console.print(Panel(
            "Enter your API keys. The key for the chosen provider is required; the other is optional.",
            title="API Keys",
            border_style="cyan"
        ))

        # Groq key prompt (optional unless provider == groq)
        groq_input = input("Groq API Key (leave blank to skip): ").strip()
        if groq_input:
            with open(groq_key_file, 'w') as f:
                f.write(groq_input)
            os.environ["GROQ_API_KEY"] = groq_input
            groq_key = groq_input
            console.print("[green]Groq API key saved.[/green]")
        elif provider == "groq" and not groq_key:
            console.print("[red]Groq API key is required for Groq provider.[/red]")
            return None, None, None, None

        # Gemini key prompt (optional unless provider == gemini)
        gemini_input = input("Gemini API Key (leave blank to skip): ").strip()
        if gemini_input:
            with open(gemini_key_file, 'w') as f:
                f.write(gemini_input)
            os.environ["GEMINI_API_KEY"] = gemini_input
            gemini_key = gemini_input
            console.print("[green]Gemini API key saved.[/green]")
        elif provider == "gemini" and not gemini_key:
            console.print("[red]Gemini API key is required for Gemini provider.[/red]")
            return None, None, None, None

        # Save configuration
        with open(config_file, 'w') as f:
            f.write(f"provider={provider}\n")
            f.write(f"model={model}\n")

        console.print("[green]Setup completed successfully![/green]")
        return provider, model, gemini_key, groq_key

    except (KeyboardInterrupt, EOFError):
        console.print("\n[red]Setup cancelled.[/red]")
        return None, None, None, None

def select_mode():
    """Let user select the operating mode."""
    console.clear()
    
    # Display themed banner
    theme_manager.display_banner()
    
    # Get current theme for dynamic styling
    current_theme = theme_manager.get_current_theme()
    
    console.print(theme_manager.create_themed_panel(
        f"Select Operating Mode:\n\n"
        f"1. [{current_theme['modes']['sage']}]🤖 SAGE[/{current_theme['modes']['sage']}] - Your cybersec study buddy (ask mode)\n"
        f"   [{current_theme['muted']}]Direct answers without tools - Just pure knowledge drops[/{current_theme['muted']}]\n\n"
        f"2. [{current_theme['modes']['forge']}]⚒️ FORGE[/{current_theme['modes']['forge']}] - The command craftsman (generate mode)\n"
        f"   [{current_theme['muted']}]Generate commands with confirmation - Precision crafted tools[/{current_theme['muted']}]\n\n"
        f"3. [{current_theme['modes']['hunter']}]🎯 HUNTER[/{current_theme['modes']['hunter']}] - Elite operative (agent mode)\n"
        f"   [{current_theme['muted']}]Full agent with tools - Complete tactical operations[/{current_theme['muted']}]\n\n"
        f"[{current_theme['accent']}]Enter your choice (1-3, default: 3):[/{current_theme['accent']}]",
        title="FlawHunt CLI Mode Selection"
    ))
    
    try:
        choice = input(f"Mode choice: ").strip() or "3"
        modes = {
            "1": "ask",
            "2": "generate", 
            "3": "agent"
        }
        return modes.get(choice, "agent")
    except (KeyboardInterrupt, EOFError):
        console.print(f"\n[{current_theme['danger']}]Mode selection cancelled. Using default agent mode.[/{current_theme['danger']}]")
        return "agent"

def ask_mode(llm, conversation_history, state):
    """Direct Q&A mode without tools."""
    console.print(Panel(
        "[bold cyan]🤖 SAGE MODE[/bold cyan] - Your Cybersec Study Buddy\n"
        "[dim]\"Yo, let's break down some security concepts! No cap, I got all the knowledge you need.\"[/dim]\n\n"
        "Direct answers without tools - Just pure knowledge drops and explanations\n"
        "Commands: :help, :clear, :quit",
        border_style="cyan",
        title="[bold cyan]SAGE[/bold cyan]"
    ))
    
    if PromptSession:
        session = PromptSession(
            history=FileHistory(HISTORY_FILE),
            auto_suggest=AutoSuggestFromHistory(),
            completer=None,
            complete_while_typing=True
        )
        get_input = lambda: get_themed_input(theme_manager.get_themed_prompt("sage"), "sage")
    else:
        get_input = lambda: get_themed_input("sage> ", "sage")
    
    while True:
        try:
            text = get_input().strip()
            if not text:
                continue
            
            # Mode switching commands
            if text.startswith(":mode"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[yellow]Available modes:[/yellow]")
                    console.print("  sage - Direct answers and explanations")
                    console.print("  forge - Command generation and crafting")
                    console.print("  hunter - Advanced agent with tools")
                    console.print("[dim]Usage: :mode [sage|forge|hunter][/dim]")
                    continue
                
                mode = parts[1].lower()
                if mode == "sage":
                    console.print("[bright_cyan]🧙‍♂️ Already in SAGE mode![/bright_cyan]")
                    continue
                elif mode == "forge":
                    console.print("[orange1]⚒️ Switching to FORGE mode...[/orange1]")
                    return "switch_to_forge"
                elif mode == "hunter":
                    console.print("[bright_red]🎯 Switching to HUNTER mode...[/bright_red]")
                    return "switch_to_hunter"
                else:
                    console.print(f"[red]Unknown mode: {mode}[/red]")
                    console.print("[dim]Available modes: sage, forge, hunter[/dim]")
                continue
                
            if text == ":main_menu":
                console.print("[green]🏠 Returning to main menu...[/green]")
                return
            
            # Mode switching commands
            if text.startswith(":mode"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[yellow]Available modes:[/yellow]")
                    console.print("  sage - Direct answers and explanations")
                    console.print("  forge - Command generation and crafting")
                    console.print("  hunter - Advanced agent with tools")
                    console.print("[dim]Usage: :mode [sage|forge|hunter][/dim]")
                    continue
                
                mode = parts[1].lower()
                if mode == "sage":
                    console.print("[bright_cyan]🧙‍♂️ Already in SAGE mode![/bright_cyan]")
                    continue
                elif mode == "forge":
                    console.print("[orange1]⚒️ Switching to FORGE mode...[/orange1]")
                    return "switch_to_forge"
                elif mode == "hunter":
                    console.print("[bright_red]🎯 Switching to HUNTER mode...[/bright_red]")
                    return "switch_to_hunter"
                else:
                    console.print(f"[red]Unknown mode: {mode}[/red]")
                    console.print("[dim]Available modes: sage, forge, hunter[/dim]")
                continue
                
            if text == ":main_menu":
                console.print("[green]🏠 Returning to main menu...[/green]")
                return
                
            # Meta commands for theming
            if text.startswith(":theme"):
                parts = text.split()
                if len(parts) == 1:
                    # Show current theme and available themes
                    current_theme = theme_manager.current_theme
                    available_themes = list(theme_manager.themes.keys())
                    
                    theme_table = Table(title="Theme Configuration", box=box.MINIMAL_DOUBLE_HEAD)
                    theme_table.add_column("Setting", style="cyan")
                    theme_table.add_column("Value", style="green")
                    
                    theme_table.add_row("Current Theme", current_theme)
                    theme_table.add_row("Available Themes", ", ".join(available_themes))
                    
                    console.print(theme_table)
                    console.print("\n[dim]Commands:[/dim]")
                    console.print("  :theme <name> - Switch to theme")
                    console.print("  :theme preview <name> - Preview theme")
                    console.print("  :theme list - List all themes")
                    console.print("  :theme random - Random theme")
                    console.print("  :theme reset - Reset to default")
                elif parts[1] == "list":
                    themes = theme_manager.list_themes()
                    theme_names = [theme["name"] for theme in themes]
                    console.print(f"[cyan]Available themes:[/cyan] {', '.join(theme_names)}")
                elif parts[1] == "preview" and len(parts) > 2:
                    theme_name = parts[2]
                    if theme_name in theme_manager.themes:
                        theme_manager.show_theme_preview(theme_name)
                    else:
                        console.print(f"[red]Theme '{theme_name}' not found[/red]")
                elif parts[1] == "random":
                    import random
                    themes = list(theme_manager.themes.keys())
                    new_theme = random.choice(themes)
                    theme_manager.set_theme(new_theme)
                    config = get_config()
                    config.ui.theme = new_theme
                    config_manager.save_config(config)
                    console.print(f"[green]Switched to random theme: {new_theme}[/green]")
                    # Show themed banner
                    console.print(theme_manager.create_themed_panel(
                        theme_manager.get_banner(),
                        title="FlawHunt CLI"
                    ))
                elif parts[1] == "reset":
                    theme_manager.set_theme("cyber_hunter")
                    config = get_config()
                    config.ui.theme = "cyber_hunter"
                    config_manager.save_config(config)
                    console.print("[green]Theme reset to default (cyber_hunter)[/green]")
                elif len(parts) > 1:
                    theme_name = parts[1]
                    if theme_name in theme_manager.themes:
                        theme_manager.set_theme(theme_name)
                        config = get_config()
                        config.ui.theme = theme_name
                        config_manager.save_config(config)
                        console.print(f"[green]Switched to theme: {theme_name}[/green]")
                        # Show themed banner
                        console.print(theme_manager.create_themed_panel(
                            theme_manager.get_banner(),
                            title="FlawHunt CLI"
                        ))
                    else:
                        console.print(f"[red]Theme '{theme_name}' not found. Available themes: {', '.join(theme_manager.themes.keys())}[/red]")
                continue

            if text.startswith(":animation"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[dim]Animation commands:[/dim]")
                    console.print("  :animation matrix - Matrix digital rain")
                    console.print("  :animation glitch <text> - Glitch text effect")
                    console.print("  :animation typewriter <text> - Typewriter effect")
                    console.print("  :animation scan - Network scan simulation")
                    console.print("  :animation boot - Boot sequence")
                    console.print("  :animation pulse <text> - Pulsing text")
                    console.print("  :animation wave <text> - Wave text effect")
                elif parts[1] == "matrix":
                    animation_engine.matrix_rain(duration=5)
                elif parts[1] == "glitch" and len(parts) > 2:
                    text_to_glitch = " ".join(parts[2:])
                    animation_engine.glitch_text(text_to_glitch)
                elif parts[1] == "typewriter" and len(parts) > 2:
                    text_to_type = " ".join(parts[2:])
                    animation_engine.typewriter_effect(text_to_type)
                elif parts[1] == "scan":
                    animation_engine.network_scan_simulation()
                elif parts[1] == "boot":
                    animation_engine.boot_sequence()
                elif parts[1] == "pulse" and len(parts) > 2:
                    text_to_pulse = " ".join(parts[2:])
                    animation_engine.pulsing_text(text_to_pulse)
                elif parts[1] == "wave" and len(parts) > 2:
                    text_to_wave = " ".join(parts[2:])
                    animation_engine.waving_text(text_to_wave)
                else:
                    console.print("[red]Invalid animation command[/red]")
                continue

            if text == ":help":
                console.print("[cyan]Ask Mode Commands:[/cyan]")
                console.print("  :help - Show this help")
                console.print("  :mode [sage|forge|hunter] - Switch to different mode")
                console.print("  :main_menu - Return to main mode selection menu")
                console.print("  :backup - Create and upload chat backup")
                console.print("  :import - List available backups or import from device")
                console.print("  :clear - Clear screen")
                console.print("  :quit - Exit ask mode")
                continue
                
            if text.startswith(":backup"):
                parts = text.split()
                handle_backup_command(conversation_history, parts)
                continue
                
            if text.startswith(":import"):
                parts = text.split()
                handle_import_command(conversation_history, parts)
                continue
                
            if text.startswith(":mode"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[cyan]Available modes:[/cyan]")
                    console.print("  sage - Direct Q&A mode (current)")
                    console.print("  forge - Command generation mode")
                    console.print("  hunter - Full agent mode")
                    console.print("[dim]Usage: :mode <mode_name>[/dim]")
                elif len(parts) > 1:
                    mode_name = parts[1].lower()
                    if mode_name == "sage":
                        console.print("[cyan]Already in SAGE mode[/cyan]")
                    elif mode_name == "forge":
                        console.print("[orange1] to FORGE mode...[orange1]")
                        return "switch_to_forge"
                    elif mode_name == "hunter":
                        console.print("[red]Switching to HUNTER mode...[/red]")
                        return "switch_to_hunter"
                    else:
                        console.print(f"[red]Unknown mode: {mode_name}. Available: sage, forge, hunter[/red]")
                continue
                
            if text == ":main_menu":
                console.print("[dim]Returning to main menu...[/dim]")
                return "main_menu"
                
            if text == ":clear":
                console.clear()
                continue
                
            # Mode switching commands
            if text.startswith(":mode"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[yellow]Available modes:[/yellow]")
                    console.print("  sage - Direct answers and explanations")
                    console.print("  forge - Command generation and crafting")
                    console.print("  hunter - Advanced agent with tools")
                    console.print("[dim]Usage: :mode [sage|forge|hunter][/dim]")
                    continue
                
                mode = parts[1].lower()
                if mode == "sage":
                    console.print("[bright_cyan]🧙‍♂️ Switching to SAGE mode...[/bright_cyan]")
                    return "switch_to_sage"
                elif mode == "forge":
                    console.print("[orange1]⚒️ Switching to FORGE mode...[/orange1]")
                    return "switch_to_forge"
                elif mode == "hunter":
                    console.print("[bright_red]🎯 Already in HUNTER mode![/bright_red]")
                    continue
                else:
                    console.print(f"[red]Unknown mode: {mode}[/red]")
                    console.print("[dim]Available modes: sage, forge, hunter[/dim]")
                continue
                
            if text == ":main_menu":
                console.print("[green]🏠 Returning to main menu...[/green]")
                return
            
            if text in (":quit", ":exit"):
                break
            
            # Check if the user is directly entering a system command
            def is_system_command(text):
                """Check if the input looks like a direct system command"""
                # Only execute commands that start with !
                return text.startswith('!')
            
            # Check if it's a direct system command
            if is_system_command(text):
                console.print("[cyan]Executing system command...[/cyan]")
                
                # Clean the command (remove the ! prefix)
                clean_command = text.lstrip('!').strip()
                
                from rich.prompt import Confirm
                if Confirm.ask(f"Execute command: {clean_command} ?", default=False):
                    console.print(f"[green]Running: {clean_command}[/green]")
                    output = run_subprocess(clean_command)
                    console.print(theme_manager.create_themed_panel(
                        output or "[dim]no output[/dim]", 
                        title="Command Output"
                    ))
                    
                    # Save to conversation history
                    metadata = {
                        "mode": "ask", 
                        "model": llm.model, 
                        "provider": llm.provider, 
                        "command": clean_command,
                        "system_command": True
                    }
                    conversation_history.add_conversation(
                        user_input=text,
                        ai_response=f"Executed system command: {clean_command}",
                        metadata=metadata
                    )
                else:
                    console.print("[dim]Command execution cancelled.[/dim]")
                continue
            
            # Check if the user is requesting command generation (precise detection)
            def is_command_generation_request(text):
                """Check if the user is explicitly asking for command generation"""
                text_lower = text.lower().strip()
                
                # Explicit command generation requests
                explicit_patterns = [
                    "generate command",
                    "create command", 
                    "make command",
                    "write command",
                    "give me command",
                    "show me command",
                    "what command",
                    "which command",
                    "command for",
                    "command to"
                ]
                
                # Action requests that clearly need command execution
                action_patterns = [
                    "run nmap",
                    "run subfinder", 
                    "run gobuster",
                    "run nikto",
                    "run sqlmap",
                    "scan with",
                    "execute nmap",
                    "perform scan"
                ]
                
                # Check for explicit patterns or clear action requests
                return (any(pattern in text_lower for pattern in explicit_patterns) or 
                        any(pattern in text_lower for pattern in action_patterns))
            
            if is_command_generation_request(text):
                console.print("[yellow]Switching to generate mode...[/yellow]")
                
                # Execute generate mode logic for this single request
                context = conversation_history.format_context_for_agent(text)
                
                prompt = f"Generate a command to: {text}\n\n"
                if context:
                    prompt += f"Previous conversation context:\n{context}\n\n"
                prompt += "Please respond in JSON format with the following structure:\n"
                prompt += "{\n"
                prompt += '  "command": "the exact command to run",\n'
                prompt += '  "explanation": "brief explanation of what the command does",\n'
                prompt += '  "safety_considerations": "any safety considerations or warnings",\n'
                prompt += '  "has_command": true/false\n'
                prompt += "}\n\n"
                prompt += "Set 'has_command' to true if you can provide a specific command, false if the request cannot be fulfilled with a command."
                
                response = invoke_llm_with_animation(llm, prompt, "🤖 SAGE is analyzing")
                clean_response = clean_ai_response(response, preserve_formatting=True) if response else response
                
                # Parse JSON response to extract command and other information
                import json
                import re
                from rich.prompt import Confirm
                
                command = None
                explanation = ""
                safety_considerations = ""
                has_command = False
                
                try:
                    # Try to parse the response as JSON
                    json_match = re.search(r'\{.*\}', clean_response, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(0)
                        parsed_response = json.loads(json_str)
                        
                        command = parsed_response.get('command', '').strip()
                        explanation = parsed_response.get('explanation', '')
                        safety_considerations = parsed_response.get('safetyconsiderations', parsed_response.get('safety_considerations', ''))
                        has_command = parsed_response.get('hascommand', parsed_response.get('has_command', False))
                        
                        # Display formatted response
                        if has_command and command:
                            formatted_response = f"[bold green]Command:[/bold green] {command}\n\n"
                            formatted_response += f"[bold blue]Explanation:[/bold blue] {explanation}\n\n"
                            if safety_considerations:
                                formatted_response += f"[bold red]Safety Considerations:[/bold red] {safety_considerations}"
                            console.print(theme_manager.create_themed_panel(
                                formatted_response, 
                                title="Generated Command"
                            ))
                        else:
                            formatted_response = f"[bold yellow]No specific command available[/bold yellow]\n\n"
                            formatted_response += f"[bold blue]Explanation:[/bold blue] {explanation}"
                            console.print(theme_manager.create_themed_panel(
                                formatted_response, 
                                title="Response"
                            ))
                    else:
                        # Fallback: display original response if JSON parsing fails
                        console.print(theme_manager.create_themed_panel(
                            clean_response or "[dim]no response[/dim]", 
                            title="Generated Command"
                        ))
                        
                except (json.JSONDecodeError, AttributeError) as e:
                    # Fallback: display original response
                    console.print(theme_manager.create_themed_panel(
                        clean_response or "[dim]no response[/dim]", 
                        title="Generated Command",
                        mode="forge"
                    ))
                    console.print(f"[dim]Note: Response was not in expected JSON format[/dim]")
                
                # Execute command if available
                if command:
                    if Confirm.ask(f"Run command: {command} ?", default=False):
                        console.print(f"[green]Running: {command}[/green]")
                        output = run_subprocess(command)
                        console.print(theme_manager.create_themed_panel(
                            output or "[dim]no output[/dim]", 
                            title="Command Output"
                        ))
                    else:
                        console.print("[dim]Command execution cancelled.[/dim]")
                
                # Save to conversation history with additional metadata
                metadata = {
                    "mode": "generate", 
                    "model": llm.model, 
                    "provider": llm.provider, 
                    "command": command,
                    "has_command": has_command,
                    "explanation": explanation,
                    "safety_considerations": safety_considerations,
                    "auto_switched": True
                }
                conversation_history.add_conversation(
                    user_input=text,
                    ai_response=clean_response or "",
                    metadata=metadata
                )
                
                console.print("[yellow]Switching back to ask mode...[/yellow]")
                continue
            
            # Build context from conversation history using the proper method
            context = conversation_history.format_context_for_agent(text, max_context_length=1000)
            
            # SAGE personality system prompt
            sage_prompt = """🤖 I am SAGE - Your Cybersec Study Buddy from FlawHunt CLI.

"Yo, let's break down some security concepts! No cap, I got all the knowledge you need."

You are SAGE, a Gen Z cybersecurity expert who makes complex security concepts accessible and engaging. You're like that friend who actually knows their stuff and explains things in a way that just clicks. Your responses are:

- Clear and relatable (no unnecessary jargon)
- Engaging and conversational
- Packed with practical examples
- Encouraging and supportive
- Modern and up-to-date with current trends

You break down complex topics into digestible pieces, use analogies that make sense, and always keep it real about both the cool and challenging aspects of cybersecurity.

User Question: """
            
            # Use context if available, otherwise just the current text
            full_prompt = sage_prompt + (context + "\n\n" + text if context else text)
            
            # Direct LLM query with loading animation
            response = invoke_llm_with_animation(llm, full_prompt, "🤖 SAGE is thinking")
            clean_response = clean_ai_response(response, preserve_formatting=True) if response else response
            console.print(theme_manager.create_themed_panel(
                clean_response or "[dim]no response[/dim]", 
                title="SAGE Response",
                mode="sage"
            ))
            
            # Save to conversation history
            conversation_history.add_conversation(
                user_input=text,
                ai_response=clean_response or "",
                metadata={"mode": "ask", "model": llm.model, "provider": llm.provider}
            )
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Exiting ask mode...[/dim]")
            break

def generate_mode(llm, conversation_history, state):
    """Command generation mode with user confirmation."""
    console.print(theme_manager.create_themed_panel(
        "[orange1]⚒️ FORGE MODE[/orange1] - The Master Craftsman\n"
        "[dim]\"Every command is a tool, every tool has purpose. Let me craft what you need.\"[/dim]\n\n"
        "Generate commands with confirmation - Precision crafted for your needs\n"
        "Commands: :help, :clear, :quit",
        title="[bold orange1]FORGE[/bold orange1]"
    ))
    
    if PromptSession:
        session = PromptSession(
            history=FileHistory(HISTORY_FILE),
            auto_suggest=AutoSuggestFromHistory(),
            completer=None,
            complete_while_typing=True
        )
        get_input = lambda: get_themed_input(theme_manager.get_themed_prompt("forge"), "forge")
    else:
        get_input = lambda: get_themed_input("forge> ", "forge")
    
    from rich.prompt import Confirm
    
    while True:
        try:
            text = get_input().strip()
            if not text:
                continue
                
            # Meta commands for theming
            if text.startswith(":theme"):
                parts = text.split()
                if len(parts) == 1:
                    # Show current theme and available themes
                    current_theme = theme_manager.current_theme
                    available_themes = list(theme_manager.themes.keys())
                    
                    theme_table = Table(title="Theme Configuration", box=box.MINIMAL_DOUBLE_HEAD)
                    theme_table.add_column("Setting", style="cyan")
                    theme_table.add_column("Value", style="green")
                    
                    theme_table.add_row("Current Theme", current_theme)
                    theme_table.add_row("Available Themes", ", ".join(available_themes))
                    
                    console.print(theme_table)
                    console.print("\n[dim]Commands:[/dim]")
                    console.print("  :theme <name> - Switch to theme")
                    console.print("  :theme preview <name> - Preview theme")
                    console.print("  :theme list - List all themes")
                    console.print("  :theme random - Random theme")
                    console.print("  :theme reset - Reset to default")
                elif parts[1] == "list":
                    themes = theme_manager.list_themes()
                    theme_names = [theme["name"] for theme in themes]
                    console.print(f"[cyan]Available themes:[/cyan] {', '.join(theme_names)}")
                elif parts[1] == "preview" and len(parts) > 2:
                    theme_name = parts[2]
                    if theme_name in theme_manager.themes:
                        theme_manager.show_theme_preview(theme_name)
                    else:
                        console.print(f"[red]Theme '{theme_name}' not found[/red]")
                elif parts[1] == "random":
                    import random
                    available_themes = list(theme_manager.themes.keys())
                    new_theme = random.choice(available_themes)
                    if theme_manager.set_theme(new_theme):
                        console.print(f"[green]Switched to random theme: {new_theme}[/green]")
                        theme_manager.display_banner()
                    else:
                        console.print(f"[red]Failed to switch to theme: {new_theme}[/red]")
                elif parts[1] == "reset":
                    if theme_manager.set_theme("cyber_hunter"):
                        console.print("[green]Theme reset to default (cyber_hunter)[/green]")
                        theme_manager.display_banner()
                    else:
                        console.print("[red]Failed to reset theme[/red]")
                elif len(parts) > 1:
                    theme_name = parts[1]
                    if theme_name in theme_manager.themes:
                        if theme_manager.set_theme(theme_name):
                            console.print(f"[green]Switched to theme: {theme_name}[/green]")
                            theme_manager.display_banner()
                        else:
                            console.print(f"[red]Failed to switch to theme: {theme_name}[/red]")
                    else:
                        console.print(f"[red]Theme '{theme_name}' not found[/red]")
                        available_themes = list(theme_manager.themes.keys())
                        console.print(f"[dim]Available themes: {', '.join(available_themes)}[/dim]")
                continue
                
            if text == ":help":
                console.print("[yellow]Generate Mode Commands:[/yellow]")
                console.print("  :help - Show this help")
                console.print("  :theme [name] - Switch themes or show theme options")
                console.print("  :mode [sage|forge|hunter] - Switch to another mode")
                console.print("  :main_menu - Return to main menu")
                console.print("  :backup - Create and upload chat backup")
                console.print("  :import - List available backups or import from device")
                console.print("  :clear - Clear screen")
                console.print("  :quit - Exit generate mode")
                continue
                
            if text.startswith(":backup"):
                parts = text.split()
                handle_backup_command(conversation_history, parts)
                continue
                
            if text.startswith(":import"):
                parts = text.split()
                handle_import_command(conversation_history, parts)
                continue
                
            if text.startswith(":mode"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[yellow]Available modes:[/yellow]")
                    console.print("  sage - Direct answers and explanations")
                    console.print("  forge - Command generation and crafting")
                    console.print("  hunter - Advanced agent with tools")
                    console.print("[dim]Usage: :mode [sage|forge|hunter][/dim]")
                    continue
                
                mode = parts[1].lower()
                if mode == "sage":
                    console.print("[bright_cyan]🧙‍♂️ Switching to SAGE mode...[/bright_cyan]")
                    return "switch_to_sage"
                elif mode == "forge":
                    console.print("[orange1]⚒️ Already in FORGE mode![/orange1]")
                    continue
                elif mode == "hunter":
                    console.print("[bright_red]🎯 Switching to HUNTER mode...[/bright_red]")
                    return "switch_to_hunter"
                else:
                    console.print(f"[red]Unknown mode: {mode}[/red]")
                    console.print("[dim]Available modes: sage, forge, hunter[/dim]")
                continue
                
            if text == ":main_menu":
                console.print("[green]🏠 Returning to main menu...[/green]")
                return
                
            if text == ":clear":
                console.clear()
                continue
                
            if text in (":quit", ":exit"):
                break
            
            # Generate command based on user request with conversation context
            context = conversation_history.format_context_for_agent(text)
            
            # FORGE personality system prompt
            forge_prompt = """⚒️ I am FORGE - The Master Craftsman of FlawHunt CLI.

"Every command is a tool, every tool has purpose. Let me craft what you need."

You are FORGE, a master craftsman who specializes in creating precise, effective commands and tools. You approach each request with the methodical precision of a skilled artisan. Your responses are:

- Precise and purposeful
- Methodically crafted
- Focused on practical solutions
- Delivered with confidence and expertise
- Always considering safety and best practices

You take pride in creating the perfect tool for each task, explaining your craftsmanship and the reasoning behind your choices.

Request: """
            
            prompt = forge_prompt + f"{text}\n\n"
            if context:
                prompt += f"Previous conversation context:\n{context}\n\n"
            prompt += "Please respond in JSON format with the following structure:\n"
            prompt += "{\n"
            prompt += '  "command": "the exact command to run",\n'
            prompt += '  "explanation": "brief explanation of what the command does",\n'
            prompt += '  "safety_considerations": "any safety considerations or warnings",\n'
            prompt += '  "has_command": true/false\n'
            prompt += "}\n\n"
            prompt += "Set 'has_command' to true if you can provide a specific command, false if the request cannot be fulfilled with a command."
            
            response = invoke_llm_with_animation(llm, prompt, "⚒️ FORGE is crafting")
            clean_response = clean_ai_response(response, preserve_formatting=True) if response else response
            
            # Parse JSON response to extract command and other information
            import json
            import re
            
            command = None
            explanation = ""
            safety_considerations = ""
            has_command = False
            
            try:
                # Try to parse the response as JSON
                # First, try to extract JSON from the response if it's wrapped in other text
                json_match = re.search(r'\{.*\}', clean_response, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                    parsed_response = json.loads(json_str)
                    
                    command = parsed_response.get('command', '').strip()
                    explanation = parsed_response.get('explanation', '')
                    safety_considerations = parsed_response.get('safetyconsiderations', parsed_response.get('safety_considerations', ''))
                    has_command = parsed_response.get('hascommand', parsed_response.get('has_command', False))
                    
                    # Display formatted response
                    if has_command and command:
                        formatted_response = f"[bold green]Command:[/bold green] {command}\n\n"
                        formatted_response += f"[bold blue]Explanation:[/bold blue] {explanation}\n\n"
                        if safety_considerations:
                            formatted_response += f"[bold red]Safety Considerations:[/bold red] {safety_considerations}"
                        console.print(theme_manager.create_themed_panel(
                            formatted_response, 
                            title="Generated Command",
                            mode="forge"
                        ))
                    else:
                        formatted_response = f"[bold yellow]No specific command available[/bold yellow]\n\n"
                        formatted_response += f"[bold blue]Explanation:[/bold blue] {explanation}"
                        console.print(theme_manager.create_themed_panel(
                            formatted_response, 
                            title="Response",
                            mode="forge"
                        ))
                else:
                    # Fallback: display original response if JSON parsing fails
                    console.print(theme_manager.create_themed_panel(
                        clean_response or "[dim]no response[/dim]", 
                        title="Generated Command"
                    ))
                    
            except (json.JSONDecodeError, AttributeError) as e:
                # Fallback: display original response and try legacy parsing
                console.print(theme_manager.create_themed_panel(
                    clean_response or "[dim]no response[/dim]", 
                    title="Generated Command",
                    mode="forge"
                ))
                console.print(f"[dim]Note: Response was not in expected JSON format, using fallback parsing[/dim]")
                
                # Legacy fallback parsing (simplified version of old logic)
                if clean_response:
                    lines = clean_response.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line.startswith('Command:') or line.startswith('command:'):
                            if line.startswith('Command:'):
                                command = line[8:].strip()
                            elif line.startswith('command:'):
                                command = line[8:].strip()
                            break
                        elif line.startswith('`') and line.endswith('`'):
                            command = line[1:-1].strip()
                            break
            
            if command:
                if Confirm.ask(f"Run command: {command} ?", default=False):
                    console.print(f"[green]Running: {command}[/green]")
                    output = run_subprocess(command)
                    console.print(Panel(output or "[dim]no output[/dim]", title="Command Output", border_style="green"))
                else:
                    console.print("[dim]Command execution cancelled.[/dim]")
            
            # Save to conversation history with additional metadata
            metadata = {
                "mode": "generate", 
                "model": llm.model, 
                "provider": llm.provider, 
                "command": command,
                "has_command": has_command,
                "explanation": explanation,
                "safety_considerations": safety_considerations
            }
            conversation_history.add_conversation(
                user_input=text,
                ai_response=clean_response or "",
                metadata=metadata
            )
            
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Exiting generate mode...[/dim]")
            break

def main():
    """Main REPL loop for FlawHunt CLI."""
    state = load_state()
    
    # License validation check
    from ai_terminal.license import LicenseManager
    license_manager = LicenseManager()
    
    if not license_manager.check_license():
        console.print("[red]License validation failed. Exiting...[/red]")
        sys.exit(1)
    
    # Setup API keys and provider
    provider, model, gemini_key, groq_key = setup_api_keys()
    if not provider:
        sys.exit(1)
    
    # Use saved model preference or default from setup
    current_model = state.get("model", model)
    current_provider = state.get("provider", provider)
    
    llm = LLM(
        model=current_model, 
        provider=current_provider,
        gemini_api_key=gemini_key,
        groq_api_key=groq_key
    )
    
    # Check if LLM initialization was successful
    if not llm.langchain_mode and llm.sdk_model is None:
        console.print(f"[red]Failed to initialize {current_provider} provider. Please check your API key and try again.[/red]")
        if current_provider == "groq":
            console.print(f"[yellow]To fix this issue:[/yellow]")
            console.print(f"[yellow]1. Get your API key from: https://console.groq.com/keys[/yellow]")
            console.print(f"[yellow]2. Set it with: export GROQ_API_KEY=your_key_here[/yellow]")
            console.print(f"[yellow]3. Or run the application again to enter it interactively[/yellow]")
        elif current_provider == "gemini":
            console.print(f"[yellow]To fix this issue:[/yellow]")
            console.print(f"[yellow]1. Get your API key from: https://aistudio.google.com/apikey[/yellow]")
            console.print(f"[yellow]2. Set it with: export GEMINI_API_KEY=your_key_here[/yellow]")
            console.print(f"[yellow]3. Or run the application again to enter it interactively[/yellow]")
        sys.exit(1)
    
    # Initialize conversation history manager
    conversation_history = ConversationHistoryManager()
    
    # Select operating mode
    mode = select_mode()
    
    # Main mode loop to handle mode switching
    while True:
        result = None
        
        # Handle different modes
        if mode == "ask":
            result = ask_mode(llm, conversation_history, state)
        elif mode == "generate":
            result = generate_mode(llm, conversation_history, state)
        elif mode == "agent":
            result = agent_mode(llm, conversation_history, state)
        
        # Handle mode switching results
        if result == "switch_to_hunter":
            mode = "agent"
            continue
        elif result == "switch_to_forge":
            mode = "generate"
            continue
        elif result == "switch_to_sage":
            mode = "ask"
            continue
        elif result == "main_menu":
            mode = select_mode()
            continue
        else:
            # If no specific result or exit, break out of loop
            return
    
def agent_mode(llm, conversation_history, state):
    """Agent mode with full tools and capabilities"""
    vstore = VectorStore()
    # Ensure verbose setting is initialized in state
    if "verbose" not in state:
        state["verbose"] = True  # Default to True in HUNTER mode for detailed operations
        save_state(state)
    agent = AgentHarness(llm, state, vstore, conversation_history)
    
    console.print(theme_manager.create_themed_panel(
        "[bold red]🎯 HUNTER MODE[/bold red] - The Elite Operative\n"
        "[dim]\"In the shadows of cyberspace, I am your eyes and hands. Every vulnerability will be found.\"[/dim]\n\n"
        "Full agent with tools - Advanced reconnaissance and exploitation capabilities\n"
        "Type your mission objectives and I'll execute with precision.",
        title="[bold red]HUNTER[/bold red]"
    ))
    console.print(theme_manager.create_themed_panel(
        HELP.strip(), 
        title="Commands"
    ))
    # Start filesystem monitor in background (watch current directory)
    monitor = None
    try:
        from pathlib import Path as _P
        monitor = start_file_monitor(_P.cwd())
    except Exception:
        monitor = None
    
    from pathlib import Path
    
    if PromptSession:
        completer = FlawHuntCLICompleter() if Completer else None
        
        # Create key bindings for better tab completion
        bindings = KeyBindings() if KeyBindings else None
        
        session = PromptSession(
            history=FileHistory(HISTORY_FILE), 
            auto_suggest=AutoSuggestFromHistory(),
            completer=completer,
            complete_while_typing=True,
            key_bindings=bindings,
            complete_style='multi-column',
            mouse_support=True,
        )
        get_input = lambda: get_themed_input(theme_manager.get_themed_prompt("hunter"), "hunter")
    else:
        get_input = lambda: get_themed_input("hunter> ", "hunter")
    
    try:
        while True:
            text = get_input().strip()
            if not text:
                continue
            
            # Meta commands
            if text == ":help":
                console.print(Panel(HELP.strip(), border_style="gray50", box=box.ROUNDED))
                continue
            
            if text.startswith(":safe"):
                _, *rest = text.split()
                if rest and rest[0].lower() == "off":
                    state["safe_mode"] = False
                else:
                    state["safe_mode"] = True
                save_state(state)
                console.print(f"Safe mode = {state['safe_mode']}")
                continue
            
            if text.startswith(":verbose"):
                _, *rest = text.split()
                if rest and rest[0].lower() in ["off", "false", "0", "no"]:
                    state["verbose"] = False
                elif rest and rest[0].lower() in ["on", "true", "1", "yes"]:
                    state["verbose"] = True
                else:
                    # Toggle if no parameter given
                    state["verbose"] = not state.get("verbose", False)
                save_state(state)
                agent.set_verbose(state["verbose"])
                console.print(f"Verbose mode = {state['verbose']}")
                continue
            
            if text.startswith(":model"):
                _, *rest = text.split(maxsplit=1)
                if rest:
                    state["model"] = rest[0].strip()
                    save_state(state)
                    console.print(f"Model set to {state['model']}. Restart recommended.")
                else:
                    console.print(f"Current model: {state.get('model', 'llama-3.3-70b-versatile')}")
                continue
            
            if text.startswith(":provider"):
                _, *rest = text.split(maxsplit=1)
                if rest:
                    new_provider = rest[0].strip().lower()
                    if new_provider in ["gemini", "groq"]:
                        state["provider"] = new_provider
                        # Set default model for the provider
                        if new_provider == "gemini":
                            state["model"] = "gemini-1.5-flash"
                        else:
                            state["model"] = "llama-3.3-70b-versatile"
                        save_state(state)
                        console.print(f"Provider set to {new_provider} with model {state['model']}. Restart recommended.")
                    else:
                        console.print("[red]Invalid provider. Use 'gemini' or 'groq'.[/red]")
                else:
                    console.print(f"Current provider: {state.get('provider', 'groq')}")
                continue
            
            if text.startswith(":history"):
                parts = text.split()
                if len(parts) == 1:
                    # Show recent history
                    conversation_history.display_history(limit=10)
                elif parts[1] == "search" and len(parts) > 2:
                    # Search history
                    query = " ".join(parts[2:])
                    results = conversation_history.search_conversations(query)
                    if results:
                        console.print(f"[cyan]Found {len(results)} matches for '{query}':[/cyan]")
                        conversation_history.display_history(limit=10, session_id=None)
                    else:
                        console.print(f"[dim]No matches found for '{query}'[/dim]")
                elif parts[1] == "clear":
                    if len(parts) > 2 and parts[2] == "all":
                        conversation_history.clear_history()
                        console.print("[green]All conversation history cleared.[/green]")
                    else:
                        conversation_history.clear_history(conversation_history.current_session_id)
                        console.print("[green]Current session history cleared.[/green]")
                elif parts[1] == "export" and len(parts) > 2:
                    filepath = parts[2]
                    if conversation_history.export_history(filepath):
                        console.print(f"[green]History exported to {filepath}[/green]")
                    else:
                        console.print("[red]Failed to export history[/red]")
                elif parts[1] == "stats":
                    stats = conversation_history.get_stats()
                    stats_tbl = Table(title="Conversation History Statistics", box=box.MINIMAL_DOUBLE_HEAD)
                    stats_tbl.add_column("Metric", style="cyan")
                    stats_tbl.add_column("Value", style="green")
                    for key, value in stats.items():
                        if key == "vector_store" and isinstance(value, dict):
                            # Display vector store stats separately
                            for vkey, vvalue in value.items():
                                formatted_key = f"Vector {vkey.replace('_', ' ').title()}"
                                stats_tbl.add_row(formatted_key, str(vvalue))
                        else:
                            formatted_key = key.replace("_", " ").title()
                            stats_tbl.add_row(formatted_key, str(value))
                    console.print(stats_tbl)
                elif parts[1] == "similar" and len(parts) > 2:
                    # Search for similar conversations
                    query = " ".join(parts[2:])
                    conversation_history.display_similar_conversations(query)
                elif parts[1] == "vector":
                    # Vector store specific commands
                    if len(parts) > 2 and parts[2] == "rebuild":
                        conversation_history.vector_store._rebuild_mappings_and_index()
                        console.print("[green]Vector store rebuilt successfully![/green]")
                    elif len(parts) > 2 and parts[2] == "status":
                        vstats = conversation_history.vector_store.get_stats()
                        console.print(f"Vector Store Status: {'Enabled' if vstats['enabled'] else 'Disabled'}")
                        console.print(f"Total Vectors: {vstats['total_vectors']}")
                        console.print(f"Model: {vstats['model_name']}")
                    else:
                        console.print("[yellow]Vector commands:[/yellow]")
                        console.print("  :history vector status - Show vector store status")
                        console.print("  :history vector rebuild - Rebuild vector index")
                else:
                    console.print("[yellow]History commands:[/yellow]")
                    console.print("  :history - Show recent conversations")
                    console.print("  :history search <query> - Search conversations by content")
                    console.print("  :history similar <query> - Find similar conversations (semantic)")
                    console.print("  :history clear - Clear current session")
                    console.print("  :history clear all - Clear all history")
                    console.print("  :history export <file> - Export history")
                    console.print("  :history stats - Show statistics")
                    console.print("  :history vector status - Vector store status")
                continue
            
            if text.startswith(":backup"):
                parts = text.split()
                if len(parts) == 1:
                    # Perform backup
                    console.print("[yellow]Creating chat backup...[/yellow]")
                    
                    try:
                        # Get license and device information
                        from ai_terminal.license import LicenseManager
                        license_manager = LicenseManager()
                        
                        license_key = license_manager.load_license_key()
                        device_info = license_manager.load_device_info()
                        
                        if not license_key or not device_info:
                            console.print("[red]License information not found. Please ensure you're properly licensed.[/red]")
                            continue
                        
                        mac_address = device_info.get("mac_address")
                        device_name = device_info.get("device_name")
                        
                        # Get conversation history
                        all_conversations = conversation_history.get_all_conversations()
                        sessions = conversation_history.get_all_sessions()
                        
                        # Prepare backup data
                        backup_data = {
                            "conversations": all_conversations,
                            "sessions": sessions,
                            "backup_timestamp": datetime.now().isoformat(),
                            "version": "1.0.0"
                        }
                        
                        # Calculate backup size and conversation count
                        import json
                        backup_json = json.dumps(backup_data)
                        backup_size = len(backup_json.encode('utf-8'))
                        conversation_count = len(all_conversations)
                        
                        # Prepare webhook payload
                        webhook_payload = {
                            "license_key": license_key,
                            "device_name": device_name,
                            "mac_address": mac_address,
                            "chat_data": backup_data,
                            "backup_size": backup_size,
                            "conversation_count": conversation_count,
                            "metadata": {
                                "cli_version": "1.0.0",
                                "platform": get_platform_info()['system'],
                                "backup_type": "manual"
                            }
                        }
                        
                        # Send to webhook
                        import requests
                        from ai_terminal.config import get_config
                        
                        # Get webhook URL from config
                        config = get_config()
                        webhook_url = config.backup.webhook_url
                        
                        headers = {
                            "Content-Type": "application/json"
                        }
                        
                        console.print("[yellow]Sending backup to server...[/yellow]")
                        response = requests.post(
                            webhook_url,
                            json=webhook_payload,
                            headers=headers,
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            console.print(f"[green]✓ Backup completed successfully![/green]")
                            console.print(f"[cyan]Backup ID: {result.get('backup_id', 'N/A')}[/cyan]")
                            console.print(f"[cyan]Conversations backed up: {conversation_count}[/cyan]")
                            console.print(f"[cyan]Backup size: {backup_size:,} bytes[/cyan]")
                        else:
                            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {"error": response.text}
                            console.print(f"[red]✗ Backup failed: {error_data.get('error', 'Unknown error')}[/red]")
                            
                    except requests.exceptions.Timeout:
                        console.print("[red]✗ Backup failed: Request timed out. Please check your internet connection.[/red]")
                    except requests.exceptions.ConnectionError:
                        console.print("[red]✗ Backup failed: Cannot connect to backup server. Please check your internet connection.[/red]")
                    except Exception as e:
                        console.print(f"[red]✗ Backup failed: {str(e)}[/red]")
                        
                elif parts[1] == "help":
                    console.print("[yellow]Backup commands:[/yellow]")
                    console.print("  :backup - Create and upload chat backup")
                    console.print("  :backup help - Show this help")
                else:
                    console.print("[red]Unknown backup command. Use ':backup help' for available options.[/red]")
                continue
            
            if text.startswith(":import"):
                parts = text.split()
                if len(parts) == 1:
                    handle_import_command(conversation_history, parts)
                elif len(parts) == 2:
                    handle_import_command(conversation_history, parts)
                else:
                    console.print("[red]Usage: :import or :import <device_name>[/red]")
                continue
            
            if text == ":platform":
                platform_info = get_platform_info()
                plat_tbl = Table(title="Platform Information", box=box.MINIMAL_DOUBLE_HEAD)
                plat_tbl.add_column("Property", style="cyan")
                plat_tbl.add_column("Value", style="green")
                plat_tbl.add_row("Operating System", platform_info['system'].title())
                plat_tbl.add_row("Shell Executable", platform_info['shell_executable'])
                plat_tbl.add_row("Package Manager", platform_info['package_manager'])
                plat_tbl.add_row("Path Separator", platform_info['path_separator'])
                plat_tbl.add_row("Python Version", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
                console.print(plat_tbl)
                continue

            # Todo commands
            if text.startswith(":todo"):
                parts = text.split(maxsplit=2)
                
                if len(parts) == 1 or parts[1] == "list":
                    # Show current todo list
                    result = agent.ask("Use todo_manager with action 'list' to show current todo")
                    console.print(result)
                elif parts[1] == "progress":
                    # Show progress report
                    result = agent.ask("Use todo_manager with action 'progress' to show detailed progress")
                    console.print(result)
                elif parts[1] == "add" and len(parts) > 2:
                    # Add new task
                    task = parts[2]
                    result = agent.ask(f"Use todo_manager to add task: {task}")
                    console.print(result)
                elif parts[1] == "mark" and len(parts) > 2:
                    # Mark task complete/incomplete
                    try:
                        task_id = int(parts[2])
                        result = agent.ask(f"Use todo_manager to mark task {task_id}")
                        console.print(result)
                    except ValueError:
                        console.print("[red]Error: Task ID must be a number[/red]")
                elif parts[1] == "clear":
                    # Clear completed tasks
                    result = agent.ask("Use todo_manager with action 'clear' to remove completed tasks")
                    console.print(result)
                elif parts[1] == "create" and len(parts) > 2:
                    # Create new todo list
                    title = parts[2]
                    result = agent.ask(f"Use todo_manager to create new todo list: {title}")
                    console.print(result)
                elif parts[1] == "export" and len(parts) > 2:
                    # Export todo list
                    filename = parts[2]
                    result = agent.ask(f"Use todo_manager to export todo to {filename}")
                    console.print(result)
                else:
                    console.print("[yellow]Todo commands:[/yellow]")
                    console.print("  :todo or :todo list - Show current todo list")
                    console.print("  :todo progress - Show detailed progress report")
                    console.print("  :todo add <task> - Add new task")
                    console.print("  :todo mark <number> - Toggle task completion")
                    console.print("  :todo clear - Remove completed tasks")
                    console.print("  :todo create <title> - Create new todo list")
                    console.print("  :todo export <filename> - Export todo list")
                continue

            if text == ":stats":
                from ai_terminal.tools import ToolLearnerTool
                
                stats_tbl = Table(title="System Statistics", box=box.MINIMAL_DOUBLE_HEAD)
                stats_tbl.add_column("Component", style="cyan")
                stats_tbl.add_column("Status", style="green")
                
                # Vector store stats
                vstore_stats = vstore.get_stats()
                stats_tbl.add_row("Vector Store", f"{vstore_stats['total_documents']} documents")
                
                # Platform info
                platform_info = get_platform_info()
                stats_tbl.add_row("Package Manager", platform_info['package_manager'])
                stats_tbl.add_row("Shell", platform_info['shell_executable'])
                
                # Memory count
                memory_count = len(state.get("memory", []))
                stats_tbl.add_row("Memory Entries", str(memory_count))
                
                console.print(stats_tbl)
                continue

            if text == ":packages":
                platform_info = get_platform_info()
                pm = platform_info['package_manager']
                
                pm_tbl = Table(title="Package Managers", box=box.MINIMAL_DOUBLE_HEAD)
                pm_tbl.add_column("System", style="cyan")
                pm_tbl.add_column("Manager", style="green")
                pm_tbl.add_row(platform_info['system'].title(), pm)
                
                if pm != "unknown":
                    pm_tbl.add_row("Available", f"Use 'package_manager search <package>' or 'python_packages search <package>'")
                
                console.print(pm_tbl)
                continue

            if text.startswith(":learn"):
                _, *rest = text.split(maxsplit=1)
                if rest:
                    tool_name = rest[0].strip()
                    from ai_terminal.tools import ToolLearnerTool
                    
                    learner = ToolLearnerTool(llm_instance=llm)
                    info = learner._run(tool_name)
                    console.print(Panel(info, title=f"Learn: {tool_name}", border_style="blue"))
                else:
                    console.print("Usage: :learn <tool_name>")
                continue
            
            if text.startswith(":session"):
                parts = text.split()
                if len(parts) == 1:
                    # Show all sessions
                    conversation_history.display_sessions()
                elif parts[1] == "new":
                    name = " ".join(parts[2:]) if len(parts) > 2 else None
                    session_id = conversation_history.create_session(name)
                    agent.reset_session_history()  # Reset agent session history
                    console.print(f"[green]Created new session: {session_id[:8]}[/green]")
                elif parts[1] == "switch" and len(parts) > 2:
                    session_id = parts[2]
                    # Allow partial ID matching
                    matching_sessions = [sid for sid in conversation_history.sessions.keys() if sid.startswith(session_id)]
                    if len(matching_sessions) == 1:
                        if conversation_history.switch_session(matching_sessions[0]):
                            agent.reset_session_history()  # Reset agent session history
                            console.print(f"[green]Switched to session: {matching_sessions[0][:8]}[/green]")
                        else:
                            console.print("[red]Failed to switch session[/red]")
                    elif len(matching_sessions) > 1:
                        console.print(f"[yellow]Multiple sessions match '{session_id}'. Please be more specific.[/yellow]")
                    else:
                        console.print(f"[red]No session found matching '{session_id}'[/red]")
                else:
                    console.print("[yellow]Session commands:[/yellow]")
                    console.print("  :session - List all sessions")
                    console.print("  :session new [name] - Create new session")
                    console.print("  :session switch <id> - Switch to session")
                continue
            
            if text == ":clear":
                console.clear()
                continue
            
            # Theme commands
            if text.startswith(":theme"):
                parts = text.split()
                if len(parts) == 1:
                    # Show available themes
                    themes = theme_manager.list_themes()
                    theme_names = [theme["name"] for theme in themes]
                    console.print(f"[cyan]Available themes:[/cyan] {', '.join(theme_names)}")
                elif parts[1] == "list":
                    themes = theme_manager.list_themes()
                    theme_names = [theme["name"] for theme in themes]
                    console.print(f"[cyan]Available themes:[/cyan] {', '.join(theme_names)}")
                elif parts[1] == "preview":
                    if len(parts) > 2:
                        theme_name = parts[2]
                        theme_manager.show_theme_preview(theme_name)
                    else:
                        console.print("[red]Please specify a theme name for preview[/red]")
                elif parts[1] == "random":
                    theme_manager.set_random_theme()
                    console.print(f"[green]Switched to random theme: {theme_manager.current_theme}[/green]")
                elif parts[1] == "reset":
                    theme_manager.set_theme("cyber_hunter")
                    console.print("[green]Theme reset to default (cyber_hunter)[/green]")
                elif len(parts) > 1:
                    theme_name = parts[1]
                    if theme_manager.set_theme(theme_name):
                        console.print(f"[green]Theme switched to: {theme_name}[/green]")
                    else:
                        console.print(f"[red]Theme '{theme_name}' not found. Use ':theme list' to see available themes.[/red]")
                continue
            
            # Animation commands
            if text.startswith(":animation"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[yellow]Available animations:[/yellow]")
                    console.print("  :animation matrix - Matrix digital rain")
                    console.print("  :animation glitch - Glitch text effect")
                    console.print("  :animation typewriter - Typewriter effect")
                    console.print("  :animation network - Network scan simulation")
                    console.print("  :animation boot - Boot sequence")
                    console.print("  :animation pulse - Pulsing text")
                    console.print("  :animation wave - Waving text")
                elif parts[1] == "matrix":
                    animation_engine.matrix_rain(duration=5)
                elif parts[1] == "glitch":
                    animation_engine.glitch_text("SYSTEM COMPROMISED", duration=3)
                elif parts[1] == "typewriter":
                    animation_engine.typewriter_effect("Initializing FlawHunt CLI systems...", delay=0.05)
                elif parts[1] == "network":
                    animation_engine.network_scan(["192.168.1.1", "10.0.0.1", "172.16.0.1"])
                elif parts[1] == "boot":
                    animation_engine.boot_sequence()
                elif parts[1] == "pulse":
                    animation_engine.pulsing_text("HUNTER MODE ACTIVE", duration=3)
                elif parts[1] == "wave":
                    animation_engine.waving_text("FlawHunt CLI", duration=3)
                else:
                    console.print(f"[red]Unknown animation: {parts[1]}[/red]")
                continue
            
            # Progress bar commands
            if text.startswith(":progress"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[yellow]Available progress demos:[/yellow]")
                    console.print("  :progress loading - Loading animation")
                    console.print("  :progress transfer - File transfer simulation")
                    console.print("  :progress scan - System scan simulation")
                    console.print("  :progress multi - Multi-task progress")
                    console.print("  :progress install - Package installation")
                    console.print("  :progress vuln - Vulnerability scan")
                    console.print("  :progress network - Network discovery")
                elif parts[1] == "loading":
                    progress_manager.loading("Initializing systems", 2.0)
                elif parts[1] == "transfer":
                    progress_manager.file_transfer("exploit.py", 5.0)
                elif parts[1] == "scan":
                    progress_manager.system_scan()
                elif parts[1] == "multi":
                    progress_manager.multi_task()
                elif parts[1] == "install":
                    progress_manager.install_packages()
                elif parts[1] == "vuln":
                    progress_manager.vulnerability_scan()
                elif parts[1] == "network":
                    progress_manager.network_discovery()
                else:
                    console.print(f"[red]Unknown progress demo: {parts[1]}[/red]")
                continue
            
            # Mode switching commands
            if text.startswith(":mode"):
                parts = text.split()
                if len(parts) == 1:
                    console.print("[yellow]Available modes:[/yellow]")
                    console.print("  sage - Direct answers and explanations")
                    console.print("  forge - Command generation and crafting")
                    console.print("  hunter - Advanced agent with tools")
                    console.print("[dim]Usage: :mode [sage|forge|hunter][/dim]")
                    continue
                
                mode = parts[1].lower()
                if mode == "sage":
                    console.print("[bright_cyan]🧙‍♂️ Switching to SAGE mode...[/bright_cyan]")
                    return "switch_to_sage"
                elif mode == "forge":
                    console.print("[orange1]⚒️ Switching to FORGE mode...[/orange1]")
                    return "switch_to_forge"
                elif mode == "hunter":
                    console.print("[bright_red]🎯 Already in HUNTER mode![/bright_red]")
                    continue
                else:
                    console.print(f"[red]Unknown mode: {mode}[/red]")
                    console.print("[dim]Available modes: sage, forge, hunter[/dim]")
                continue
                
            if text == ":main_menu":
                console.print("[green]🏠 Returning to main menu...[/green]")
                return
            
            if text in (":quit", ":exit"):
                break
            
            # Shell shortcuts
            if text.startswith("!"):
                from rich.prompt import Confirm
                
                cmd = text[1:].strip()
                
                # Handle cd commands specially using DirectoryNavigationTool
                if cmd.startswith(("cd ", "cd")) or cmd in ["pwd", "ls", "dir"]:
                    from ai_terminal.tools import DirectoryNavigationTool
                    
                    nav_tool = DirectoryNavigationTool(get_state=lambda: state)
                    
                    # Map shell commands to DirectoryNavigationTool commands
                    if cmd == "pwd":
                        nav_cmd = "current path"
                    elif cmd in ["ls", "dir"]:
                        nav_cmd = "list"
                    elif cmd.startswith("cd "):
                        path = cmd[3:].strip()
                        nav_cmd = f"go to {path}"
                    elif cmd == "cd":
                        nav_cmd = "go home"
                    else:
                        nav_cmd = cmd
                    
                    try:
                        output = nav_tool._run(nav_cmd)
                        console.print(Panel(output, title=cmd, border_style="green"))
                    except Exception as e:
                        console.print(Panel(f"Error: {e}", title=cmd, border_style="red"))
                    continue
                
                if looks_dangerous(cmd):
                    console.print("[red]Blocked dangerous command.[/red]")
                    continue
                
                if state.get("safe_mode", True):
                    if not Confirm.ask(f"Run: {cmd} ?", default=False):
                        console.print("Canceled.")
                        continue
                
                output = run_subprocess(cmd)
                console.print(Panel(output or "[dim]no output[/dim]", title=cmd, border_style="green"))
                continue
            
            if text.startswith("?"):
                from ai_terminal.tools import ExplainTool
                
                cmd = text[1:].strip()
                exp = ExplainTool()._run(cmd)
                console.print(Panel(exp or "[dim]no info[/dim]", title=f"Explain: {cmd}", border_style="yellow"))
                continue
            
            # Agent flow - inject conversation context
            
            # Check for previous execution
            exact_matches = [
                e for e in conversation_history.conversations 
                if e.user_input.strip().lower() == text.strip().lower()
            ]
            
            if exact_matches:
                most_recent = sorted(exact_matches, key=lambda x: x.timestamp, reverse=True)[0]
                created_time = most_recent.get_formatted_time()
                
                console.print(f"[bold yellow]It seems I see the results in your previous conversation ({created_time}).[/bold yellow]")
                
                # Check for "y" or "rerun" to bypass
                should_rerun = False
                if text.lower() in ["y", "yes", "rerun"]:
                     # If the user explicitly typed 'y' as a command, they probably meant to answer a previous prompt, 
                     # but here we are treating 'text' as the command itself. 
                     # Actually, the user flow is: User types "get subdomains..." -> System finds match -> Prompts.
                     pass

                from rich.prompt import Confirm
                if not Confirm.ask("Do you like me to re run it?", default=True):
                     console.print(theme_manager.create_themed_panel(
                         most_recent.ai_response, 
                         f"HUNTER Cached Response ({created_time})", 
                         mode="hunter"
                     ))
                     continue
                
                # If rerun confirmed, force fresh execution by disabling history context
                reply = agent.ask(text, use_history=False)
            else:
                reply = agent.ask(text)
            # Clean the AI response to remove markdown formatting but preserve line breaks
            clean_reply = clean_ai_response(reply, preserve_formatting=True) if reply else reply
            console.print(theme_manager.create_themed_panel(clean_reply or "[dim]no reply[/dim]", "HUNTER Response", mode="hunter"))
            
            # Save conversation to enhanced history system
            conversation_history.add_conversation(
                user_input=text,
                ai_response=clean_reply or "",
                metadata={
                    "model": llm.model,
                    "provider": llm.provider,
                    "safe_mode": state.get("safe_mode", True)
                }
            )
            
            # Keep old memory system for backward compatibility
            state.setdefault("memory", []).append({"user": text, "ai": clean_reply, "ts": time.time()})
            if len(state["memory"]) > 200:
                state["memory"] = state["memory"][-200:]
            save_state(state)
            
            if vstore.enabled:
                vstore.add(f"User: {text}\nAI: {clean_reply}")
    
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Bye[/dim]")
        return "exit"
    finally:
        try:
            if monitor:
                monitor.stop()
        except Exception:
            pass

if __name__ == "__main__":
    main()