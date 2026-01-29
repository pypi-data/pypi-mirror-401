"""
Windows Bedrock Edition
"""

from typing import Optional
from os import path
from mcpath.facades import BedrockGDK
from mcpath.utils import step_back
import os


class WinBedrockGDK(BedrockGDK):

    def _get_root_dir(self, *paths):
        return path.expandvars("%appdata%\\Minecraft Bedrock")

    def _get_game_dir(self, user: Optional[str], *paths):
        root = self.get_root_dir()
        if not root:
            return None
        p = path.join(root, "users", user or "Shared", "games", "com.mojang", *paths)
        return p if os.path.exists(p) else None

    def _get_logs_dir(self):
        game_dir = self.get_game_dir()

        if not game_dir:
            return None
        return step_back(game_dir, 4, "logs")

    def _get_executable(self):
        return "minecraft://"

    def _get_users(self):
        root = self.get_root_dir()
        if not root or not path.isdir(root):
            return []
        return os.listdir(path.join(root, "Users"))


def instance():
    return WinBedrockGDK()
