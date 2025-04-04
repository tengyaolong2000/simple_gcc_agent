from tools_raw.firefox_tools import FirefoxTools
from smolagents import tool

fox_tools = FirefoxTools(display=":99", container_name="cua-image")

@tool
def open_firefox() -> None:
    """
    Opens Firefox in the VM.
    """
    fox_tools.open_firefox()

@tool
def click(x: int, y: int) -> None:
    """
    Simulates a mouse click at the specified coordinates.
    
    Args:
        x: X-coordinate for the click.
        y: Y-coordinate for the click.
    """
    fox_tools.click(x, y)

@tool
def search_in_firefox(text: str) -> None:
    """
    Searches for the given text in Firefox.
   
    Args:
        text: The text to search for.

    """
    fox_tools.search_in_firefox(text)

@tool
def select_option_by_index(index: int) -> None:
    """
    Select an option from Firefox's suggestion list after a search (also works with dropdowns).
    This method presses the Down arrow key 'index' times and then hits Enter.
    For example, index=1 selects the first suggestion.
    
    Args:
        index: The index of the option to select.
    """
    return fox_tools.select_option_by_index(index)

@tool
def press_key_combo(keys: list[str]) -> None:
    """
    Simulates pressing a combination of keys. To press enter, use 'Return'.
    
    Args:
        keys: List of keys to press.
    """
    return fox_tools.press_key_combo(keys)

@tool
def scroll_down(num_pixels: int = 1200) -> None:
    """
    Scrolls down the page by a specified number of pixels.
    
    Args:
        num_pixels: Number of pixels to scroll down.
    """
    return fox_tools.scroll_down(num_pixels)

@tool
def scroll_up(num_pixels: int = 1200) -> None:
    """
    Scrolls up the page by a specified number of pixels.
    
    Args:
        num_pixels: Number of pixels to scroll up.
    """
    return fox_tools.scroll_up(num_pixels)

@tool
def switch_tab() -> None:
    """
    Switches to the next tab in Firefox.
    """
    return fox_tools.switch_tab()

@tool
def type_text(text: str) -> None:
    """
    Types the given text. Remember to select the location you want to type first.
    
    Args:
        text: The text to type.
    """
    return fox_tools.type_text(text)

@tool
def close_window() -> None:
    """
    Closes the current window.
    """
    return fox_tools.close_window()

@tool
def press_key(key: str) -> None:
    """
    Simulates pressing a specific key.
    
    Args:
        key: The key to press.
    """
    return fox_tools.press_key(key)

@tool
def focus_address_bar() -> None:
    """
    Focuses on the address bar in Firefox.
    """
    return fox_tools.focus_address_bar()

@tool
def open_terminal() -> None:
    """
    Opens a terminal emulator in the VM.
    """
    return fox_tools.open_terminal()
