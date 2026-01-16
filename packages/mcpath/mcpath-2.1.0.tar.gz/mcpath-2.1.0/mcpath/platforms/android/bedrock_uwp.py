"""
Android Bedrock Edition
"""

from os import path
from mcpath.facades import BedrockUWP


class AndroidBedrockUWP(BedrockUWP):
    def _get_game_dir(self, *paths: str):
        internal = path.join(
            "data", "user", "0", "com.mojang.minecraftpe", "games", "com.mojang", *paths
        )
        external = path.join(
            "storage",
            "emulated",
            "0",
            "Android",
            "data",
            "com.mojang.minecraftpe",
            "files",
            "games",
            "com.mojang",
            *paths
        )
        if path.isdir(internal):
            return internal
        if path.isdir(external):
            return external
        return None

    def _get_executable(self):
        return "minecraft://"


def instance():
    return AndroidBedrockUWP()
