from io import BytesIO
from PIL import Image

from typing import Union
import tempfile
import os

from smolagents import Tool
from utils.utils import docker_exec, VM


class WindowsTools:
    container_name = "gcc_agent-cua-vm-1"

    @staticmethod
    def close_window():
        """Close the current window (Alt+F4)."""
        cmd = 'xdotool key Alt+F4'
        return docker_exec(cmd, WindowsTools.container_name)

    @staticmethod
    def switch_tab():
        """Switch to the next tab (Ctrl+Tab)."""
        cmd = 'xdotool key ctrl+Tab'
        return docker_exec(cmd, WindowsTools.container_name)

    @staticmethod
    def drag_and_drop(start_x: int, start_y: int, end_x: int, end_y: int):
        """
        Simulate a drag-and-drop action from one coordinate to another.
        Moves to the start position, holds the left mouse button, moves to the end position, then releases.
        """
        cmd = (f'xdotool mousemove {start_x} {start_y} mousedown 1 '
               f'mousemove {end_x} {end_y} mouseup 1')
        return docker_exec(cmd, WindowsTools.container_name)

    @staticmethod
    def press_key(key: str):
        """Simulate pressing a specific key."""
        cmd = f'xdotool key {key}'
        return docker_exec(cmd, WindowsTools.container_name)

    @staticmethod
    def press_key_combo(keys: list[str]):
        """Simulate pressing a combination of keys."""
        cmd = '+'.join(keys)
        cmd = f'xdotool key {cmd}'
        return docker_exec(cmd, WindowsTools.container_name)

    @staticmethod
    def open_terminal():
        """Open a terminal emulator."""
        cmd = 'exo-open --launch TerminalEmulator &'
        return docker_exec(cmd, WindowsTools.container_name)

    @staticmethod
    def click_at(x: int, y: int):
        """Simulate a mouse click at the specified coordinates."""
        cmd = f'xdotool mousemove {x} {y} click 1'
        return docker_exec(cmd, WindowsTools.container_name)