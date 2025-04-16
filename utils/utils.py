import subprocess
from typing import Union

from io import BytesIO
from PIL import Image

import os
import sys

# Add the project directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

class VM:
    def __init__(self, display, container_name):
        self.display = display
        self.container_name = container_name

    def get_vm(self):
        """Returns the currently instantiated VM object."""
        return self


def docker_exec(cmd: str, container_name: str, decode=True) -> Union[str, None]:
    """
    Execute a command in a Docker container and return the output.
    Args:
        cmd (str): Command to execute.
        container_name (str): Name of the Docker container.
        decode (bool): Whether to decode the output. Defaults to True.
    Returns:
        str: Output of the command.
    """
    # Escape single quotes for single-quoted shell string
    safe_cmd = cmd.replace("'", "'\\''")
    docker_cmd = f"docker exec {container_name} sh -c '{safe_cmd}'"

    output = subprocess.check_output(docker_cmd, shell=True)
    if decode:
        return output.decode("utf-8", errors="ignore")
    return output

def get_screenshot(container_name="gcc_agent-cua-vm-1"):
    """Capture a screenshot of the current display.
    Returns:
        Image object or None if an error occurs.
    """
    try:
        cmd = 'import -window root -silent png:-'
        output = docker_exec(cmd, container_name, decode=False)
        image = Image.open(BytesIO(output))
        image.load()  # Force load to catch issues early
        return image
    except Exception as e:
        print(f"[get_screenshot] Error capturing screenshot: {e}")
        return None