"""
Audio files monitoring handlers.

This module contains Classes and Methods to deal with 
watchdog library events.
"""

from pathlib import Path
from typing import Tuple

from watchdog.events import FileSystemEventHandler


class AudioFileHandler(FileSystemEventHandler):
    """
    Implements watchdog FileSystemEventHandler class
    for Anki compatible audio file detection and management.
    """
    def __init__(self, audio_extensions: Tuple[str, ...]) -> None:
        self._allowed_extensions = audio_extensions
        self.caught_file = None
    
    def on_moved(self, event):
        extension = Path(event.dest_path).suffix
        if extension in self._allowed_extensions:
            self.caught_file = event.dest_path