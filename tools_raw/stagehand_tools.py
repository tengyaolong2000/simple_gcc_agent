import requests

class StagehandTools:
    """A class to interact with Stagehand tools for web automation."""

    @staticmethod
    def initialize():
        """Initialize the Stagehand browser (Chromium)."""
        try:
            response = requests.get(f"http://localhost:4000/initialize")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error initializing: {e}")

    @staticmethod
    def navigate(url: str):
        """Navigate to a specified URL."""
        try:
            response = requests.post(f"http://localhost:4000/navigate", json={"url": url})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error navigating: {e}")

    @staticmethod
    def perform_action(action: str):
        """Perform a specified action."""
        try:
            response = requests.post(f"http://localhost:4000/action", json={"action": action})
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
        except requests.RequestException as e:
            print(f"Error performing action: {e}")


    