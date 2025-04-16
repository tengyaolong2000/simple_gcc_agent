
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
        if key.lower() == "enter":
            key = "Return"
        cmd = f'xdotool key {key}'
        return docker_exec(cmd, WindowsTools.container_name)

    @staticmethod
    def type_text(text: str):
        """Simulate typing text."""
        # Escape all special characters in the text
        #text = text.replace('"', '\"')

        cmd = f'xdotool type "{text}"'
        print(cmd.replace("'", "'\\''"))
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
    def left_click_at(x: int, y: int):
        """Simulate a mouse left click at the specified coordinates."""
        cmd = f'xdotool mousemove {x} {y} click 1'
        return docker_exec(cmd, WindowsTools.container_name)
    
    @staticmethod
    def right_click_at(x: int, y: int):
        """Simulate a mouse right click at the specified coordinates."""
        cmd = f'xdotool mousemove {x} {y} click 3'
        return docker_exec(cmd, WindowsTools.container_name)


if __name__ == "__main__":
    # Type the command char by char safely
    WindowsTools.type_text("mkdir 'hello world'")
    #WindowsTools.press_key(key="Enter")