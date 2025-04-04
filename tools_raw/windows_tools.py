from io import BytesIO
from PIL import Image

from typing import Union
import tempfile
import os

from smolagents import Tool
from utils.utils import docker_exec, VM



class Window_tools(VM):
    
    def __init__(self, display, container_name):
        super().__init__(display, container_name)
        self.display = display
        self.container_name = container_name    
    
    def close_window(self):
        """Close the current window (Alt+F4)."""
        cmd = 'xdotool key Alt+F4'
        return docker_exec(cmd, self.container_name)
    
    def switch_tab(self):
        """Switch to the next tab (Ctrl+Tab)."""
        cmd = 'xdotool key ctrl+Tab'
        return docker_exec(cmd, self.container_name)
    
    
    def drag_and_drop(self, start_x: int, start_y: int, end_x: int, end_y: int):
        """
        Simulate a drag-and-drop action from one coordinate to another.
        Moves to the start position, holds the left mouse button, moves to the end position, then releases.
        """
        cmd = (f'xdotool mousemove {start_x} {start_y} mousedown 1 '
               f'mousemove {end_x} {end_y} mouseup 1')
        return docker_exec(cmd, self.container_name)
    
    def press_key(self, key: str):
        """Simulate pressing a specific key."""
        cmd = f'xdotool key {key}'
        return docker_exec(cmd, self.container_name)
    
    def press_key_combo(self, keys: list[str]):
        """Simulate pressing a combination of keys."""
        cmd = '+'.join(keys)
        cmd = f'xdotool key {cmd}'
        return docker_exec(cmd, self.container_name)
    
    def open_terminal(self):
        """Open a terminal emulator."""
        cmd = 'exo-open --launch TerminalEmulator &'
        return docker_exec(cmd, self.container_name)
    
    def click_at(self, x: int, y: int):
        """Simulate a mouse click at the specified coordinates."""
        cmd = f'xdotool mousemove {x} {y} click 1'
        return docker_exec(cmd, self.container_name)