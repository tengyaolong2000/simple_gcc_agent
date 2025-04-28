from smolagents import CodeAgent, ToolCallingAgent
import textwrap
from smolagents.memory import (
    ActionStep,
    AgentMemory,
    FinalAnswerStep,
    Message,
    PlanningStep,
    SystemPromptStep,
    TaskStep,
    ToolCall,
)
import requests
from rich.rule import Rule, Text
from smolagents.models import  MessageRole
from smolagents.agents import populate_template
from smolagents.monitoring import LogLevel

def refine_plan(plan: str) -> str:

    response = requests.post("http://localhost:9000/generate", json={"prompt": f"You are tasked to improve this plan: {plan}. Improved/Corrected version:"})
    result = "Refined " + response.json()["response"]

    return result

class CustomCodeAgent(CodeAgent):
    def _create_planning_step(self, task, is_first_step: bool, step: int) -> PlanningStep:
        if is_first_step:
            input_messages = [
                {
                    "role": MessageRole.USER,
                    "content": [
                        {
                            "type": "text",
                            "text": populate_template(
                                self.prompt_templates["planning"]["initial_plan"],
                                variables={"task": task, "tools": self.tools, "managed_agents": self.managed_agents},
                            ),
                        }
                    ],
                }
            ]
            plan_message = self.model(input_messages, stop_sequences=["<end_plan>"])
            plan = textwrap.dedent(
                f"""Here are the facts I know and the plan of action that I will follow to solve the task:\n```\n{plan_message.content}\n```"""
            )
            plan = refine_plan(plan=plan)
        else:
            # Summary mode removes the system prompt and previous planning messages output by the model.
            # Removing previous planning messages avoids influencing too much the new plan.
            memory_messages = self.write_memory_to_messages(summary_mode=True)
            plan_update_pre = {
                "role": MessageRole.SYSTEM,
                "content": [
                    {
                        "type": "text",
                        "text": populate_template(
                            self.prompt_templates["planning"]["update_plan_pre_messages"], variables={"task": task}
                        ),
                    }
                ],
            }
            plan_update_post = {
                "role": MessageRole.USER,
                "content": [
                    {
                        "type": "text",
                        "text": populate_template(
                            self.prompt_templates["planning"]["update_plan_post_messages"],
                            variables={
                                "task": task,
                                "tools": self.tools,
                                "managed_agents": self.managed_agents,
                                "remaining_steps": (self.max_steps - step),
                            },
                        ),
                    }
                ],
            }
            input_messages = [plan_update_pre] + memory_messages + [plan_update_post]
            plan_message = self.model(input_messages, stop_sequences=["<end_plan>"])
            plan = textwrap.dedent(
                f"""I still need to solve the task I was given:\n```\n{self.task}\n```\n\nHere are the facts I know and my new/updated plan of action to solve the task:\n```\n{plan_message.content}\n```"""
            )
            plan = refine_plan(plan=plan)
        log_headline = "Initial plan" if is_first_step else "Updated plan"
        self.logger.log(Rule(f"[bold]{log_headline}", style="orange"), Text(plan), level=LogLevel.INFO)
        return PlanningStep(
            model_input_messages=input_messages,
            plan=plan,
            model_output_message=plan_message,
        )

class CustomToolAgent(ToolCallingAgent):
    def _create_planning_step(self, task, is_first_step: bool, step: int) -> PlanningStep:
        if is_first_step:
            input_messages = [
                {
                    "role": MessageRole.USER,
                    "content": [
                        {
                            "type": "text",
                            "text": populate_template(
                                self.prompt_templates["planning"]["initial_plan"],
                                variables={"task": task, "tools": self.tools, "managed_agents": self.managed_agents},
                            ),
                        }
                    ],
                }
            ]
            plan_message = self.model(input_messages, stop_sequences=["<end_plan>"])
            plan = textwrap.dedent(
                f"""Here are the facts I know and the plan of action that I will follow to solve the task:\n```\n{plan_message.content}\n```"""
            )
            plan = refine_plan(plan=plan)
        else:
            # Summary mode removes the system prompt and previous planning messages output by the model.
            # Removing previous planning messages avoids influencing too much the new plan.
            memory_messages = self.write_memory_to_messages(summary_mode=True)
            plan_update_pre = {
                "role": MessageRole.SYSTEM,
                "content": [
                    {
                        "type": "text",
                        "text": populate_template(
                            self.prompt_templates["planning"]["update_plan_pre_messages"], variables={"task": task}
                        ),
                    }
                ],
            }
            plan_update_post = {
                "role": MessageRole.USER,
                "content": [
                    {
                        "type": "text",
                        "text": populate_template(
                            self.prompt_templates["planning"]["update_plan_post_messages"],
                            variables={
                                "task": task,
                                "tools": self.tools,
                                "managed_agents": self.managed_agents,
                                "remaining_steps": (self.max_steps - step),
                            },
                        ),
                    }
                ],
            }
            input_messages = [plan_update_pre] + memory_messages + [plan_update_post]
            plan_message = self.model(input_messages, stop_sequences=["<end_plan>"])
            plan = textwrap.dedent(
                f"""I still need to solve the task I was given:\n```\n{self.task}\n```\n\nHere are the facts I know and my new/updated plan of action to solve the task:\n```\n{plan_message.content}\n```"""
            )
            plan = refine_plan(plan=plan)
        log_headline = "Initial plan" if is_first_step else "Updated plan"
        self.logger.log(Rule(f"[bold]{log_headline}", style="orange"), Text(plan), level=LogLevel.INFO)
        return PlanningStep(
            model_input_messages=input_messages,
            plan=plan,
            model_output_message=plan_message,
        )
