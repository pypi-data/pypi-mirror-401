"""
MacOS X Bedrock Edition
"""

from typing import List
from .bedrock_uwp import OSXBedrockUWP


class OSXBedrockGDK(OSXBedrockUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return OSXBedrockGDK()
