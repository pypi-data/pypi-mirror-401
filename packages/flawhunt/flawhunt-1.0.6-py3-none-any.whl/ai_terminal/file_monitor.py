from pathlib import Path
from typing import Optional
import threading

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
except Exception:
    Observer = None
    FileSystemEventHandler = object  # type: ignore
    FileSystemEvent = object  # type: ignore

from .notifications import notify


class _Handler(FileSystemEventHandler):
    def __init__(self, base_dir: Path):
        super().__init__()
        self.base_dir = base_dir

    def on_created(self, event: FileSystemEvent):
        try:
            if getattr(event, "is_directory", False):
                return
            notify("File Created", Path(event.src_path).name)
        except Exception:
            pass

    def on_modified(self, event: FileSystemEvent):
        try:
            if getattr(event, "is_directory", False):
                return
            notify("File Modified", Path(event.src_path).name)
        except Exception:
            pass

    def on_deleted(self, event: FileSystemEvent):
        try:
            if getattr(event, "is_directory", False):
                return
            notify("File Deleted", Path(event.src_path).name)
        except Exception:
            pass

    def on_moved(self, event: FileSystemEvent):
        try:
            if getattr(event, "is_directory", False):
                return
            notify("File Renamed", f"{Path(event.src_path).name} → {Path(event.dest_path).name}")
        except Exception:
            pass


class FileMonitor:
    def __init__(self, directory: Path):
        self.directory = directory
        self.observer: Optional[Observer] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        # File monitoring disabled by user request
        return
        if Observer is None:
            return
        handler = _Handler(self.directory)
        self.observer = Observer()
        self.observer.schedule(handler, str(self.directory), recursive=True)
        self.observer.start()

    def stop(self) -> None:
        try:
            if self.observer:
                self.observer.stop()
                self.observer.join(timeout=2)
        except Exception:
            pass


def start_file_monitor(directory: Path) -> FileMonitor:
    """Start a watchdog observer for the provided directory."""
    monitor = FileMonitor(directory)
    monitor.start()
    return monitor