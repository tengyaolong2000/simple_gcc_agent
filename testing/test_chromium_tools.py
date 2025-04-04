import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from agent.tools.chromium_tools import *

#navigate_to_url("https://www.wikipedia.com")
#type_text(selector="textarea[name='q']", text="Trump tariffs on Singapore")  # Typing the search query                                                                             
#press_key(key="Enter")  # Submitting the search  
#scroll_page(x=0, y=1000, behavior='smooth')  # Scroll down the page
#initialize_browser()

click_element('#btn_close_359734_1743744680190')
#if __name__ == "__main__":
#    click_by_text(text='Trump tariff')  