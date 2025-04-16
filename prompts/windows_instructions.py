window_instructions = \
"""
\n Try to use the terminal to complete tasks as much as possible. You can open the terminal with the open_terminal tool. You can type text into the terminal with the type_text tool. You can also press a specific key using the press_key_system tool. You can also press a combination of keys using the press_key_combo_system tool. You can do key combinations with the press_key_combo_system tool. You can also drag and drop elements using the drag_and_drop tool. You can also close windows using the close_window tool. You can also switch tabs using the switch_tab tool. You can also left click at a specific position using the left_click_at tool. You can also right click at a specific position using the right_click_at tool.
\n\n

\nYou should only use tools that are available to you, mainly the windows_tools: close_window, switch_tab, drag_and_drop, press_key_system, press_key_combo_system, open_terminal, left_click_at, right_click_at. If you feel that something is wrong, it is highly recommended to redo what you are doing by performaing actions such as using the tool close_window or clearning the text you have typed in the terminal.
\n Additionally, when using rools such as typing tools, remember to use the following escape sequences:
Escape Double Quotes ("):

Replace " with \" to ensure the shell interprets it correctly.
Escape Single Quotes ('):

Replace ' with \' to handle cases where single quotes might cause issues.

The 'Enter' key should be replaced with 'Return' when using the press_key_system tool.

If you want to type text, it is very very much recommended and important to use the type_text tool instead ofthe press_key tool, or else you are likely to fail.
"""