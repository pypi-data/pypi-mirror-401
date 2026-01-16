"""
Windows Education Edition
"""

from os import path
from typing import Optional
from mcpath.facades import EducationGDK
from mcpath.utils import step_back


class WinEducationGDKEdition(EducationGDK):

    def _get_root_dir(self, *paths):
        return path.expandvars("%appdata%\\Minecraft Bedrock Education")

    def _get_game_dir(self, user: Optional[str], *paths):
        root = self.get_root_dir()
        if not root:
            return None
        return path.join(root, "users", user or "Shared", *paths)

    def _get_executable(self):
        return "minecraftEdu://"

    def _get_logs_dir(self):
        game_dir = self.get_game_dir()

        if not game_dir:
            return None
        return step_back(game_dir, 4, "logs")


def instance():
    return WinEducationGDKEdition()
