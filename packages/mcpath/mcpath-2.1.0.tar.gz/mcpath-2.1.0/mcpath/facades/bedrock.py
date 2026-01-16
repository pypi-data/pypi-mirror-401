"""
Supported Platforms
-------------------
Android, iOS, Linux, MacOS, Windows
"""

__all__ = ["BedrockUWP", "BedrockGDK"]

from typing import Optional, List
from os import path
import glob
import webbrowser
import os


class Bedrock:
    def _get_packs(self, root: str) -> List[str]:
        return [
            path.join(root, folder)
            for folder in os.listdir(root)
            if path.isdir(path.join(root, folder))
            and path.isfile(path.join(root, folder, "manifest.json"))
        ]

    def launch(self) -> Optional[str]:
        return self._launch()

    def get_root_dir(self) -> Optional[str]:
        return self._get_root_dir()

    def get_executable(self) -> Optional[str]:
        return self._get_executable()

    def get_logs_dir(self) -> Optional[str]:
        return self._get_logs_dir()

    def get_logs(self) -> List[str]:
        root = self.get_logs_dir()
        if not root:
            return []
        return [
            path.join(root, file)
            for file in os.listdir(root)
            if path.isfile(path.join(root, file)) and file.endswith(".txt")
        ]

    def _get_executable(self) -> Optional[str]:
        return None

    def _get_logs_dir(self) -> Optional[str]:
        root = self.get_root_dir()
        if not root or not os.path.isdir(root):
            return None
        return os.path.join(root, "logs")

    def _launch(self) -> Optional[str]:
        url = self.get_executable()
        if url:
            webbrowser.open(url)
        return url

    def _get_root_dir(self) -> Optional[str]:
        return None


class BedrockUWP(Bedrock):
    """
    Bedrock Edition UWP facade.
    """

    def get_game_dir(self, *paths: str) -> Optional[str]:
        return self._get_game_dir(*paths)

    # Data

    def get_worlds_dir(self) -> Optional[str]:
        return self._get_worlds_dir()

    def get_world_templates_dir(
        self,
    ) -> Optional[str]:
        return self._get_world_templates_dir()

    def get_resource_packs_dir(
        self,
    ) -> Optional[str]:
        return self._get_resource_packs_dir()

    def get_behavior_packs_dir(
        self,
    ) -> Optional[str]:
        return self._get_behavior_packs_dir()

    def get_skin_packs_dir(
        self,
    ) -> Optional[str]:
        return self._get_skin_packs_dir()

    def get_development_resource_packs_dir(
        self,
    ) -> Optional[str]:
        return self._get_development_resource_packs_dir()

    def get_development_behavior_packs_dir(
        self,
    ) -> Optional[str]:
        return self._get_development_behavior_packs_dir()

    def get_development_skin_packs_dir(
        self,
    ) -> Optional[str]:
        return self._get_development_skin_packs_dir()

    def get_custom_skins_dir(
        self,
    ) -> Optional[str]:
        return self._get_custom_skins_dir()

    def get_screenshots_dir(
        self,
    ) -> Optional[str]:
        return self._get_screenshots_dir()

    # Helpers

    def get_worlds(self) -> List[str]:
        root = self.get_worlds_dir()
        if not root:
            return []
        return [
            path.join(root, folder)
            for folder in os.listdir(root)
            if path.isdir(path.join(root, folder))
        ]

    def get_behavior_packs(self) -> List[str]:
        root = self.get_behavior_packs_dir()
        if not root:
            return []
        return self._get_packs(root)

    def get_resource_packs(self) -> List[str]:
        root = self.get_resource_packs_dir()
        if not root:
            return []
        return self._get_packs(root)

    def get_development_behavior_packs(self) -> List[str]:
        root = self.get_development_behavior_packs_dir()
        if not root:
            return []
        return self._get_packs(root)

    def get_development_resource_packs(self) -> List[str]:
        root = self.get_development_resource_packs_dir()
        if not root:
            return []
        return self._get_packs(root)

    def get_development_skin_packs(self) -> List[str]:
        root = self.get_development_skin_packs_dir()
        if not root:
            return []
        return self._get_packs(root)

    def get_screenshots(self) -> List[str]:
        root = self.get_screenshots_dir()
        if not root:
            return []
        return [file for file in glob.glob(f"{root}/**/*.jpeg")]

    # private

    def _get_worlds_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("minecraftWorlds")

    def _get_world_templates_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("world_templates")

    def _get_resource_packs_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("resource_packs")

    def _get_behavior_packs_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("behavior_packs")

    def _get_skin_packs_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("skin_packs")

    def _get_development_resource_packs_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("development_resource_packs")

    def _get_development_behavior_packs_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("development_behavior_packs")

    def _get_development_skin_packs_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("development_skin_packs")

    def _get_custom_skins_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("custom_skins")

    def _get_screenshots_dir(
        self,
    ) -> Optional[str]:
        return self.get_game_dir("screenshots")

    # Hooks

    def _get_game_dir(self, *paths: str) -> Optional[str]:
        return None


class BedrockGDK(Bedrock):
    """
    Bedrock Edition GDK facade.
    """

    def get_users(self) -> List[str]:
        return self._get_users()

    def get_game_dir(self, user: Optional[str] = None, *paths: str) -> Optional[str]:
        return self._get_game_dir(user or "Shared", *paths)

    # Data

    def get_worlds_dir(self, user: Optional[str] = None) -> Optional[str]:
        return self._get_worlds_dir(user or "Shared")

    def get_world_templates_dir(self, user: Optional[str] = None) -> Optional[str]:
        return self._get_world_templates_dir(user or "Shared")

    def get_resource_packs_dir(self, user: Optional[str] = None) -> Optional[str]:
        return self._get_resource_packs_dir(user or "Shared")

    def get_behavior_packs_dir(self, user: Optional[str] = None) -> Optional[str]:
        return self._get_behavior_packs_dir(user or "Shared")

    def get_skin_packs_dir(self, user: Optional[str] = None) -> Optional[str]:
        return self._get_skin_packs_dir(user or "Shared")

    def get_development_resource_packs_dir(
        self, user: Optional[str] = None
    ) -> Optional[str]:
        return self._get_development_resource_packs_dir(user or "Shared")

    def get_development_behavior_packs_dir(
        self, user: Optional[str] = None
    ) -> Optional[str]:
        return self._get_development_behavior_packs_dir(user or "Shared")

    def get_development_skin_packs_dir(
        self, user: Optional[str] = None
    ) -> Optional[str]:
        return self._get_development_skin_packs_dir(user or "Shared")

    def get_custom_skins_dir(self, user: Optional[str] = None) -> Optional[str]:
        return self._get_custom_skins_dir(user or "Shared")

    def get_screenshots_dir(self, user: Optional[str] = None) -> Optional[str]:
        return self._get_screenshots_dir(user or "Shared")

    # Helpers

    # Fetch all packs including Shared and all users

    def _packs(self, start_path: str) -> List[str]:
        root = self.get_root_dir()
        return glob.glob(f"{root}\\Users\\*\\games\\com.mojang\\{start_path}\\*")

    def get_worlds(self) -> List[str]:
        return self._packs("minecraftWorlds")

    def get_resource_packs(self) -> List[str]:
        return self._packs("resource_packs")

    def get_behavior_packs(self) -> List[str]:
        return self._packs("behavior_packs")

    def get_skin_packs(self) -> List[str]:
        return self._packs("skin_packs")

    def get_development_resource_packs(self) -> List[str]:
        return self._packs("development_resource_packs")

    def get_development_behavior_packs(self) -> List[str]:
        return self._packs("development_behavior_packs")

    def get_development_skin_packs(self) -> List[str]:
        return self._packs("development_skin_packs")

    def get_screenshots(self) -> List[str]:
        root = self.get_screenshots_dir()
        if not root:
            return []
        return [file for file in glob.glob(f"{root}/**/*.jpeg")]

    # private

    def _get_worlds_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "minecraftWorlds")

    def _get_world_templates_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "world_templates")

    def _get_resource_packs_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "resource_packs")

    def _get_behavior_packs_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "behavior_packs")

    def _get_skin_packs_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "skin_packs")

    def _get_development_resource_packs_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "development_resource_packs")

    def _get_development_behavior_packs_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "development_behavior_packs")

    def _get_development_skin_packs_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "development_skin_packs")

    def _get_custom_skins_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "custom_skins")

    def _get_screenshots_dir(self, user: str) -> Optional[str]:
        return self.get_game_dir(user, "screenshots")

    # Hooks

    def _get_users(self) -> List[str]:
        return []

    def _get_game_dir(self, user: str, *paths: str) -> Optional[str]:
        return None
