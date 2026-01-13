"""
Advanced animation system for FlawHunt CLI.
Provides loading animations, visual effects, and interactive elements.
"""
import time
import random
import threading
from typing import List, Dict, Any, Optional, Callable
from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.align import Align
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeElapsedColumn
from rich.table import Table
from rich import box
import math

class AnimationEngine:
    """Advanced animation engine for terminal effects."""
    
    def __init__(self, console: Optional[Console] = None, theme_manager=None):
        self.console = console or Console()
        self.theme_manager = theme_manager
        self.is_running = False
        self.animation_thread = None
        
    def get_theme_colors(self):
        """Get current theme colors."""
        if self.theme_manager:
            theme = self.theme_manager.get_current_theme()
            return {
                'primary': theme['primary'],
                'secondary': theme['secondary'],
                'accent': theme['accent'],
                'success': theme['success'],
                'warning': theme['warning'],
                'danger': theme['danger'],
                'border': theme['border']
            }
        return {
            'primary': 'cyan',
            'secondary': 'blue',
            'accent': 'magenta',
            'success': 'green',
            'warning': 'yellow',
            'danger': 'red',
            'border': 'white'
        }
        
    def matrix_digital_rain(self, duration: float = 10.0, width: int = 80, height: int = 25):
        """Create Matrix-style digital rain effect."""
        colors = self.get_theme_colors()
        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        drops = []
        
        # Initialize drops
        for i in range(width // 2):
            drops.append({
                'x': i * 2,
                'y': random.randint(-height, 0),
                'speed': random.uniform(0.5, 2.0),
                'chars': [random.choice(chars) for _ in range(random.randint(5, 15))]
            })
        
        with Live(refresh_per_second=20, console=self.console) as live:
            start_time = time.time()
            
            while time.time() - start_time < duration:
                lines = [' ' * width for _ in range(height)]
                
                for drop in drops:
                    for i, char in enumerate(drop['chars']):
                        y_pos = int(drop['y'] + i)
                        if 0 <= y_pos < height and 0 <= drop['x'] < width:
                            # Use themed colors for the matrix effect
                            if i == 0:  # Leading character
                                color = colors['accent']
                            elif i < 3:  # Bright trail
                                color = colors['primary']
                            else:  # Fading trail
                                color = colors['secondary']
                            
                            # Safely insert character with proper string handling
                            line = list(lines[y_pos])
                            if drop['x'] < len(line):
                                line[drop['x']] = char
                            lines[y_pos] = ''.join(line)
                
                # Update drop positions
                for drop in drops:
                    drop['y'] += drop['speed']
                    if drop['y'] > height + len(drop['chars']):
                        drop['y'] = random.randint(-height//2, 0)
                        drop['x'] = random.randint(0, width-1)
                        drop['chars'] = [random.choice(chars) for _ in range(random.randint(5, 15))]
                
                # Create display with themed colors
                display_lines = []
                for line in lines:
                    colored_line = f"[{colors['primary']}]{line}[/{colors['primary']}]"
                    display_lines.append(colored_line)
                
                display_text = '\n'.join(display_lines)
                live.update(Text.from_markup(display_text))
                time.sleep(0.05)
    
    def cyber_loading_bar(self, total_steps: int = 100, description: str = "Initializing Systems"):
        """Create a cyberpunk-style loading bar."""
        colors = self.get_theme_colors()
        loading_chars = ["▱", "▰"]
        
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[{colors['primary']}]{description}[/{colors['primary']}]"),
            BarColumn(bar_width=40, complete_style=colors['success']),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Loading...", total=total_steps)
            
            for i in range(total_steps):
                # Simulate variable loading speed
                delay = random.uniform(0.01, 0.1)
                time.sleep(delay)
                progress.update(task, advance=1)
                
                # Add some glitch effects
                if random.randint(1, 20) == 1:
                    time.sleep(0.2)  # Brief pause for "glitch"
    
    def glitch_text_animation(self, text: str, duration: float = 3.0, intensity: int = 5):
        """Animate text with glitch effects using themed colors."""
        colors = self.get_theme_colors()
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        original_text = text
        
        with Live(refresh_per_second=15, console=self.console) as live:
            start_time = time.time()
            
            while time.time() - start_time < duration:
                glitched_text = ""
                
                for i, char in enumerate(original_text):
                    if random.randint(1, 100) <= intensity:
                        # Glitch this character
                        if random.randint(1, 3) == 1:
                            # Replace with glitch character
                            glitch_char = random.choice(glitch_chars)
                            glitched_text += f"[{colors['danger']}]{glitch_char}[/{colors['danger']}]"
                        else:
                            # Color shift using theme colors
                            theme_colors = [colors['accent'], colors['warning'], colors['secondary']]
                            color = random.choice(theme_colors)
                            glitched_text += f"[{color}]{char}[/{color}]"
                    else:
                        glitched_text += f"[{colors['primary']}]{char}[/{colors['primary']}]"
                
                panel = Panel(
                    Align.center(glitched_text),
                    border_style=colors['danger'],
                    box=box.HEAVY
                )
                live.update(panel)
                time.sleep(0.1)
            
            # Show final clean text
            final_panel = Panel(
                Align.center(f"[{colors['success']}]{original_text}[/{colors['success']}]"),
                border_style=colors['success'],
                box=box.DOUBLE
            )
            live.update(final_panel)
            time.sleep(1)
    
    def typewriter_with_cursor(self, text: str, delay: float = 0.05, cursor_char: str = "▌"):
        """Typewriter effect with blinking cursor."""
        with Live(refresh_per_second=20, console=self.console) as live:
            displayed_text = ""
            
            for char in text:
                displayed_text += char
                content = f"[bright_green]{displayed_text}[/bright_green][bright_yellow]{cursor_char}[/bright_yellow]"
                live.update(content)
                time.sleep(delay)
            
            # Blink cursor a few times
            for _ in range(6):
                content = f"[bright_green]{displayed_text}[/bright_green]"
                live.update(content)
                time.sleep(0.3)
                
                content = f"[bright_green]{displayed_text}[/bright_green][bright_yellow]{cursor_char}[/bright_yellow]"
                live.update(content)
                time.sleep(0.3)
            
            # Final text without cursor
            final_content = f"[bright_green]{displayed_text}[/bright_green]"
            live.update(final_content)
    
    def scanning_animation(self, target: str = "192.168.1.0/24", duration: float = 5.0):
        """Simulate network scanning animation."""
        scan_states = ["Scanning", "Analyzing", "Probing", "Detecting", "Mapping"]
        
        with Live(refresh_per_second=10, console=self.console) as live:
            start_time = time.time()
            
            while time.time() - start_time < duration:
                # Generate fake scan results
                current_ip = f"192.168.1.{random.randint(1, 254)}"
                state = random.choice(scan_states)
                port = random.choice([22, 80, 443, 8080, 3389, 21, 25])
                
                # Create scan display
                table = Table(box=box.MINIMAL_DOUBLE_HEAD, border_style="bright_cyan")
                table.add_column("Target", style="bright_yellow")
                table.add_column("Status", style="bright_green")
                table.add_column("Current", style="bright_white")
                
                table.add_row(target, f"{state}...", f"{current_ip}:{port}")
                
                # Add some discovered hosts
                for _ in range(random.randint(1, 5)):
                    fake_ip = f"192.168.1.{random.randint(1, 254)}"
                    status = random.choice(["OPEN", "CLOSED", "FILTERED"])
                    color = "bright_green" if status == "OPEN" else "dim red" if status == "CLOSED" else "bright_yellow"
                    table.add_row("", f"[{color}]{status}[/{color}]", fake_ip)
                
                panel = Panel(
                    table,
                    title="🔍 Network Reconnaissance",
                    border_style="bright_cyan"
                )
                
                live.update(panel)
                time.sleep(0.5)
    
    def boot_sequence_animation(self, system_name: str = "HUNTER OS"):
        """Simulate system boot sequence."""
        boot_messages = [
            "Initializing kernel modules...",
            "Loading security protocols...",
            "Mounting encrypted filesystems...",
            "Starting network interfaces...",
            "Initializing AI subsystems...",
            "Loading cybersecurity tools...",
            "Establishing secure connections...",
            "Activating stealth mode...",
            "System ready for operations..."
        ]
        
        self.console.print(f"\n[bright_cyan]╔══════════════════════════════════════╗[/bright_cyan]")
        self.console.print(f"[bright_cyan]║[/bright_cyan]     [bright_green]{system_name} BOOT SEQUENCE[/bright_green]      [bright_cyan]║[/bright_cyan]")
        self.console.print(f"[bright_cyan]╚══════════════════════════════════════╝[/bright_cyan]\n")
        
        for i, message in enumerate(boot_messages):
            # Show loading dots
            for dots in range(4):
                dot_str = "." * dots
                self.console.print(f"\r[bright_yellow]>[/bright_yellow] {message}{dot_str}   ", end="")
                time.sleep(0.2)
            
            # Show completion
            self.console.print(f"\r[bright_green]✓[/bright_green] {message}                    ")
            time.sleep(random.uniform(0.1, 0.5))
        
        self.console.print(f"\n[bright_green]🎯 {system_name} initialized successfully![/bright_green]\n")
    
    def pulse_effect(self, text: str, duration: float = 3.0):
        """Create pulsing text effect."""
        colors = ["dim white", "white", "bright_white", "white"]
        
        with Live(refresh_per_second=8, console=self.console) as live:
            start_time = time.time()
            color_index = 0
            
            while time.time() - start_time < duration:
                color = colors[color_index % len(colors)]
                content = f"[{color}]{text}[/{color}]"
                
                panel = Panel(
                    Align.center(content),
                    border_style=color,
                    box=box.ROUNDED
                )
                
                live.update(panel)
                color_index += 1
                time.sleep(0.25)
    
    def wave_text_animation(self, text: str, duration: float = 4.0):
        """Create wave effect on text."""
        with Live(refresh_per_second=20, console=self.console) as live:
            start_time = time.time()
            
            while time.time() - start_time < duration:
                wave_text = ""
                current_time = time.time() - start_time
                
                for i, char in enumerate(text):
                    # Calculate wave offset
                    wave_offset = math.sin(current_time * 3 + i * 0.3) * 2
                    
                    # Apply color based on wave position
                    if wave_offset > 1:
                        color = "bright_cyan"
                    elif wave_offset > 0:
                        color = "cyan"
                    elif wave_offset > -1:
                        color = "blue"
                    else:
                        color = "dim blue"
                    
                    wave_text += f"[{color}]{char}[/{color}]"
                
                panel = Panel(
                    Align.center(wave_text),
                    border_style="bright_blue",
                    box=box.DOUBLE
                )
                
                live.update(panel)
                time.sleep(0.05)
    
    def simple_thinking_animation(self, message: str = "🤖 SAGE is thinking", animation_done_flag=None):
        """Simple thinking animation with dots that clears itself and responds to done flag."""
        colors = self.get_theme_colors()
        dots_cycle = ["", ".", "..", "..."]
        
        # Show the message with cycling dots until animation is done
        i = 0
        while True:
            # Check if animation should stop
            if animation_done_flag and animation_done_flag.is_set():
                break
                
            dots = dots_cycle[i % len(dots_cycle)]
            print(f"\r{message}{dots}   ", end="", flush=True)
            time.sleep(0.1)
            i += 1
            
            # Safety timeout after 30 seconds
            if i > 300:
                break
        
        # Clear the line completely
        print(f"\r{' ' * (len(message) + 10)}", end="", flush=True)
        print("\r", end="", flush=True)

    def hacker_terminal_simulation(self, duration: float = 8.0):
        """Simulate hacker terminal activity."""
        commands = [
            "nmap -sS 192.168.1.0/24",
            "sqlmap -u http://target.com/login.php",
            "hydra -l admin -P passwords.txt ssh://target.com",
            "metasploit > use exploit/windows/smb/ms17_010_eternalblue",
            "john --wordlist=rockyou.txt hashes.txt",
            "aircrack-ng -w wordlist.txt capture.cap",
            "gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/common.txt"
        ]
        
        outputs = [
            "Host is up (0.0012s latency)",
            "Parameter 'username' appears to be injectable",
            "Login successful: admin:password123",
            "Exploit completed successfully",
            "Password found: secret123",
            "WPA handshake captured",
            "Found: /admin (Status: 200)"
        ]
        
        with Live(refresh_per_second=10, console=self.console) as live:
            start_time = time.time()
            terminal_lines = []
            
            while time.time() - start_time < duration:
                # Add new command
                if random.randint(1, 30) == 1:  # Occasionally add new command
                    cmd = random.choice(commands)
                    terminal_lines.append(f"[bright_green]root@hunter:~#[/bright_green] [bright_white]{cmd}[/bright_white]")
                    
                    # Add output after a delay
                    if random.randint(1, 2) == 1:
                        output = random.choice(outputs)
                        terminal_lines.append(f"[bright_yellow]{output}[/bright_yellow]")
                
                # Keep only last 15 lines
                if len(terminal_lines) > 15:
                    terminal_lines = terminal_lines[-15:]
                
                # Create terminal display
                content = "\n".join(terminal_lines)
                if not content:
                    content = "[bright_green]root@hunter:~#[/bright_green] [bright_white]_[/bright_white]"
                
                panel = Panel(
                    content,
                    title="🖥️  Elite Hacker Terminal",
                    border_style="bright_green",
                    box=box.HEAVY
                )
                
                live.update(panel)
                time.sleep(0.3)

# Global animation engine instance
animation_engine = AnimationEngine()

def show_matrix_rain(duration: float = 5.0):
    """Show matrix rain effect."""
    animation_engine.matrix_digital_rain(duration)

def show_loading_bar(steps: int = 100, description: str = "Loading"):
    """Show cyber loading bar."""
    animation_engine.cyber_loading_bar(steps, description)

def show_glitch_text(text: str, duration: float = 3.0):
    """Show glitch text animation."""
    animation_engine.glitch_text_animation(text, duration)

def show_boot_sequence(system_name: str = "HUNTER OS"):
    """Show boot sequence animation."""
    animation_engine.boot_sequence_animation(system_name)

def show_typewriter(text: str, delay: float = 0.05):
    """Show typewriter effect."""
    animation_engine.typewriter_with_cursor(text, delay)