"""
License validation module for FlawHunt CLI.
Handles license key storage, MAC address detection, and validation.
"""
import os
import json
import uuid
import platform
import subprocess
import requests
from pathlib import Path
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel

console = Console()

class LicenseManager:
    """Manages license validation and storage."""
    
    def __init__(self):
        self.config_dir = Path.home() / ".ai_terminal"
        self.config_dir.mkdir(exist_ok=True)
        self.license_file = self.config_dir / "license_key.txt"
        self.device_file = self.config_dir / "device_info.json"
        self.validation_url = "https://n8n.gamkers.in/webhook/validate-license"
        # Check license every 24 hours
        self.validation_interval = timedelta(hours=24)
    
    def parse_expiry_date(self, expires_at):
        """Parse expiry date from various formats."""
        if not expires_at:
            return None
        
        # Try ISO 8601 format first (most common for APIs)
        try:
            from datetime import datetime
            # Handle ISO 8601 with timezone info
            expires_str = str(expires_at)
            if expires_str.endswith('+00:00'):
                expires_str = expires_str[:-6] + 'Z'
            elif '+' in expires_str and expires_str.count(':') >= 3:
                # Remove timezone offset for parsing
                expires_str = expires_str.split('+')[0]
            
            # Try parsing ISO format with fromisoformat (Python 3.7+)
            try:
                if expires_str.endswith('Z'):
                    expires_str = expires_str[:-1]
                return datetime.fromisoformat(expires_str)
            except (ValueError, AttributeError):
                pass
        except Exception:
            pass
        
        # Common date formats to try
        date_formats = [
            "%Y-%m-%dT%H:%M:%S.%f",     # 2024-12-31T23:59:59.123456
            "%Y-%m-%dT%H:%M:%S.%fZ",    # 2024-12-31T23:59:59.123456Z
            "%Y-%m-%dT%H:%M:%S",        # 2024-12-31T23:59:59
            "%Y-%m-%dT%H:%M:%SZ",       # 2024-12-31T23:59:59Z
            "%Y-%m-%d",                 # 2024-12-31
            "%Y-%m-%d %H:%M:%S",        # 2024-12-31 23:59:59
            "%d/%m/%Y",                 # 31/12/2024
            "%m/%d/%Y",                 # 12/31/2024
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(str(expires_at), fmt)
            except ValueError:
                continue
        
        # If no format matches, try to parse as timestamp
        try:
            return datetime.fromtimestamp(float(expires_at))
        except (ValueError, TypeError):
            console.print(f"[yellow]Warning: Could not parse expiry date: {expires_at}[/yellow]")
            return None
    
    def is_license_expired(self, expires_at):
        """Check if license has expired."""
        if not expires_at:
            return False  # No expiry date means no expiry
        
        expiry_date = self.parse_expiry_date(expires_at)
        if not expiry_date:
            return False  # Could not parse, assume not expired
        
        return datetime.now() > expiry_date
    
    def days_until_expiry(self, expires_at):
        """Calculate days until license expires."""
        if not expires_at:
            return None
        
        expiry_date = self.parse_expiry_date(expires_at)
        if not expiry_date:
            return None
        
        delta = expiry_date - datetime.now()
        return delta.days
    
    def should_revalidate(self, device_info):
        """Check if license should be revalidated with server."""
        if not device_info:
            return True
        
        # Check if last validation was more than validation_interval ago
        last_validation = device_info.get("last_validation")
        if last_validation:
            try:
                last_validation_date = datetime.fromisoformat(last_validation)
                if datetime.now() - last_validation_date > self.validation_interval:
                    return True
            except ValueError:
                return True  # Invalid date format, revalidate
        else:
            return True  # No last validation date, revalidate
        
        # Check if license is close to expiry (within 7 days)
        validation_result = device_info.get("validation_result", {})
        expires_at = validation_result.get("expires_at")
        if expires_at:
            days_left = self.days_until_expiry(expires_at)
            if days_left is not None and days_left <= 7:
                return True  # Revalidate if expiring soon
        
        return False
    
    def is_guest_user(self):
        """Check if current user is a guest user."""
        license_key = self.load_license_key()
        device_info = self.load_device_info()
        return license_key == "guest" and device_info and device_info.get("guest_access")
    
    def get_mac_address(self):
        """Get the MAC address of the current device."""
        try:
            # Get MAC address using uuid.getnode()
            mac = uuid.getnode()
            mac_address = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
            return mac_address
        except Exception as e:
            console.print(f"[red]Error getting MAC address: {e}[/red]")
            return None
    
    def get_device_name(self):
        """Get a friendly device name."""
        try:
            system = platform.system()
            if system == "Darwin":  # macOS
                try:
                    result = subprocess.run(['scutil', '--get', 'ComputerName'], 
                                          capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        return result.stdout.strip()
                except:
                    pass
                return f"Mac ({platform.node()})"
            elif system == "Linux":
                return f"Linux ({platform.node()})"
            elif system == "Windows":
                return f"Windows ({platform.node()})"
            else:
                return f"{system} ({platform.node()})"
        except Exception:
            return "Unknown Device"
    
    def load_license_key(self):
        """Load license key from storage."""
        if self.license_file.exists():
            try:
                with open(self.license_file, 'r') as f:
                    return f.read().strip()
            except Exception as e:
                console.print(f"[red]Error reading license key: {e}[/red]")
        return None
    
    def save_license_key(self, license_key):
        """Save license key to storage."""
        try:
            with open(self.license_file, 'w') as f:
                f.write(license_key)
            return True
        except Exception as e:
            console.print(f"[red]Error saving license key: {e}[/red]")
            return False
    
    def load_device_info(self):
        """Load device information from storage."""
        if self.device_file.exists():
            try:
                with open(self.device_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                console.print(f"[red]Error reading device info: {e}[/red]")
        return None
    
    def save_device_info(self, device_info):
        """Save device information to storage."""
        try:
            with open(self.device_file, 'w') as f:
                json.dump(device_info, f, indent=2)
            return True
        except Exception as e:
            console.print(f"[red]Error saving device info: {e}[/red]")
            return False
    
    def validate_license(self, license_key, mac_address, device_name):
        """Validate license key with the server."""
        try:
            payload = {
                "license_key": license_key,
                "mac_address": mac_address,
                "device_name": device_name
            }
            
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                self.validation_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return True, data
                except json.JSONDecodeError:
                    return False, {"error": "Invalid response format"}
            else:
                try:
                    error_data = response.json()
                    return False, error_data
                except json.JSONDecodeError:
                    return False, {"error": f"HTTP {response.status_code}: {response.text}"}
                    
        except requests.exceptions.Timeout:
            return False, {"error": "License validation timed out. Please check your internet connection."}
        except requests.exceptions.ConnectionError:
            return False, {"error": "Cannot connect to license server. Please check your internet connection."}
        except Exception as e:
            return False, {"error": f"License validation failed: {str(e)}"}
    
    def prompt_for_license(self):
        """Prompt user for license key or guest sign-in."""
        console.print(Panel(
            "FlawHunt CLI License Required\n\n"
            "Please enter your FlawHunt CLI license key.\n"
            "Get the license key at flawhunt.gamkers.in\n"
            "License keys are in the format: FH-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX\n\n"
            "Or type 'guest' to sign in as a guest user with limited features.\n"
            "If you don't have a license key, please contact support.",
            title="License Key Required",
            border_style="yellow"
        ))
        
        try:
            user_input = input("License Key (or 'guest'): ").strip()
            if not user_input:
                console.print("[red]License key is required to use FlawHunt CLI.[/red]")
                return None
            return user_input.lower() if user_input.lower() == 'guest' else user_input.strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[red]License setup cancelled.[/red]")
            return None
    
    def setup_license(self):
        """Setup and validate license on first run or when license is missing."""
        # Check for existing license
        license_key = self.load_license_key()
        
        if not license_key:
            license_key = self.prompt_for_license()
            if not license_key:
                return False, "License key is required"
            
            # Handle guest sign-in
            if license_key.lower() == 'guest':
                return self.setup_guest_access()
        
        # Get device information
        mac_address = self.get_mac_address()
        if not mac_address:
            return False, "Could not determine device MAC address"
        
        device_name = self.get_device_name()
        
        # Validate license
        console.print("[yellow]Validating license...[/yellow]")
        success, result = self.validate_license(license_key, mac_address, device_name)
        
        if success:
            # Save license key and device info
            self.save_license_key(license_key)
            device_info = {
                "mac_address": mac_address,
                "device_name": device_name,
                "license_key": license_key,
                "validation_result": result,
                "last_validation": datetime.now().isoformat()
            }
            self.save_device_info(device_info)
            
            console.print("[green]✓ License validated successfully![/green]")
            
            # Display license information and expiry warnings
            if isinstance(result, dict):
                if "plan_type" in result:
                    console.print(f"[cyan]Plan: {result['plan_type'].title()}[/cyan]")
                if "expires_at" in result:
                    expires_at = result["expires_at"]
                    console.print(f"[cyan]Expires: {expires_at}[/cyan]")
                    
                    # Check if license is expiring soon
                    days_left = self.days_until_expiry(expires_at)
                    if days_left is not None:
                        if days_left <= 0:
                            console.print("[red]⚠️  License has expired![/red]")
                        elif days_left <= 7:
                            console.print(f"[yellow]⚠️  License expires in {days_left} days![/yellow]")
                        elif days_left <= 30:
                            console.print(f"[dim yellow]License expires in {days_left} days[/dim yellow]")
                if "device_name" in result:
                    console.print(f"[cyan]Device: {result['device_name']}[/cyan]")
            
            return True, "License validated successfully"
        else:
            error_msg = result.get("error", "Unknown validation error") if isinstance(result, dict) else str(result)
            console.print(f"[red]✗ License validation failed: {error_msg}[/red]")
            
            # If license key was just entered, don't save it
            if not self.load_license_key():
                console.print("[yellow]Please check your license key and try again.[/yellow]")
            else:
                # Existing license failed, might need to re-enter
                console.print("[yellow]Your saved license key is invalid. Please enter a new one.[/yellow]")
                # Remove invalid license
                if self.license_file.exists():
                    self.license_file.unlink()
            
            return False, error_msg
    
    def setup_guest_access(self):
        """Setup guest access with limited features."""
        console.print(Panel(
            "Guest Access Enabled\n\n"
            "You are now signed in as a guest user.\n"
            "Guest access provides limited functionality:\n"
            "• Basic command generation and explanations\n"
            "• Limited cybersecurity tool access\n"
            "• No cloud backup features\n"
            "• Session-only conversation history\n\n"
            "To unlock full features, please purchase a license key.",
            title="Guest Access",
            border_style="cyan"
        ))
        
        # Save guest access information
        device_info = {
            "mac_address": "guest",
            "device_name": "Guest User",
            "license_key": "guest",
            "validation_result": {
                "plan_type": "guest",
                "expires_at": None,
                "guest_access": True
            },
            "last_validation": datetime.now().isoformat(),
            "guest_access": True
        }
        
        # Save guest license key
        self.save_license_key("guest")
        self.save_device_info(device_info)
        
        console.print("[green]✓ Guest access setup complete![/green]")
        console.print("[dim]Note: Some features may be limited in guest mode.[/dim]")
        
        return True, "Guest access enabled"
    
    def check_license(self):
        """Check if license is valid and setup if needed."""
        license_key = self.load_license_key()
        device_info = self.load_device_info()
        
        # Handle guest access
        if license_key == "guest" and device_info and device_info.get("guest_access"):
            console.print("[cyan]✓ Guest access validated[/cyan]")
            console.print("[dim]Plan: Guest (Limited Features)[/dim]")
            return True
        
        if not license_key or not device_info:
            # No license found, setup required
            success, message = self.setup_license()
            return success
        
        # Validate MAC address matches (skip for guest)
        if license_key != "guest":
            current_mac = self.get_mac_address()
            if current_mac != device_info.get("mac_address"):
                console.print("[red]Device MAC address mismatch. License validation required.[/red]")
                success, message = self.setup_license()
                return success
        
        # Check if license has expired (skip for guest)
        validation_result = device_info.get("validation_result", {})
        expires_at = validation_result.get("expires_at")
        if expires_at and self.is_license_expired(expires_at):
            console.print("[red]⚠️  License has expired! Please renew your license.[/red]")
            # Remove expired license and prompt for new one
            if self.license_file.exists():
                self.license_file.unlink()
            if self.device_file.exists():
                self.device_file.unlink()
            success, message = self.setup_license()
            return success
        
        # Check if we should revalidate with server (skip for guest)
        if license_key != "guest" and self.should_revalidate(device_info):
            console.print("[yellow]Revalidating license with server...[/yellow]")
            mac_address = self.get_mac_address()
            device_name = self.get_device_name()
            
            success, result = self.validate_license(license_key, mac_address, device_name)
            if success:
                # Update device info with new validation result
                device_info["validation_result"] = result
                device_info["last_validation"] = datetime.now().isoformat()
                self.save_device_info(device_info)
                console.print("[green]✓ License revalidated successfully[/green]")
                
                # Check for expiry warnings after revalidation
                new_expires_at = result.get("expires_at") if isinstance(result, dict) else None
                if new_expires_at:
                    days_left = self.days_until_expiry(new_expires_at)
                    if days_left is not None:
                        if days_left <= 0:
                            console.print("[red]⚠️  License has expired![/red]")
                            return False
                        elif days_left <= 7:
                            console.print(f"[yellow]⚠️  License expires in {days_left} days![/yellow]")
                        elif days_left <= 30:
                            console.print(f"[dim yellow]License expires in {days_left} days[/dim yellow]")
            else:
                console.print("[red]License revalidation failed. Please check your license.[/red]")
                # Remove invalid license and prompt for new one
                if self.license_file.exists():
                    self.license_file.unlink()
                if self.device_file.exists():
                    self.device_file.unlink()
                success, message = self.setup_license()
                return success
        else:
            if license_key == "guest":
                console.print("[green]✓ Guest access validated[/green]")
            else:
                console.print("[green]✓ License validated[/green]")
            
            # Show expiry warnings for cached license
            if expires_at:
                days_left = self.days_until_expiry(expires_at)
                if days_left is not None:
                    if days_left <= 7:
                        console.print(f"[yellow]⚠️  License expires in {days_left} days![/yellow]")
                    elif days_left <= 30:
                        console.print(f"[dim yellow]License expires in {days_left} days[/dim yellow]")
        
        # Display license info if available
        if isinstance(validation_result, dict):
            if "plan_type" in validation_result:
                console.print(f"[dim]Plan: {validation_result['plan_type'].title()}[/dim]")
            if "expires_at" in validation_result:
                console.print(f"[dim]Expires: {validation_result['expires_at']}[/dim]")
        
        return True