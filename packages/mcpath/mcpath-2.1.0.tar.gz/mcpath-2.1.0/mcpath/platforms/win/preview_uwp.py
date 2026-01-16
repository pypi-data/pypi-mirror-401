"""
Windows Preview Edition
"""

from os import path
from mcpath.facades import PreviewUWP
from mcpath.utils import step_back


class WinPreviewUWPEdition(PreviewUWP):

    def _get_game_dir(self, *paths: str):
        p = path.expandvars(
            "%LOCALAPPDATA%\\Packages\\Microsoft.MinecraftWindowsBeta_8wekyb3d8bbwe\\LocalState\\games\\com.mojang"
        )
        p = path.join(p, *paths)
        if path.isdir(p):
            return p
        return None

    def _get_executable(self):
        return "minecraft-preview://"

    def _get_logs_dir(self):
        game_dir = self.get_game_dir()

        if not game_dir:
            return None
        return step_back(game_dir, 2, "logs")


def instance():
    return WinPreviewUWPEdition()
