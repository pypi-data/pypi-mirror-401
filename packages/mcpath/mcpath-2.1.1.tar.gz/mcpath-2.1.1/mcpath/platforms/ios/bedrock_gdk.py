"""
iOS Bedrock Edition
"""

from typing import List
from bedrock_uwp import iOSBedrockUWP


class iOSBedrockGDK(iOSBedrockUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return iOSBedrockGDK()
