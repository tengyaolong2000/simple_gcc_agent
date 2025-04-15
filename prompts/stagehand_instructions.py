# These are prompts to be APPENDED to the default prompts.yaml files in smolagents

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
