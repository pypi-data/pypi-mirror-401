"""
Supported Platforms
-------------------
Linux, MacOS, Windows
"""

__all__ = ["Java"]

from typing import Optional, List
from os import path
import os


class Java:
    """
    Java Edition facade.
    """

    def launch(self) -> Optional[str]:
        return self._launch()

    def get_runtime(self, version: str) -> Optional[str]:
        return self._get_runtime(version)

    def get_root_dir(self, *paths: str) -> Optional[str]:
        return self._get_root_dir(*paths)

    def get_game_dir(self, *paths: str) -> Optional[str]:
        return self._get_game_dir(*paths)

    def get_launcher(self) -> Optional[str]:
        return self._get_launcher()

    def get_launcher_logs(self) -> Optional[str]:
        return self._get_launcher_logs()

    def get_versions_dir(self) -> Optional[str]:
        return self._get_versions_dir()

    def get_saves_dir(self) -> Optional[str]:
        return self._get_saves_dir()

    def get_resource_packs_dir(self) -> Optional[str]:
        return self._get_resource_packs_dir()

    def get_screenshots_dir(self) -> Optional[str]:
        return self._get_screenshots_dir()

    def get_backups_dir(self) -> Optional[str]:
        return self._get_backups_dir()

    def get_logs_dir(self) -> Optional[str]:
        return self._get_logs_dir()

    # private

    def _launch(self) -> Optional[str]:
        return None

    def _get_runtime(self, version) -> Optional[str]:
        return None

    def _get_root_dir(self, *paths: str) -> Optional[str]:
        return None

    def _get_launcher(self) -> Optional[str]:
        return None

    def _get_game_dir(self, *paths: str) -> Optional[str]:
        return None

    def _get_launcher_logs(self) -> Optional[str]:
        root = self.get_root_dir()
        if not root:
            return None
        return os.path.join(root, "launcher_log.txt")

    def _get_versions_dir(self) -> Optional[str]:
        return self.get_root_dir("versions")

    def _get_saves_dir(self) -> Optional[str]:
        return self.get_game_dir("saves")

    def _get_resource_packs_dir(self) -> Optional[str]:
        return self.get_game_dir("resourcepacks")

    def _get_screenshots_dir(self) -> Optional[str]:
        return self.get_game_dir("screenshots")

    def _get_backups_dir(self) -> Optional[str]:
        return self.get_game_dir("backups")

    def _get_logs_dir(self) -> Optional[str]:
        return self.get_game_dir("logs")

    def get_versions(self) -> List[str]:
        root = self.get_versions_dir()
        if not root:
            return []
        return [
            path.join(root, folder)
            for folder in os.listdir(root)
            if path.isdir(path.join(root, folder))
        ]

    def get_saves(self) -> List[str]:
        root = self.get_saves_dir()
        if not root:
            return []

        return [
            path.join(root, folder)
            for folder in os.listdir(root)
            if path.isdir(path.join(root, folder))
            and path.isfile(path.join(root, folder, "level.dat"))
        ]

    def get_resource_packs(self) -> List[str]:
        root = self.get_resource_packs_dir()
        if not root:
            return []
        return [
            path.join(root, folder)
            for folder in os.listdir(root)
            if path.isdir(path.join(root, folder))
            and path.isfile(path.join(root, folder, "pack.mcmeta"))
        ]

    def get_screenshots(self) -> List[str]:
        root = self.get_screenshots_dir()
        if not root:
            return []
        return [
            path.join(root, file)
            for file in os.listdir(root)
            if path.isfile(path.join(root, file)) and file.endswith(".png")
        ]

    def get_backups(self) -> List[str]:
        root = self.get_backups_dir()
        if not root:
            return []
        return [
            path.join(root, file)
            for file in os.listdir(root)
            if path.isfile(path.join(root, file)) and file.endswith(".zip")
        ]

    def get_logs(self) -> List[str]:
        root = self.get_logs_dir()
        if not root:
            return []
        return [
            path.join(root, file)
            for file in os.listdir(root)
            if path.isfile(path.join(root, file)) and file.endswith(".log")
        ]
