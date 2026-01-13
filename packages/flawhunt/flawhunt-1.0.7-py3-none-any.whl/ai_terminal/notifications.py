import os
import platform
import subprocess


def notify(title: str, message: str) -> None:
    """Show a native popup notification where possible.

    - macOS: uses AppleScript `display notification`
    - Linux: tries `notify-send` if available
    - Windows: prints to console (avoid extra deps)
    """
    system = platform.system().lower()

    try:
        if system == "darwin":
            # macOS system notification via AppleScript
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system == "linux":
            # Use notify-send if available
            if shutil_which("notify-send"):
                subprocess.run(["notify-send", title, message], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                print(f"[Notification] {title}: {message}")
        else:
            # Fallback: console output
            print(f"[Notification] {title}: {message}")
    except Exception:
        # Silent failure to avoid interrupting CLI operations
        pass


def shutil_which(bin_name: str):
    try:
        from shutil import which
        return which(bin_name)
    except Exception:
        return None