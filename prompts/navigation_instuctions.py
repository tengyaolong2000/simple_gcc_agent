# These are prompts to be APPENDED to the default prompts.yaml files in smolagents

navigation_instructions = """- If no suitable elements exist, use other functions to complete the task
- If stuck, try alternative approaches - like going back to a previous page, new search, new tab etc.
- Handle popups/cookies by accepting or closing them (most of them can be closed by clicking on the 'X' button likely situated on the top right corner, use the click_at tool)
-If you cannot close the advertisment, go to another page
- Use scroll to find elements you are looking for
- If you want to research something, open a new tab instead of using the current tab
- If captcha pops up, try to solve it - else try a different approach
- If the page is not fully loaded, use wait action"""