# These are prompts to be APPENDED to the default prompts.yaml files in smolagents

codeagent_formatting = \
""" 
\n ⚠️ Extremely CRITICAL! : All tasks you are asked to perform is in the context of the virtual machine desktop (Ubuntu).
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


n⚠️ CRITICAL:
Importantly, print(...) does not type in or execute commands in the virtual machine desktop (it is useless). Use tools and get the help of your managed agents instead to execute actions in the vm.

n⚠️ CRITICAL:
You can call your managed agents such as the user_environment_control_agent like this:
user_environment_control_agent(task=task_description)
and the search_agent like this:
search_agent(task=task_description)
"""