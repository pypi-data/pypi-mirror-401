"""
Windows Education Edition
"""

from typing import Optional
from os import path
from mcpath.facades import EducationUWP


class WinEducationUWPEdition(EducationUWP):
    def _get_game_dir(self, *paths: str) -> Optional[str]:
        p = path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftEducationEdition_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )
        if path.isdir(p):
            return p
        return None

    def _get_executable(self):
        return "minecraftEdu://"


def instance():
    return WinEducationUWPEdition()
