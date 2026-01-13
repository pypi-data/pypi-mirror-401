"""
Configuration management system for FlawHunt CLI.
Handles user preferences, themes, animations, and customization settings.
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
from rich.console import Console

@dataclass
class UIConfig:
    """UI-related configuration settings."""
    theme: str = "cyber_hunter"
    show_animations: bool = True
    animation_speed: float = 1.0
    show_ascii_art: bool = True
    show_loading_effects: bool = True
    typewriter_speed: float = 0.05
    matrix_rain_duration: float = 5.0
    glitch_intensity: int = 3
    show_boot_sequence: bool = True
    custom_banner: Optional[str] = None

@dataclass
class TerminalConfig:
    """Terminal behavior configuration."""
    safe_mode: bool = True
    verbose: bool = False
    auto_confirm_safe_commands: bool = False
    command_history_size: int = 1000
    show_command_explanations: bool = True
    enable_autocomplete: bool = True
    show_platform_info: bool = True
    max_output_lines: int = 100

@dataclass
class SecurityConfig:
    """Security-related configuration."""
    block_dangerous_commands: bool = True
    require_confirmation: bool = True
    log_all_commands: bool = True
    enable_sandbox_mode: bool = False
    allowed_networks: List[str] = field(default_factory=lambda: ["127.0.0.1", "localhost"])
    blocked_commands: List[str] = field(default_factory=lambda: ["rm -rf", "format", "del /f"])

@dataclass
class AIConfig:
    """AI model and behavior configuration."""
    model: str = "moonshotai/kimi-k2-instruct-0905"
    provider: str = "groq"
    temperature: float = 0.7
    max_tokens: int = 2048
    enable_memory: bool = True
    memory_size: int = 50
    context_window: int = 10

@dataclass
class NotificationConfig:
    """Notification and sound configuration."""
    enable_sounds: bool = False
    sound_theme: str = "cyber"
    notification_level: str = "normal"  # minimal, normal, verbose
    show_progress_bars: bool = True
    show_status_indicators: bool = True

@dataclass
class BackupConfig:
    """Backup and webhook configuration."""
    webhook_url: str = "https://n8n.gamkers.in/webhook/chat-backup"
    import_list_webhook_url: str = "https://n8n.gamkers.in/webhook/chat-import-list"
    import_webhook_url: str = "https://n8n.gamkers.in/webhook/chat-import"
    enable_auto_backup: bool = False
    backup_frequency_hours: int = 24
    max_backup_size_mb: int = 50
    include_metadata: bool = True
    compress_backup: bool = True

@dataclass
class FlawHuntConfig:
    """Main configuration class containing all settings."""
    ui: UIConfig = field(default_factory=UIConfig)
    terminal: TerminalConfig = field(default_factory=TerminalConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    ai: AIConfig = field(default_factory=AIConfig)
    notifications: NotificationConfig = field(default_factory=NotificationConfig)
    backup: BackupConfig = field(default_factory=BackupConfig)
    version: str = "1.0.0"
    last_updated: Optional[str] = None

class ConfigManager:
    """Manages configuration loading, saving, and validation."""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = config_dir or Path.home() / ".ai_terminal"
        self.config_file = self.config_dir / "config.json"
        self.backup_file = self.config_dir / "config.backup.json"
        self.console = Console()
        
        # Ensure config directory exists
        self.config_dir.mkdir(exist_ok=True)
        
        # Load or create default config
        self.config = self.load_config()
    
    def load_config(self) -> FlawHuntConfig:
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Convert dict to config object
                config = FlawHuntConfig()
                
                if 'ui' in data:
                    config.ui = UIConfig(**data['ui'])
                if 'terminal' in data:
                    config.terminal = TerminalConfig(**data['terminal'])
                if 'security' in data:
                    config.security = SecurityConfig(**data['security'])
                if 'ai' in data:
                    config.ai = AIConfig(**data['ai'])
                if 'notifications' in data:
                    config.notifications = NotificationConfig(**data['notifications'])
                
                config.version = data.get('version', '1.0.0')
                
                # Auto-migrate model for version 1.0.7
                current_ver = config.version
                if current_ver < "1.0.7":
                    config.ai.model = "moonshotai/kimi-k2-instruct-0905"
                    config.version = "1.0.7"
                    # We will save this updated config back to disk in the main execution flow or upon next save
                
                config.last_updated = data.get('last_updated')
                
                return config
                
            except (json.JSONDecodeError, TypeError, KeyError) as e:
                self.console.print(f"[yellow]Warning: Config file corrupted, using defaults. Error: {e}[/yellow]")
                return FlawHuntConfig()
        
        return FlawHuntConfig()
    
    def save_config(self, backup: bool = True) -> bool:
        """Save current configuration to file."""
        try:
            # Create backup if requested
            if backup and self.config_file.exists():
                import shutil
                shutil.copy2(self.config_file, self.backup_file)
            
            # Update timestamp
            import datetime
            self.config.last_updated = datetime.datetime.now().isoformat()
            
            # Convert to dict and save
            config_dict = asdict(self.config)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            self.console.print(f"[red]Error saving config: {e}[/red]")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to default values."""
        try:
            # Backup current config
            if self.config_file.exists():
                import shutil
                backup_name = f"config.backup.{int(__import__('time').time())}.json"
                shutil.copy2(self.config_file, self.config_dir / backup_name)
            
            # Reset to defaults
            self.config = FlawHuntConfig()
            return self.save_config(backup=False)
            
        except Exception as e:
            self.console.print(f"[red]Error resetting config: {e}[/red]")
            return False
    
    def get_theme_config(self) -> Dict[str, Any]:
        """Get theme-related configuration."""
        return {
            'theme': self.config.ui.theme,
            'show_animations': self.config.ui.show_animations,
            'animation_speed': self.config.ui.animation_speed,
            'show_ascii_art': self.config.ui.show_ascii_art,
            'show_loading_effects': self.config.ui.show_loading_effects,
            'custom_banner': self.config.ui.custom_banner
        }
    
    def set_theme(self, theme_name: str) -> bool:
        """Set the UI theme."""
        valid_themes = [
            "cyber_hunter", "neon_purple", "ocean_blue", 
            "fire_red", "stealth_gray", "rainbow"
        ]
        
        if theme_name in valid_themes:
            self.config.ui.theme = theme_name
            return self.save_config()
        return False
    
    def toggle_animations(self) -> bool:
        """Toggle animation display."""
        self.config.ui.show_animations = not self.config.ui.show_animations
        return self.save_config()
    
    def set_animation_speed(self, speed: float) -> bool:
        """Set animation speed (0.1 to 3.0)."""
        if 0.1 <= speed <= 3.0:
            self.config.ui.animation_speed = speed
            return self.save_config()
        return False
    
    def toggle_safe_mode(self) -> bool:
        """Toggle safe mode."""
        self.config.terminal.safe_mode = not self.config.terminal.safe_mode
        return self.save_config()
    
    def toggle_verbose_mode(self) -> bool:
        """Toggle verbose mode."""
        self.config.terminal.verbose = not self.config.terminal.verbose
        return self.save_config()
    
    def set_ai_model(self, model: str, provider: str = None) -> bool:
        """Set AI model and optionally provider."""
        self.config.ai.model = model
        if provider:
            self.config.ai.provider = provider
        return self.save_config()
    
    def add_blocked_command(self, command: str) -> bool:
        """Add a command to the blocked list."""
        if command not in self.config.security.blocked_commands:
            self.config.security.blocked_commands.append(command)
            return self.save_config()
        return False
    
    def remove_blocked_command(self, command: str) -> bool:
        """Remove a command from the blocked list."""
        if command in self.config.security.blocked_commands:
            self.config.security.blocked_commands.remove(command)
            return self.save_config()
        return False
    
    def export_config(self, export_path: Path) -> bool:
        """Export configuration to a file."""
        try:
            config_dict = asdict(self.config)
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.console.print(f"[red]Error exporting config: {e}[/red]")
            return False
    
    def import_config(self, import_path: Path) -> bool:
        """Import configuration from a file."""
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Backup current config
            self.save_config()
            
            # Load new config
            old_config = self.config
            try:
                self.config = FlawHuntConfig()
                
                if 'ui' in data:
                    self.config.ui = UIConfig(**data['ui'])
                if 'terminal' in data:
                    self.config.terminal = TerminalConfig(**data['terminal'])
                if 'security' in data:
                    self.config.security = SecurityConfig(**data['security'])
                if 'ai' in data:
                    self.config.ai = AIConfig(**data['ai'])
                if 'notifications' in data:
                    self.config.notifications = NotificationConfig(**data['notifications'])
                
                return self.save_config()
                
            except Exception:
                # Restore old config on error
                self.config = old_config
                raise
                
        except Exception as e:
            self.console.print(f"[red]Error importing config: {e}[/red]")
            return False
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        # Validate UI config
        valid_themes = ["cyber_hunter", "neon_purple", "ocean_blue", "fire_red", "stealth_gray", "rainbow"]
        if self.config.ui.theme not in valid_themes:
            issues.append(f"Invalid theme: {self.config.ui.theme}")
        
        if not 0.1 <= self.config.ui.animation_speed <= 3.0:
            issues.append(f"Invalid animation speed: {self.config.ui.animation_speed}")
        
        # Validate AI config
        if not 0.0 <= self.config.ai.temperature <= 2.0:
            issues.append(f"Invalid AI temperature: {self.config.ai.temperature}")
        
        if self.config.ai.max_tokens < 100:
            issues.append(f"Max tokens too low: {self.config.ai.max_tokens}")
        
        # Validate security config
        if self.config.terminal.command_history_size < 10:
            issues.append(f"Command history size too low: {self.config.terminal.command_history_size}")
        
        return issues
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get a summary of current configuration."""
        return {
            "Theme": self.config.ui.theme,
            "Animations": "Enabled" if self.config.ui.show_animations else "Disabled",
            "Safe Mode": "Enabled" if self.config.terminal.safe_mode else "Disabled",
            "Verbose Mode": "Enabled" if self.config.terminal.verbose else "Disabled",
            "AI Model": f"{self.config.ai.provider}/{self.config.ai.model}",
            "Memory": "Enabled" if self.config.ai.enable_memory else "Disabled",
            "Sounds": "Enabled" if self.config.notifications.enable_sounds else "Disabled",
            "Backup Webhook": self.config.backup.webhook_url,
            "Auto Backup": "Enabled" if self.config.backup.enable_auto_backup else "Disabled",
            "Config File": str(self.config_file),
            "Last Updated": self.config.last_updated or "Never"
        }
    
    def set_backup_webhook_url(self, url: str) -> bool:
        """Set the backup webhook URL."""
        try:
            self.config.backup.webhook_url = url
            return self.save_config()
        except Exception as e:
            self.console.print(f"[red]Error setting webhook URL: {e}[/red]")
            return False
    
    def toggle_auto_backup(self) -> bool:
        """Toggle automatic backup."""
        self.config.backup.enable_auto_backup = not self.config.backup.enable_auto_backup
        return self.save_config()
    
    def set_backup_frequency(self, hours: int) -> bool:
        """Set backup frequency in hours."""
        if hours < 1:
            self.console.print("[red]Backup frequency must be at least 1 hour[/red]")
            return False
        try:
            self.config.backup.backup_frequency_hours = hours
            return self.save_config()
        except Exception as e:
            self.console.print(f"[red]Error setting backup frequency: {e}[/red]")
            return False

# Global config manager instance
config_manager = ConfigManager()

def get_config() -> FlawHuntConfig:
    """Get the current configuration."""
    return config_manager.config

def save_config() -> bool:
    """Save the current configuration."""
    return config_manager.save_config()

def set_theme(theme_name: str) -> bool:
    """Set the UI theme."""
    return config_manager.set_theme(theme_name)

def toggle_animations() -> bool:
    """Toggle animations."""
    return config_manager.toggle_animations()

def get_theme_config() -> Dict[str, Any]:
    """Get theme configuration."""
    return config_manager.get_theme_config()