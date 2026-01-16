"""
Windows Bedrock Edition
"""

from typing import Optional
from os import path
from mcpath.facades import BedrockUWP


class WinBedrockUWP(BedrockUWP):
    def _get_game_dir(self, *paths: str) -> Optional[str]:
        p = path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )
        p = path.join(p, *paths)
        if path.isdir(p):
            return p
        return None


def instance():
    return WinBedrockUWP()
