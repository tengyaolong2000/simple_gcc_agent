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
    - doubleClick
    - type
    - keypress
    - scroll
    - drag
    - move
    - wait
    - function, where
        - "goto": Navigates to a specific URL if provided in the arguments. It also updates the client's URL afterward.
        - "back": Goes back to the previous page in the browser's history and updates the client's URL.
        - "forward": Goes forward in the browser's history and updates the client's URL.
        - "reload": Reloads the current page and updates the client's URL.

        To call the "function" action in the code, you need to format it with the required name of the function and any arguments it needs. Here's some example structures:

{
  type: "function",
  name: "goto", // Replace with the desired function name ("goto", "back", "forward", "reload")
  arguments: {
    url: "https://example.com" // For "goto", provide the target URL
  }
}

{
  type: "function",
  name: "forward"
}

        - Make sure to replace name and arguments with the appropriate values based on the action you want to perform. If the function is unsupported, the system will return an error message.

    Args:
        action: The described string action to perform.
    """
    StagehandTools.perform_action(action)
