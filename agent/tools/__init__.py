from .firefox_tools import (
    open_firefox,
    click,
    search_in_firefox,
    select_option_by_index,
    press_key_combo,
    scroll_down,
    scroll_up,
    switch_tab,
    type_text as type_text_firefox,
    close_window,
    press_key as press_key_firefox,
    focus_address_bar,
)

firefox_tools = [open_firefox, click, search_in_firefox, select_option_by_index, press_key_combo, scroll_down, scroll_up, switch_tab, type_text_firefox, close_window, press_key_firefox, focus_address_bar]

from .chromium_tools import (
    navigate_to_url,
    type_text as type_text_chromium,
    click_element,
    press_key as press_key_chromium,
    press_key_combo as press_key_combo_chromium,
    scroll_page, initialize_browser as initialize_chromium,
    close_popup
)

chromium_tools = [navigate_to_url, type_text_chromium, click_element, press_key_chromium, press_key_combo_chromium, scroll_page, initialize_chromium, close_popup]


from .windows_tools import (
    close_window,
    switch_tab,
    drag_and_drop,
    press_key_system,
    press_key_combo_system,
    open_terminal,
    click_at,
)

windows_tools = [close_window, switch_tab, drag_and_drop, press_key_system, press_key_combo_system, open_terminal, click_at]

from .stagehand_tools import (
    initialize_stagehand,
    navigate_stagehand,
    perform_action,
)
stagehand_tools = [initialize_stagehand, navigate_stagehand, perform_action]

from .additional_tools import (
    YouTubeTranscriptExtractorTool,
    LinksCheckpointStorageTool,
)

additional_tools = [YouTubeTranscriptExtractorTool, LinksCheckpointStorageTool]
