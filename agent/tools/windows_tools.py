from tools_raw.windows_tools import WindowsTools
from smolagents import tool

@tool
def close_window() -> None:
    """
    Close the current window (Alt+F4).
    """
    WindowsTools.close_window()

@tool
def switch_tab() -> None:
    """
    Switch to the next tab (Ctrl+Tab).
    """
    WindowsTools.switch_tab()

@tool
def drag_and_drop(start_x: int, start_y: int, end_x: int, end_y: int) -> None:
    """
    Simulate a drag-and-drop action from one coordinate to another.
    Moves to the start position, holds the left mouse button, moves to the end position, then releases.

    Args:
        start_x: The starting x-coordinate.
        start_y: The starting y-coordinate.
        end_x: The ending x-coordinate.
        end_y: The ending y-coordinate.
    """
    WindowsTools.drag_and_drop(start_x, start_y, end_x, end_y)

@tool
def press_key_system(key: str) -> None:
    """
    Simulate pressing a specific key at the system level..
    
    Args:
        key: The key to press.
    """
    WindowsTools.press_key(key)

@tool
def press_key_combo_system(keys: list[str]) -> None:
    """
    Simulate pressing a combination of keys at the system-wide level.
    
    Args:
        keys: List of keys to press.
    """
    WindowsTools.press_key_combo(keys)

@tool
def open_terminal() -> None:
    """
    Open a terminal emulator.
    """
    WindowsTools.open_terminal()

@tool
def left_click_at(x: int, y: int) -> None:
    """
    Simulate a mouse click at the specified coordinates.
    
    Args:
        x: The x-coordinate.
        y: The y-coordinate.
    """
    WindowsTools.left_click_at(x, y)

@tool
def right_click_at(x: int, y: int) -> None:
    """
    Simulate a right mouse click at the specified coordinates.
    
    Args:
        x: The x-coordinate.
        y: The y-coordinate.
    """
    WindowsTools.right_click_at(x, y)

@tool
def type_text(text: str) -> None:
    """
    Simulate typing text.
    
    Args:
        text: The text to type.
    """
    WindowsTools.type_text(text)

