"""
Advanced progress bar system with themed styling and animations.
"""

import time
import threading
from typing import Optional, Callable, Any
from rich.console import Console
from rich.progress import Progress, TaskID, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box

class ThemedProgressBar:
    """A themed progress bar with customizable styling."""
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self.console = Console()
        self._active_progress = None
        self._active_task = None
        
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
    
    def create_progress_bar(self, description: str = "Processing", show_spinner: bool = True):
        """Create a themed progress bar."""
        colors = self.get_theme_colors()
        
        columns = []
        if show_spinner:
            columns.append(SpinnerColumn(spinner_style=colors['accent']))
        
        columns.extend([
            TextColumn("[bold]{task.description}"),
            BarColumn(
                bar_width=40,
                complete_style=colors['success'],
                finished_style=colors['primary']
            ),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn()
        ])
        
        progress = Progress(*columns, console=self.console)
        task = progress.add_task(description, total=100)
        
        return progress, task
    
    def show_loading_animation(self, message: str = "Loading", duration: float = 3.0):
        """Show a loading animation with themed styling."""
        colors = self.get_theme_colors()
        
        with Progress(
            SpinnerColumn(),
            TextColumn(f"[{colors['primary']}]{message}..."),
            console=self.console
        ) as progress:
            task = progress.add_task("loading", total=None)
            time.sleep(duration)
    
    def show_file_transfer(self, filename: str, total_size: int, chunk_size: int = 1024):
        """Simulate file transfer with progress bar."""
        colors = self.get_theme_colors()
        
        with Progress(
            TextColumn("[bold blue]Transferring"),
            TextColumn("[bold]{task.fields[filename]}"),
            BarColumn(bar_width=40, complete_style=colors['success']),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("•"),
            TextColumn("[progress.filesize]{task.completed}/{task.total}"),
            TextColumn("•"),
            TextColumn("[progress.rate]{task.speed}"),
            TimeRemainingColumn(),
            console=self.console
        ) as progress:
            task = progress.add_task("transfer", filename=filename, total=total_size)
            
            transferred = 0
            while transferred < total_size:
                chunk = min(chunk_size, total_size - transferred)
                transferred += chunk
                progress.update(task, completed=transferred)
                time.sleep(0.01)  # Simulate transfer delay
    
    def show_system_scan(self, targets: list, scan_duration: float = 0.5):
        """Show system scanning progress."""
        colors = self.get_theme_colors()
        
        with Progress(
            SpinnerColumn(spinner_style=colors['accent']),
            TextColumn("[bold]Scanning"),
            TextColumn("[bold]{task.fields[target]}"),
            BarColumn(bar_width=30, complete_style=colors['warning']),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            for target in targets:
                task = progress.add_task("scan", target=target, total=100)
                
                for i in range(0, 101, 10):
                    progress.update(task, completed=i)
                    time.sleep(scan_duration / 10)
                
                # Show completion
                progress.update(task, completed=100)
                time.sleep(0.2)
    
    def show_multi_task_progress(self, tasks: list):
        """Show multiple tasks running simultaneously."""
        colors = self.get_theme_colors()
        
        with Progress(
            TextColumn("[bold blue]Task"),
            TextColumn("[bold]{task.description}"),
            BarColumn(bar_width=30),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            task_ids = []
            for task_name in tasks:
                task_id = progress.add_task(task_name, total=100)
                task_ids.append(task_id)
            
            # Simulate tasks completing at different rates
            import random
            while not all(progress.tasks[tid].finished for tid in task_ids):
                for tid in task_ids:
                    if not progress.tasks[tid].finished:
                        increment = random.randint(1, 5)
                        progress.update(tid, advance=increment)
                time.sleep(0.1)
    
    def show_installation_progress(self, packages: list):
        """Show package installation progress."""
        colors = self.get_theme_colors()
        
        for package in packages:
            self.console.print(f"[{colors['primary']}]Installing {package}...[/{colors['primary']}]")
            
            with Progress(
                SpinnerColumn(spinner_style=colors['accent']),
                TextColumn("[bold]{task.description}"),
                BarColumn(bar_width=40, complete_style=colors['success']),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                console=self.console
            ) as progress:
                task = progress.add_task(f"Installing {package}", total=100)
                
                # Simulate installation phases
                phases = [
                    ("Downloading", 30),
                    ("Extracting", 20),
                    ("Configuring", 25),
                    ("Installing", 25)
                ]
                
                completed = 0
                for phase_name, phase_duration in phases:
                    progress.update(task, description=f"{phase_name} {package}")
                    for _ in range(phase_duration):
                        completed += 1
                        progress.update(task, completed=completed)
                        time.sleep(0.05)
            
            self.console.print(f"[{colors['success']}]✓ {package} installed successfully[/{colors['success']}]")
    
    def show_vulnerability_scan(self, targets: list):
        """Show vulnerability scanning progress."""
        colors = self.get_theme_colors()
        
        scan_table = Table(title="Vulnerability Scan Progress", box=box.ROUNDED)
        scan_table.add_column("Target", style=colors['primary'])
        scan_table.add_column("Status", style=colors['secondary'])
        scan_table.add_column("Vulnerabilities", style=colors['warning'])
        
        with Live(scan_table, console=self.console, refresh_per_second=4):
            for target in targets:
                # Simulate scanning
                scan_table.add_row(target, "[yellow]Scanning...", "")
                time.sleep(1)
                
                # Simulate results
                import random
                vuln_count = random.randint(0, 5)
                status_color = colors['success'] if vuln_count == 0 else colors['warning']
                status_text = "Clean" if vuln_count == 0 else "Issues Found"
                
                # Update the last row
                scan_table.rows[-1] = (
                    target,
                    f"[{status_color}]{status_text}[/{status_color}]",
                    str(vuln_count) if vuln_count > 0 else "None"
                )
                time.sleep(0.5)
    
    def show_network_discovery(self, network_range: str = "192.168.1.0/24"):
        """Show network discovery progress."""
        colors = self.get_theme_colors()
        
        self.console.print(Panel(
            f"[{colors['primary']}]Discovering devices on {network_range}[/{colors['primary']}]",
            border_style=colors['border']
        ))
        
        discovered_devices = []
        
        with Progress(
            SpinnerColumn(spinner_style=colors['accent']),
            TextColumn("[bold]Scanning IP"),
            TextColumn("[bold]{task.fields[current_ip]}"),
            BarColumn(bar_width=30, complete_style=colors['success']),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("discovery", current_ip="", total=254)
            
            for i in range(1, 255):
                current_ip = f"192.168.1.{i}"
                progress.update(task, current_ip=current_ip, completed=i)
                
                # Simulate device discovery
                import random
                if random.random() < 0.1:  # 10% chance of finding a device
                    device_type = random.choice(["Router", "Computer", "Phone", "IoT Device"])
                    discovered_devices.append((current_ip, device_type))
                
                time.sleep(0.02)
        
        # Show discovered devices
        if discovered_devices:
            device_table = Table(title="Discovered Devices", box=box.ROUNDED)
            device_table.add_column("IP Address", style=colors['primary'])
            device_table.add_column("Device Type", style=colors['secondary'])
            
            for ip, device_type in discovered_devices:
                device_table.add_row(ip, device_type)
            
            self.console.print(device_table)
        else:
            self.console.print(f"[{colors['warning']}]No devices discovered[/{colors['warning']}]")

class ProgressBarManager:
    """Manager for creating and controlling progress bars."""
    
    def __init__(self, theme_manager=None):
        self.theme_manager = theme_manager
        self.progress_bar = ThemedProgressBar(theme_manager)
    
    def loading(self, message: str = "Loading", duration: float = 3.0):
        """Show a loading animation."""
        self.progress_bar.show_loading_animation(message, duration)
    
    def file_transfer(self, filename: str, size_mb: float = 10.0):
        """Simulate file transfer."""
        total_bytes = int(size_mb * 1024 * 1024)
        self.progress_bar.show_file_transfer(filename, total_bytes)
    
    def system_scan(self, targets: list = None):
        """Show system scanning."""
        if targets is None:
            targets = ["127.0.0.1", "192.168.1.1", "10.0.0.1"]
        self.progress_bar.show_system_scan(targets)
    
    def multi_task(self, tasks: list = None):
        """Show multiple tasks."""
        if tasks is None:
            tasks = ["Analyzing", "Processing", "Validating", "Finalizing"]
        self.progress_bar.show_multi_task_progress(tasks)
    
    def install_packages(self, packages: list = None):
        """Show package installation."""
        if packages is None:
            packages = ["nmap", "wireshark", "metasploit"]
        self.progress_bar.show_installation_progress(packages)
    
    def vulnerability_scan(self, targets: list = None):
        """Show vulnerability scanning."""
        if targets is None:
            targets = ["web-server", "database", "api-endpoint", "file-server"]
        self.progress_bar.show_vulnerability_scan(targets)
    
    def network_discovery(self, network: str = "192.168.1.0/24"):
        """Show network discovery."""
        self.progress_bar.show_network_discovery(network)