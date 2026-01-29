"""
Android Bedrock Edition
"""

from typing import List
from .bedrock_uwp import AndroidBedrockUWP


class AndroidBedrockGDK(AndroidBedrockUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return AndroidBedrockGDK()
