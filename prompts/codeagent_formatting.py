# These are prompts to be APPENDED to the default prompts.yaml files in smolagents

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