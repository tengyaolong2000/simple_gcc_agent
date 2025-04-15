
from time import sleep

from dotenv import load_dotenv

from smolagents import CodeAgent, ToolCallingAgent , OpenAIServerModel
from smolagents.agents import ActionStep
from utils.utils import get_screenshot
from agent.tools import chromium_tools, firefox_tools, windows_tools, stagehand_tools
from agent.tools.additional_tools import YouTubeTranscriptExtractor, LinksCheckpointStorage

from flask import Flask, request, jsonify
app = Flask(__name__)

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from smolagents.models import ChatMessage
from smolagents import DuckDuckGoSearchTool, FinalAnswerTool
from typing import Any, Dict, List, Optional, Union
from smolagents.tools import Tool
from smolagents.gradio_ui import GradioUI
import openai


load_dotenv()
import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

#sys.path.append(r"/Users/tengyaolong/Desktop/agent_stuff/personal_agent")

AUTHORIZED_IMPORTS = [
    "requests",
    "zipfile",
    "os",
    "pandas",
    "numpy",
    "sympy",
    "json",
    "bs4",
    "pubchempy",
    "xml",
    "yahoo_finance",
    "Bio",
    "sklearn",
    "scipy",
    "pydub",
    "io",
    "PIL",
    "chess",
    "PyPDF2",
    "pptx",
    "torch",
    "datetime",
    "fractions",
    "csv",
]

def save_screenshot(step_log: ActionStep, agent: CodeAgent) -> None:
    
    """Callback function to save a screenshot after each step."""

    sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
    current_step = step_log.step_number

    for step_logs in agent.memory.steps:  # Remove previous screenshots from logs for lean processing
        if isinstance(step_log, ActionStep) and step_log.step_number <= current_step - 2:
            step_logs.observations_images = None
            print(f"Removed previous screenshot from step {step_logs.step_number}")
        image = get_screenshot()
        #print(f"Captured a browser screenshot: {image.size} pixels")
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
    max_tokens=4096,
)
search = DuckDuckGoSearchTool()
final_answer = FinalAnswerTool()
tools = chromium_tools + windows_tools + [search, final_answer] 
tools_stagehand = stagehand_tools + windows_tools + [search, final_answer]

web_browser_agent = ToolCallingAgent(
        model=model,
        tools=tools_stagehand,
        max_steps=20,
        verbosity_level=2,
        planning_interval=4,
        name="search_agent",
        description="""A team member that will search the internet to answer your question.
    Ask him for all your questions that require browsing the web.
    Provide him as much context as possible, in particular if you need to search on a specific timeframe!
    And don't hesitate to provide him with a complex search task, like finding a difference between two webpages.
    Your request must be a real sentence, not a google search! Like "Find me this information (...)" rather than a few keywords.
    """,
    step_callbacks = [save_screenshot],
    provide_run_summary=True,

        
    )

manager_agent = CodeAgent(
    tools=[],
    model=model,
    step_callbacks = [save_screenshot],
    max_steps=12,
    planning_interval=4,
    verbosity_level=2,
    managed_agents=[web_browser_agent],
    additional_authorized_imports=AUTHORIZED_IMPORTS,

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

stagehand_instuctions = """ \nYou should first open a browser to use the web if the browser is not already open. As much as possible, use the DuckDuckGoSearchTool (the tool not the website) to query and get the links of the pages and use these links directly instead of searching on Google. 
# Important guidelines
1. Break down complex actions into individual atomic steps
2. For `act` commands, use only one action at a time, such as:
   - Single click on a specific element
   - Type into a single input field
   - Select a single option
3. Avoid combining multiple actions in one instruction
4. If multiple actions are needed, they should be separate steps`

# Additional instructions
- Maintain a storage (can be a list) of 3 links. If you are highly confident that the current link you are on is useful and correct, push it to the storage and remove the oldest link.
- If you are not sure about the current step/link, do not push it to the storage.

If you are a managed agent, for example, use search_agent(task="...") 
"""

codeagent_formatting = \
""" 
\n⚠️ CRITICAL: Always provide a 'Thought:' sequence, and a 'Code:\n```py' sequence ending with '```<end_code>' sequence, else you will fail.
     IMPORTANT: The format must be EXACTLY:
     Thought: Your reasoning here
     Code:
     ```py
     your_python_code_here()
     ```<end_code>
    
    - Do NOT use ```python or any other format - ONLY use ```py followed by your code and then ```<end_code>
    - Even if you have no code to run you still must include the python code block:
      - Thought: I have no code to run
      - Code:
        ```py
        final_answer("")
        ```<end_code>

If you are a managed agent, for example, use search_agent(task="...") 
"""

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_input = data.get("query")
    if not user_input:
        return jsonify({"error": "No query provided"}), 400
    result = manager_agent.run(stagehand_instuctions + user_input)
    return jsonify({"response": result})

web_browser_agent.prompt_templates["system_prompt"]+= stagehand_instuctions
manager_agent.prompt_templates["system_prompt"]+= codeagent_formatting
demo = GradioUI(manager_agent)

if __name__ == "__main__":
    demo.launch()
    #app.run(host="0.0.0.0", port=5001)
demo = GradioUI(manager_agent)
# python -m agent.computer_agent
# python GUI_app.py   

# test_query: 
"""What’s the title of the scientific paper published in the EMNLP conference between 2018-
2023 where the first author did their undergrad at Dartmouth College and the fourth
author did their undergrad at University of Pennsylvania? (Answer: Frequency Effects on
Syntactic Rule Learning in Transformers)"""