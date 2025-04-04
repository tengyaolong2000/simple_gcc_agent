
import requests

class ChromiumTools():

    @staticmethod
    def navigate_to_url(url: str):
        """Navigate to a specific URL using the browser."""
        try:
            response = requests.post("http://localhost:3000/navigate", json={"url": url})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error navigating: {e}")

    @staticmethod
    def type_text(selector: str, text: str):
        """Type text into an input field identified by a selector."""
        try:
            response = requests.post("http://localhost:3000/type", json={"selector": selector, "text": text})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error typing text: {e}")
    
    @staticmethod
    def click_element(selector: str):
        """Click an element identified by a selector."""
        try:
            response = requests.post("http://localhost:3000/click", json={"selector": selector})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error clicking element: {e}")
    
    @staticmethod
    def press_key(key: str):
        """Simulate a key press."""
        try:
            response = requests.post("http://localhost:3000/press", json={"key": key})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error pressing key: {e}")
    @staticmethod
    def press_key_combination(key1: str, key2: str):
        """Simulate pressing a combination of two keys."""
        try:
            response = requests.post("http://localhost:3000/press-combination", json={"key1": key1, "key2": key2})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error pressing key combination: {e}")
    
    @staticmethod
    def scroll_page(x: int = 0, y: int = 0, behavior: str = 'auto'):
        """Scroll the page by the specified x and y offsets."""
        try:
            response = requests.post("http://localhost:3000/scroll", json={"x": x, "y": y, "behavior": behavior})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error scrolling page: {e}")
    @staticmethod
    def clear_input(selector: str):
        """Clear the input field identified by a selector."""
        try:
            response = requests.post("http://localhost:3000/clear", json={"selector": selector})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error clearing input: {e}")

    @staticmethod
    def initialize_browser():
        """Initialize the browser."""
        try:
            response = requests.post("http://localhost:3000/initialize")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error initializing Chromium: {e}")
    
    @staticmethod
    def close_popup():
        """Close the popup in the browser."""
        try:
            response = requests.post("http://localhost:3000/close-popup")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error closing popup: {e}")