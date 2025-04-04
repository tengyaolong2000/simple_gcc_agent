
from utils.utils import docker_exec, VM


class FirefoxTools(VM):
    def __init__(self, display, container_name):
        super().__init__(display, container_name)
        self.display = display
        self.container_name = container_name
        self.browser = "firefox"

    def open_firefox(self):
        cmd = f'DISPLAY={self.display} exo-open --launch WebBrowser &'
        return docker_exec(cmd, self.container_name)

    def search_in_firefox(self, text: str):
        """Use firefox browser to search given a query."""
        cmd = f'xdotool type "{text}" && xdotool key Return'
        return docker_exec(cmd, self.container_name)

    def go_back(self):
        """Simulate the back button in Firefox."""
        cmd = 'xdotool key Alt+Left'
        return docker_exec(cmd, self.container_name)
    
    def type_text(self, text: str):
        """Simulate typing text."""
        cmd = f'xdotool type "{text}"'
        return docker_exec(cmd, self.container_name)
 
    def refresh_page(self):
        """Refresh the current page (F5 key)."""
        cmd = 'xdotool key F5'
        return docker_exec(cmd, self.container_name)
    
    def scroll_down(self):
        """Scroll down the page (Page Down key)."""
        cmd = 'xdotool key Page_Down'
        return docker_exec(cmd, self.container_name)
    
    def scroll_up(self):
        """Scroll up the page (Page Up key)."""
        cmd = 'xdotool key Page_Up'
        return docker_exec(cmd, self.container_name)
    
    def focus_address_bar(self):
        """Focus the browser's address bar (Ctrl+L)."""
        cmd = 'xdotool key ctrl+l'
        return docker_exec(cmd, self.container_name)
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode (F11 key)."""
        cmd = 'xdotool key F11'
        return docker_exec(cmd, self.container_name)
    
    def select_option_by_index(self, index: int):
        """
        Select an option from Firefox's suggestion list after a search.
        This method presses the Down arrow key 'index' times and then hits Enter.
        For example, index=1 selects the first suggestion.
        """
        for _ in range(index):
            docker_exec("xdotool key Down", self.container_name)
        docker_exec("xdotool key Return", self.container_name)
    


    



if __name__ == "__main__":

    vm = VM(display=":99", container_name="cua-image")

    # Example: List files in the home directory of the container
    #output = docker_exec("ls -la /home/myuser", vm.container_name)
    #print("Files in /home/myuser:")
    #print(output)

    # Search for the "Mozilla Firefox" window, activate it, and press Ctrl+L
    #vm.open_firefox()
    #print('Activated the "Mozilla Firefox" window and focused on the address bar.')
    import requests

    vm.navigate_to_url("https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content")
    #vm.navigate_to_url("https://www.wikipedia.com")