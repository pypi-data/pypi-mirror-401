"""
Advanced theming system for FlawHunt CLI.
Provides multiple visual themes, ASCII art, animations, and customization options.
"""
import time
import random
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich import box
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.live import Live
import threading

class ThemeManager:
    """Manages visual themes and customization for the terminal."""
    
    def __init__(self):
        self.current_theme = "cyber_hunter"
        self.console = Console()
        self.themes = self._load_themes()
        self.ascii_art = self._load_ascii_art()
        self.animations = self._load_animations()
        
    def _load_themes(self) -> Dict[str, Dict[str, Any]]:
        """Load all available themes."""
        return {
            "cyber_hunter": {
                "name": "🎯 Cyber Hunter",
                "primary": "bright_green",
                "secondary": "green",
                "accent": "bright_cyan",
                "warning": "orange1",
                "danger": "bright_red",
                "info": "bright_blue",
                "success": "bright_green",
                "muted": "dim white",
                "border": "bright_green",
                "background": "black",
                "box_style": box.DOUBLE,
                "description": "Elite cybersecurity operative theme with matrix-style green",
                "modes": {
                    "sage": "bright_blue",      # Bright blue for knowledge/wisdom
                    "forge": "orange1",   # Bright yellow for crafting/creation
                    "hunter": "bright_green"    # Bright green for hunting/operations
                }
            },
            "neon_purple": {
                "name": "💜 Neon Purple",
                "primary": "bright_magenta",
                "secondary": "magenta",
                "accent": "bright_cyan",
                "warning": "orange1",
                "danger": "bright_red",
                "info": "bright_blue",
                "success": "bright_green",
                "muted": "dim white",
                "border": "bright_magenta",
                "background": "black",
                "box_style": box.HEAVY,
                "description": "Futuristic neon purple theme for night hackers",
                "modes": {
                    "sage": "bright_blue",      # Bright blue for knowledge
                    "forge": "orange1",   # Bright yellow for crafting
                    "hunter": "bright_magenta"  # Bright magenta for hunting
                }
            },
            "ocean_blue": {
                "name": "🌊 Ocean Blue",
                "primary": "bright_blue",
                "secondary": "blue",
                "accent": "bright_cyan",
                "warning": "orange1",
                "danger": "bright_red",
                "info": "bright_white",
                "success": "bright_green",
                "muted": "dim cyan",
                "border": "bright_blue",
                "background": "black",
                "box_style": box.ROUNDED,
                "description": "Deep ocean blue theme for calm operations",
                "modes": {
                    "sage": "bright_cyan",      # Bright cyan for wisdom
                    "forge": "orange1",   # Bright yellow for creation
                    "hunter": "bright_blue"     # Bright blue for operations
                }
            },
            "fire_red": {
                "name": "🔥 Fire Red",
                "primary": "bright_red",
                "secondary": "red",
                "accent": "orange1",
                "warning": "bright_orange",
                "danger": "bright_red",
                "info": "bright_white",
                "success": "bright_green",
                "muted": "dim red",
                "border": "bright_red",
                "background": "black",
                "box_style": box.DOUBLE_EDGE,
                "description": "Aggressive red theme for high-intensity operations",
                "modes": {
                    "sage": "bright_white",     # Bright white for knowledge
                    "forge": "orange1",         # Orange color for crafting
                    "hunter": "bright_red"      # Bright red for aggressive hunting
                }
            },
            "stealth_gray": {
                "name": "👤 Stealth Gray",
                "primary": "bright_white",
                "secondary": "white",
                "accent": "bright_cyan",
                "warning": "orange1",
                "danger": "bright_red",
                "info": "bright_blue",
                "success": "bright_green",
                "muted": "dim white",
                "border": "white",
                "background": "black",
                "box_style": box.ASCII,
                "description": "Minimalist gray theme for stealth operations",
                "modes": {
                    "sage": "bright_blue",      # Bright blue for knowledge
                    "forge": "orange1",   # Bright yellow for crafting
                    "hunter": "bright_white"    # Bright white for stealth
                }
            },
            "rainbow": {
                "name": "🌈 Rainbow",
                "primary": "bright_cyan",
                "secondary": "cyan",
                "accent": "bright_magenta",
                "warning": "orange1",
                "danger": "bright_red",
                "info": "bright_blue",
                "success": "bright_green",
                "muted": "dim white",
                "border": "bright_cyan",
                "background": "black",
                "box_style": box.HEAVY_EDGE,
                "description": "Colorful rainbow theme for creative hackers",
                "modes": {
                    "sage": "bright_blue",      # Bright blue for wisdom
                    "forge": "orange1",   # Bright yellow for creation
                    "hunter": "bright_magenta"  # Bright magenta for hunting
                }
            }
        }
    
    def _load_ascii_art(self) -> Dict[str, List[str]]:
        """Load ASCII art banners for different themes."""
        return {
            "cyber_hunter": [
                """
╔═══════════════════════════════════════════════════════════════════════╗
║                 ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗   ║
║                 ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗  ║
║                 ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝  ║
║                 ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗  ║
║                 ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║  ║
║                 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═══════╝╚═╝  ╚═╝  ║
╚═══════════════════════════════════════════════════════════════════════╝
                """,
                """
╔═══════════════════════════════════════════════════════════════════════╗
║                 ██╗  ██╗██╗   ██╗███╗   ██╗████████╗███████╗██████╗   ║
║                 ██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗  ║
║                 ███████║██║   ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝  ║
║                 ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗  ║
║                 ██║  ██║╚██████╔╝██║ ╚████║   ██║   ███████╗██║  ██║  ║
║                 ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═══════╝╚═╝  ╚═╝  ║
╚═══════════════════════════════════════════════════════════════════════╝
                """
            ],
            "neon_purple": [
                """
    ███╗   ██╗███████╗ ██████╗ ███╗   ██╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
    ████╗  ██║██╔════╝██╔═══██╗████╗  ██║    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
    ██╔██╗ ██║█████╗  ██║   ██║██╔██╗ ██║    ███████║███████║██║     █████╔╝ 
    ██║╚██╗██║██╔══╝  ██║   ██║██║╚██╗██║    ██╔══██║██╔══██║██║     ██╔═██╗ 
    ██║ ╚████║███████╗╚██████╔╝██║ ╚████║    ██║  ██║██║  ██║╚██████╗██║  ██╗
    ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                """
            ],
            "ocean_blue": [
                """
     ██████╗  ██████╗███████╗ █████╗ ███╗   ██╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
    ██╔═══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
    ██║   ██║██║     █████╗  ███████║██╔██╗ ██║    ███████║███████║██║     █████╔╝ 
    ██║   ██║██║     ██╔══╝  ██╔══██║██║╚██╗██║    ██╔══██║██╔══██║██║     ██╔═██╗ 
    ╚██████╔╝╚██████╗███████╗██║  ██║██║ ╚████║    ██║  ██║██║  ██║╚██████╗██║  ██╗
     ╚═════╝  ╚═════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                """
            ],
            "fire_red": [
                """
    ███████╗██╗██████╗ ███████╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
    ██╔════╝██║██╔══██╗██╔════╝    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
    █████╗  ██║██████╔╝█████╗      ███████║███████║██║     █████╔╝ 
    ██╔══╝  ██║██╔══██╗██╔══╝      ██╔══██║██╔══██║██║     ██╔═██╗ 
    ██║     ██║██║  ██║███████╗    ██║  ██║██║  ██║╚██████╗██║  ██╗
    ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
                """
            ],
            "stealth_gray": [
                """
    ███████╗████████╗███████╗ █████╗ ██╗  ████████╗██╗  ██╗
    ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║  ╚══██╔══╝██║  ██║
    ███████╗   ██║   █████╗  ███████║██║     ██║   ███████║
    ╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██║   ██╔══██║
    ███████║   ██║   ███████╗██║  ██║███████╗██║   ██║  ██║
    ╚══════╝   ╚═╝   ╚═══════╝╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝  ╚═╝
                """
            ],
            "rainbow": [
                """
    ██████╗  █████╗ ██╗███╗   ██╗██████╗  ██████╗ ██╗    ██╗
    ██╔══██╗██╔══██╗██║████╗  ██║██╔══██╗██╔═══██╗██║    ██║
    ██████╔╝███████║██║██╔██╗ ██║██████╔╝██║   ██║██║ █╗ ██║
    ██╔══██╗██╔══██║██║██║╚██╗██║██╔══██╗██║   ██║██║███╗██║
    ██║  ██║██║  ██║██║██║ ╚████║██████╔╝╚██████╔╝╚███╔███╔╝
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝  ╚══╝╚══╝ 
                """
            ]
        }
    
    def _load_animations(self) -> Dict[str, List[str]]:
        """Load animation frames for loading screens."""
        return {
            "matrix": [
                "▓░░░░░░░░░",
                "█▓░░░░░░░░",
                "██▓░░░░░░",
                "███▓░░░░░",
                "████▓░░░░",
                "█████▓░░",
                "██████▓░",
                "███████▓",
                "████████"
            ],
            "cyber": [
                "[    ]",
                "[=   ]",
                "[==  ]",
                "[=== ]",
                "[====]",
                "[ ===]",
                "[  ==]",
                "[   =]",
                "[    ]"
            ],
            "pulse": [
                "●○○○○",
                "○●○○○",
                "○○●○○",
                "○○○●○",
                "○○○○●",
                "○○○●○",
                "○○●○○",
                "○●○○○"
            ]
        }
    
    def get_theme(self, theme_name: Optional[str] = None) -> Dict[str, Any]:
        """Get theme configuration."""
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes["cyber_hunter"])
    
    def set_theme(self, theme_name: str) -> bool:
        """Set the current theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def list_themes(self) -> List[Dict[str, str]]:
        """List all available themes."""
        return [
            {
                "name": theme["name"],
                "key": key,
                "description": theme["description"]
            }
            for key, theme in self.themes.items()
        ]
    
    def get_banner(self, theme_name: Optional[str] = None) -> str:
        """Get ASCII art banner for theme."""
        if theme_name is None:
            theme_name = self.current_theme
        
        banners = self.ascii_art.get(theme_name, self.ascii_art["cyber_hunter"])
        return random.choice(banners)
    
    def create_themed_panel(self, content: str, title: str = "", theme_name: Optional[str] = None, mode: Optional[str] = None) -> Panel:
        """Create a panel with current theme styling."""
        theme = self.get_theme(theme_name)
        
        # Use mode-specific color if mode is provided and exists in theme
        border_style = theme["border"]
        if mode and "modes" in theme and mode in theme["modes"]:
            border_style = theme["modes"][mode]
        
        return Panel(
            content,
            title=title,
            border_style=border_style,
            box=theme["box_style"]
        )
    
    def create_themed_table(self, title: str = "", theme_name: Optional[str] = None) -> Table:
        """Create a table with current theme styling."""
        theme = self.get_theme(theme_name)
        return Table(
            title=title,
            box=theme["box_style"],
            border_style=theme["border"]
        )
    
    def animate_loading(self, message: str = "Loading", duration: float = 3.0, animation: str = "matrix"):
        """Display animated loading screen."""
        theme = self.get_theme()
        frames = self.animations.get(animation, self.animations["matrix"])
        
        with Live(refresh_per_second=10) as live:
            start_time = time.time()
            frame_index = 0
            
            while time.time() - start_time < duration:
                frame = frames[frame_index % len(frames)]
                content = f"[{theme['primary']}]{message}[/{theme['primary']}]\n\n[{theme['accent']}]{frame}[/{theme['accent']}]"
                panel = self.create_themed_panel(content, "🔄 Processing")
                live.update(Align.center(panel))
                
                time.sleep(0.1)
                frame_index += 1
    
    def show_theme_preview(self, theme_name: str):
        """Show a preview of a theme."""
        if theme_name not in self.themes:
            self.console.print(f"[red]Theme '{theme_name}' not found![/red]")
            return
        
        theme = self.themes[theme_name]
        
        # Create preview content
        preview_content = f"""
[{theme['primary']}]Primary Color[/{theme['primary']}] - Main interface elements
[{theme['secondary']}]Secondary Color[/{theme['secondary']}] - Supporting elements  
[{theme['accent']}]Accent Color[/{theme['accent']}] - Highlights and emphasis
[{theme['warning']}]Warning Color[/{theme['warning']}] - Caution messages
[{theme['danger']}]Danger Color[/{theme['danger']}] - Error messages
[{theme['info']}]Info Color[/{theme['info']}] - Information messages
[{theme['success']}]Success Color[/{theme['success']}] - Success messages
[{theme['muted']}]Muted Color[/{theme['muted']}] - Subtle text

{self.get_banner(theme_name)}
        """
        
        panel = Panel(
            preview_content.strip(),
            title=f"🎨 {theme['name']} Preview",
            subtitle=theme['description'],
            border_style=theme['border'],
            box=theme['box_style']
        )
        
        self.console.print(panel)
    
    def create_progress_bar(self, description: str = "Processing", theme_name: Optional[str] = None):
        """Create a themed progress bar."""
        theme = self.get_theme(theme_name)
        
        return Progress(
            SpinnerColumn(spinner_style=theme['accent']),
            TextColumn(f"[{theme['primary']}]{description}[/{theme['primary']}]"),
            BarColumn(bar_width=None, style=theme['secondary'], complete_style=theme['success']),
            TaskProgressColumn(style=theme['info'])
        )
    
    def display_banner(self, theme_name: Optional[str] = None):
        """Display the themed banner for the current theme."""
        theme = self.get_theme(theme_name)
        banner_art = self.get_banner(theme_name)
        
        # Create banner content with theme colors
        banner_content = f"[{theme['primary']}]{banner_art}[/{theme['primary']}]\n\n"
        banner_content += f"[{theme['accent']}]FlawHunt CLI[/{theme['accent']}] — the smart CLI for cyber security professionals and ethical hackers\n"
        banner_content += f"[{theme['muted']}]Theme: {theme['name']} | Safe mode ON by default | Type ':help' for commands.[/{theme['muted']}]"
        
        panel = Panel(
            banner_content,
            border_style=theme['border'],
            box=theme['box_style']
        )
        
        self.console.print(panel)
    
    def get_themed_prompt(self, mode: str) -> str:
        """Get a themed prompt string for the specified mode."""
        theme = self.get_theme()
        
        # Get mode-specific color from theme, fallback to default colors
        mode_colors = theme.get('modes', {})
        
        mode_configs = {
            "sage": {
                "icon": "🤖",
                "name": "sage",
                "color": mode_colors.get('sage', theme['info'])
            },
            "forge": {
                "icon": "⚒️",
                "name": "forge", 
                "color": mode_colors.get('forge', theme['warning'])
            },
            "hunter": {
                "icon": "🎯",
                "name": "hunter",
                "color": mode_colors.get('hunter', theme['danger'])
            }
        }
        
        config = mode_configs.get(mode.lower(), {
            "icon": "›",
            "name": mode,
            "color": theme['primary']
        })
        
        return f"[{config['color']}]{config['icon']} {config['name']}›[/{config['color']}] "

    def get_current_theme(self) -> Dict[str, Any]:
        """Get the current theme configuration."""
        return self.get_theme()
    
    def matrix_rain_effect(self, duration: float = 5.0):
        """Display matrix rain effect."""
        theme = self.get_theme()
        chars = "01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン"
        
        with Live(refresh_per_second=20) as live:
            start_time = time.time()
            
            while time.time() - start_time < duration:
                lines = []
                for _ in range(20):
                    line = ''.join(random.choice(chars) for _ in range(80))
                    lines.append(f"[{theme['primary']}]{line}[/{theme['primary']}]")
                
                content = '\n'.join(lines)
                live.update(content)
                time.sleep(0.05)
    
    def glitch_text(self, text: str, intensity: int = 3) -> str:
        """Apply glitch effect to text."""
        theme = self.get_theme()
        glitch_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        result = []
        for char in text:
            if random.randint(1, 10) <= intensity:
                glitch_char = random.choice(glitch_chars)
                result.append(f"[{theme['danger']}]{glitch_char}[/{theme['danger']}]")
            else:
                result.append(char)
        
        return ''.join(result)
    
    def typewriter_effect(self, text: str, delay: float = 0.05):
        """Display text with typewriter effect."""
        theme = self.get_theme()
        
        with Live(refresh_per_second=20) as live:
            displayed_text = ""
            for char in text:
                displayed_text += char
                content = f"[{theme['primary']}]{displayed_text}[/{theme['primary']}]▌"
                live.update(content)
                time.sleep(delay)
            
            # Remove cursor
            final_content = f"[{theme['primary']}]{displayed_text}[/{theme['primary']}]"
            live.update(final_content)
            time.sleep(0.5)

# Global theme manager instance
theme_manager = ThemeManager()

def get_current_theme():
    """Get the current theme configuration."""
    return theme_manager.get_theme()

def set_theme(theme_name: str) -> bool:
    """Set the global theme."""
    return theme_manager.set_theme(theme_name)

def create_themed_panel(content: str, title: str = "") -> Panel:
    """Create a panel with current theme."""
    return theme_manager.create_themed_panel(content, title)

def show_loading_animation(message: str = "Loading", duration: float = 2.0):
    """Show loading animation with current theme."""
    theme_manager.animate_loading(message, duration)