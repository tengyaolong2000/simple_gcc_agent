from tools_raw.chromium_tools import ChromiumTools
from smolagents import tool


@tool
def navigate_to_url(url: str) -> None:
    """
    Navigate to a specified URL in the Chromium browser.

    Args:
        url: The URL to navigate to.
    """
    ChromiumTools.navigate_to_url(url)

@tool
def type_text(selector: str, text: str) -> None:
    """
    Type text into an input field in the Chromium browser.

    Args:
        selector: The CSS selector of the input field.
        text: The text to type.
    """
    ChromiumTools.type_text(selector, text)

@tool
def click_element(selector: str) -> None:
    """
    Click an element in the Chromium browser.

    Args:
        selector: The CSS selector of the element to click.
    """
    ChromiumTools.click_element(selector)

@tool
def press_key(key: str) -> None:
    """
    Simulate a key press in the Chromium browser.

    Args:
        key: The key to press (e.g., "Enter", "ArrowDown").
    """
    ChromiumTools.press_key(key)

@tool
def press_key_combo(key1: str, key2: str) -> None:
    """
    Simulate pressing a combination of two keys in the Chromium browser.

    Args:
        key1: The first key to press.
        key2: The second key to press.
    """
    ChromiumTools.press_key_combination(key1, key2)

@tool
def scroll_page(x: int = 0, y: int = 0, behavior: str = 'auto') -> None:
    """
    Scroll the page in the Chromium browser.

    Args:
        x: The horizontal scroll offset.
        y: The vertical scroll offset.
        behavior: The scroll behavior ('auto' or 'smooth').
    """
    ChromiumTools.scroll_page(x, y, behavior)

@tool
def clear_text(selector: str) -> None:
    """
    Clear text in an input field in the Chromium browser.

    Args:
        selector: The CSS selector of the input field.
    """
    ChromiumTools.clear_text(selector)

@tool
def click_by_text(text: str) -> None:
    """
    Click an element in the Chromium browser by its visible text.

    Args:
        text: The visible text of the element to click.
    """
    ChromiumTools.click_by_text(text)

@tool
def initialize_browser() -> None:
    """
    Initialize the Chromium browser.
    """
    ChromiumTools.initialize_browser()

@tool
def close_popup() -> None:
    """
    Close any pop-up in the Chromium browser.
    """
    ChromiumTools.close_popup()