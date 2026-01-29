"""
Linux Bedrock Edition
"""

from typing import List
from .bedrock_uwp import LinuxBedrockUWP


class LinuxBedrockGDK(LinuxBedrockUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return LinuxBedrockGDK()
