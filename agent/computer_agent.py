
from time import sleep

from dotenv import load_dotenv

from smolagents import CodeAgent, OpenAIServerModel
from smolagents.agents import ActionStep
from utils.utils import get_screenshot
from agent.tools import chromium_tools, firefox_tools, windows_tools

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from smolagents.models import ChatMessage
from smolagents import DuckDuckGoSearchTool, FinalAnswerTool
from typing import Any, Dict, List, Optional, Union
from smolagents.tools import Tool
import openai


load_dotenv()
import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

#sys.path.append(r"/Users/tengyaolong/Desktop/agent_stuff/personal_agent")


def save_screenshot(step_log: ActionStep, agent: CodeAgent) -> None:
    
    """Callback function to save a screenshot after each step."""

    sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
    current_step = step_log.step_number

    for step_logs in agent.memory.steps:  # Remove previous screenshots from logs for lean processing
        if isinstance(step_log, ActionStep) and step_log.step_number <= current_step - 2:
            step_logs.observations_images = None
            print(f"Removed previous screenshot from step {step_logs.step_number}")
        image = get_screenshot()
        print(f"Captured a browser screenshot: {image.size} pixels")
        step_log.observations_images = [image.copy()]  # Create a copy to ensure it persists, important!

    #check if the directory exists, if not create it
    if not os.path.exists("SCREENSHOTS"):
        print('creating directory')
        os.makedirs("SCREENSHOTS")

    # Save the screenshot to a file
    screenshot_path = f"SCREENSHOTS/screenshot_{current_step}"

    #log the observations to the same text file
    with open("observations.txt", "a") as f:
        print(f"Step {current_step}: {step_log.observations}")
        f.write(f"Step {current_step}: {step_log.observations}\n")
        if step_log.observations_images:
            print("images found")
            for img in step_log.observations_images:
                img.save(f"{screenshot_path}_{current_step}.png")
                f.write(f"Image saved: {screenshot_path}_{current_step}.png\n")

    return


class RetryingOpenAIServerModel(OpenAIServerModel):
    """
    Extension of OpenAIServerModel with retry/backoff logic for rate limits and transient errors.
    """

    @retry(
        reraise=True,
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((
            openai.RateLimitError,
            openai.APIConnectionError,
            openai.APIStatusError  # optional: depends on what errors you're seeing
        ))
    )
    def _call_with_retry(self, completion_kwargs):
        return self.client.chat.completions.create(**completion_kwargs)

    def __call__(
        self,
        messages: List[Dict[str, str]],
        stop_sequences: Optional[List[str]] = None,
        grammar: Optional[str] = None,
        tools_to_call_from: Optional[List[Tool]] = None,
        **kwargs,
    ) -> ChatMessage:
        completion_kwargs = self._prepare_completion_kwargs(
            messages=messages,
            stop_sequences=stop_sequences,
            grammar=grammar,
            tools_to_call_from=tools_to_call_from,
            model=self.model_id,
            custom_role_conversions=self.custom_role_conversions,
            convert_images_to_image_urls=True,
            **kwargs,
        )

        response = self._call_with_retry(completion_kwargs)

        self.last_input_token_count = response.usage.prompt_tokens
        self.last_output_token_count = response.usage.completion_tokens

        first_message = ChatMessage.from_dict(
            response.choices[0].message.model_dump(include={"role", "content", "tool_calls"}),
        )
        return self.postprocess_message(first_message, tools_to_call_from)

model = RetryingOpenAIServerModel(
    model_id="gpt-4o-mini",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
)
search = DuckDuckGoSearchTool()
final_answer = FinalAnswerTool()
tools = chromium_tools + windows_tools + [search, final_answer] 

agent = CodeAgent(
    tools=tools,
    model=model,
    step_callbacks = [save_screenshot],
    max_steps=10,
    verbosity_level=2
)


firefox_instructions = """ You can click on the screen using the coordinates (x, y) and type text in the browser. To search in firefox, you have to first open firefox then click on the search bar, followed by inputting the text query. Remember to always select the search bar before typing. Use search_in_firefox to query in firefox. Try not to use clicking but other ways of selection first. You can also use the search bar to search for text in the page. You can scroll up and down the page using the scroll_up and scroll_down functions. You can also switch tabs using the switch_tab function. You can close the current window using the close_window function. You can also press a specific key using the press_key function. You can focus on the address bar using the focus_address_bar function. You can also type text in the address bar using the type_text function. You can also press a combination of keys using the press_key_combo function. You can also select an option from firefox's suggestion list after a search (also works with dropdowns) by pressing the Down arrow key 'index' times and then hitting Enter. For example, index=1 selects the first suggestion."""

chromium_instructions = """You can navigate to a specific url with the navigate_to_url tool. You can also type text into an input field identified by a selector with the type_text tool. If you are at google.com and want to select the google search bar, use selector="textarea[name='q']". You can click on an element identified by a selector with the click_element tool. You can also scroll the page using the scroll_page tool. You can also press a specific key using the press_key tool. You can also press a combination of keys using the press_key_combo tool. You can do key combinations with the press_key_combo_chromium tool. It is better to use the DuckDuckGoSearchTool to query and get the links of the pages and use these links directly, instead of searching in Google. Try to do that as much as possible"""

navigation_instructions = """- If no suitable elements exist, use other functions to complete the task
- If stuck, try alternative approaches - like going back to a previous page, new search, new tab etc.
- Handle popups/cookies by accepting or closing them (mosst of them can be closed by clicking on the 'X' button likely situated on the top right corner, use the click_at tool)
-If you cannot close the advertisment, go to another page
- Use scroll to find elements you are looking for
- If you want to research something, open a new tab instead of using the current tab
- If captcha pops up, try to solve it - else try a different approach
- If the page is not fully loaded, use wait action"""

if __name__ == "__main__":
    agent.run(chromium_instructions+navigation_instructions+"Search for what Trump has done on tariffs, and the amount levied on Singapore.")

# python -m agent.computer_agent   