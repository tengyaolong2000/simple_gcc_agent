from tools_raw.stagehand_tools import StagehandTools
from smolagents import tool

@tool
def initialize_stagehand() -> None:
    """
    Initialize the Stagehand browser (Chromium).
    """
    StagehandTools.initialize()

@tool
def navigate_stagehand(url: str) -> None:
    """
    Navigate to a specified URL in the Stagehand browser.
    
    Args:
        url: The URL to navigate to.
    """
    StagehandTools.navigate(url)

@tool
def perform_action(action: str) -> None:
    """
    Perform a specified action described by string input in the Stagehand browser. Actions are mostly limited to:
    - Click
    - Type
    - Scroll
    - Next chunk
    - Prev chunk
        - If the user is asking to scroll to a position on the page, e.g., 'halfway' or 0.75, etc, you must return the argument formatted as the correct percentage, e.g., '50%' or '75%', etc.
        - If the user is asking to scroll to the next chunk/previous chunk, choose the nextChunk/prevChunk method. No arguments are required here.

    Args:
        action: The described string action to perform.
    """
    StagehandTools.perform_action(action)
