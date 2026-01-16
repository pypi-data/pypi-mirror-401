"""
Linux Bedrock Edition
"""

from os import path
from mcpath.facades import BedrockUWP
import configparser
import os


class LinuxBedrockUWP(BedrockUWP):
    def _launch(self):
        path = self.get_executable()
        if path:
            os.system(f'"{path}"')
        return path

    def _get_game_dir(self, *paths: str):
        fp = path.join(
            path.expanduser("~"),
            ".var",
            "app",
            "io.mrarm.mcpelauncher",
            "data",
            "mcpelauncher",
            "profiles",
            "profiles.ini",
        )
        if path.isfile(fp):
            try:
                config = configparser.ConfigParser()
                config.read(fp)
                if config.has_section("General"):
                    general = config["General"]
                    sel = general.get("selected")
                    if not sel:
                        return None
                    profile = config[sel]
                    data_dir = profile.get("dataDir")
                    if not data_dir:
                        return None
                    p = path.join(data_dir, "games", "com.mojang", *paths)
                    if path.isdir(p):
                        return p
                    return None
            except KeyError:
                pass

        # Fallback
        p = path.join(
            path.expanduser("~"),
            ".var",
            "app",
            "io.mrarm.mcpelauncher",
            "data",
            "mcpelauncher",
            "games",
            "com.mojang",
            *paths,
        )
        if path.isdir(p):
            return p
        return None

    def _get_executable(self):
        p = path.join(
            "/var",
            "lib",
            "flatpak",
            "app",
            "io.mrarm.mcpelauncher",
            "current",
            "active",
            "export",
            "bin",
            "io.mrarm.mcpelauncher",
        )
        if path.isfile(p):
            return p
        return None


def instance():
    return LinuxBedrockUWP()
