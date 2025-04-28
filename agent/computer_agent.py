
from time import sleep

from dotenv import load_dotenv

from smolagents import CodeAgent, ToolCallingAgent , OpenAIServerModel
from smolagents.agents import ActionStep
from utils.utils import get_screenshot
from agent.tools import chromium_tools, firefox_tools, windows_tools, stagehand_tools, additional_tools


from flask import Flask, request, jsonify
app = Flask(__name__)

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from smolagents.models import ChatMessage
from smolagents import DuckDuckGoSearchTool, FinalAnswerTool
from typing import Any, Dict, List, Optional, Union
from smolagents import Tool
from smolagents.gradio_ui import GradioUI
import openai

from prompts.stagehand_instructions import stagehand_instuctions
from prompts.chromium_instructions import chromium_instructions
from prompts.firefox_instructions import firefox_instructions
from prompts.codeagent_formatting import codeagent_formatting
from prompts.windows_instructions import window_instructions

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
    model_id="gpt-4.1-nano",
    api_base="https://api.openai.com/v1",
    api_key=os.environ["OPENAI_API_KEY"],
    max_tokens=4096,
)
search = DuckDuckGoSearchTool()
final_answer = FinalAnswerTool()
tools = chromium_tools + windows_tools + [search, final_answer] 
tools = stagehand_tools + windows_tools + [search, final_answer] + additional_tools

for i in tools:
    assert isinstance(i, Tool), f"Tool {i} is not an instance of Tool class"

web_browser_agent = ToolCallingAgent(
        model=model,
        tools=tools,
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

operating_system_control_agent = ToolCallingAgent(
        model=model,
        tools=windows_tools,
        max_steps=20,
        verbosity_level=2,
        planning_interval=4,
        name="user_environment_control_agent",
        description="""A team member that will control the user environment to complete your tasks (such as creating a folder).
    Ask him for all your tasks that require conducting actions in the user environment.
    Provide him as much context as possible. He will execute actions with the windows tools at his disposal.
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
    managed_agents=[web_browser_agent,operating_system_control_agent],
    #additional_authorized_imports=AUTHORIZED_IMPORTS,

)

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    user_input = data.get("query")
    if not user_input:
        return jsonify({"error": "No query provided"}), 400
    result = manager_agent.run(stagehand_instuctions + user_input)
    return jsonify({"response": result})

web_browser_agent.prompt_templates["system_prompt"]+= stagehand_instuctions
operating_system_control_agent.prompt_templates["system_prompt"]+= window_instructions
manager_agent.prompt_templates["system_prompt"]+= codeagent_formatting
demo = GradioUI(manager_agent)

if __name__ == "__main__":
    demo.launch()
    #app.run(host="0.0.0.0", port=5001)


           
    #demo = GradioUI(manager_agent)
    # python -m agent.computer_agent
    # python GUI_app.py   

    # test_query: 
    """What’s the title of the scientific paper published in the EMNLP conference between 2018-
    2023 where the first author did their undergrad at Dartmouth College and the fourth
    author did their undergrad at University of Pennsylvania? (Answer: Frequency Effects on
    Syntactic Rule Learning in Transformers)"""

    """Who is the author of the Neurips 2024 best paper? What is the controversy surrounding him?"""