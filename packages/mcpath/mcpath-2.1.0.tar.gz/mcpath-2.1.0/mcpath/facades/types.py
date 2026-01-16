__all__ = [
    "BedrockUWPProtocol",
    "BedrockGDKProtocol",
    "PreviewUWPProtocol",
    "PreviewGDKProtocol",
    "EducationUWPProtocol",
    "EducationGDKProtocol",
    "JavaProtocol",
]

from abc import abstractmethod
from typing import List, Protocol, Optional


class JavaProtocol(Protocol):
    @abstractmethod
    def launch(self) -> Optional[str]:
        """
        Launches Minecraft.
        """
        ...

    @abstractmethod
    def get_runtime(self, version: str) -> Optional[str]:
        """
        Get the path to the java runtime executable.
        """
        ...

    @abstractmethod
    def get_root_dir(self) -> Optional[str]:
        """
        Get the path to the `.minecraft` folder.
        """
        ...

    @abstractmethod
    def get_game_dir(self) -> Optional[str]:
        """
        Get the path to the game directory.

        NOTE: If you want the `.minecraft` folder use get_root_dir instead.
        """
        ...

    @abstractmethod
    def get_launcher(self) -> Optional[str]:
        """
        Get the path to the Minecraft launcher.
        """
        ...

    @abstractmethod
    def get_launcher_logs(self) -> Optional[str]:
        """
        Get the path to the Minecraft launcher log file.
        """
        ...

    @abstractmethod
    def get_versions_dir(self) -> Optional[str]:
        """
        Get the path of the directory holding version jar files.
        """
        ...

    @abstractmethod
    def get_saves_dir(self) -> Optional[str]:
        """
        Get the path of the directory holding world files.
        """
        ...

    @abstractmethod
    def get_resource_packs_dir(self) -> Optional[str]:
        """
        Get the path of the directory holding resource pack files.
        """
        ...

    @abstractmethod
    def get_screenshots_dir(self) -> Optional[str]:
        """
        Get the path of the directory holding screenshot files.
        """
        ...

    @abstractmethod
    def get_backups_dir(self) -> Optional[str]:
        """
        Get the path of the directory holding world backups.
        """
        ...

    @abstractmethod
    def get_logs_dir(self) -> Optional[str]:
        """
        Get the path of the directory holding game log files.
        """
        ...

    @abstractmethod
    def get_versions(self) -> List[str]:
        """
        Get a list of game versions.
        """
        ...

    @abstractmethod
    def get_saves(self) -> List[str]:
        """
        Get a list of world saves.
        """
        ...

    @abstractmethod
    def get_resource_packs(self) -> List[str]:
        """
        Get a list of resource packs.
        """
        ...

    @abstractmethod
    def get_screenshots(self) -> List[str]:
        """
        Get a list of screenshots.
        """
        ...

    @abstractmethod
    def get_backups(self) -> List[str]:
        """
        Get a list of world backups.
        """
        ...

    @abstractmethod
    def get_logs(self) -> List[str]:
        """
        Get a list of game logs.
        """
        ...


class BedrockProtocol(Protocol):
    @abstractmethod
    def launch(self) -> Optional[str]:
        """
        Launches Minecraft.
        """
        ...

    @abstractmethod
    def get_executable(self) -> Optional[str]:
        """
        Get the path of the executable file.
        """
        ...

    @abstractmethod
    def get_logs_dir(self) -> Optional[str]:
        """
        Get the path of the directory holding game log files.
        """
        ...

    @abstractmethod
    def get_logs(self) -> List[str]:
        """
        Get a list of game logs.
        """
        ...


class BedrockUWPProtocol(BedrockProtocol):

    @abstractmethod
    def get_game_dir(self, *paths: str) -> Optional[str]:
        """
        Get the path to the com.mojang folder.
        """
        ...

    @abstractmethod
    def get_worlds_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding world files.
        """
        ...

    @abstractmethod
    def get_world_templates_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding world template files.
        """
        ...

    @abstractmethod
    def get_resource_packs_dir(self, user: Optional[str] = None) -> Optional[str]:
        """
        Get the path of the directory holding resource pack files.
        """
        ...

    @abstractmethod
    def get_behavior_packs_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding behavior pack files.
        """
        ...

    @abstractmethod
    def get_skin_packs_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding skin pack files.
        """
        ...

    @abstractmethod
    def get_development_resource_packs_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding development resource pack files.
        """
        ...

    @abstractmethod
    def get_development_behavior_packs_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding development behavior pack files.
        """
        ...

    @abstractmethod
    def get_development_skin_packs_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding development skin pack files.
        """
        ...

    @abstractmethod
    def get_custom_skins_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding custom skin files.
        """
        ...

    @abstractmethod
    def get_screenshots_dir(
        self,
    ) -> Optional[str]:
        """
        Get the path of the directory holding screenshot files.
        """
        ...

    # Helpers

    @abstractmethod
    def get_worlds(self) -> List[str]:
        """
        Get a list of world paths.
        """
        ...

    @abstractmethod
    def get_behavior_packs(self) -> List[str]:
        """
        Get a list of behavior packs.
        """
        ...

    @abstractmethod
    def get_resource_packs(self) -> List[str]:
        """
        Get a list of resource packs.
        """
        ...

    @abstractmethod
    def get_development_behavior_packs(self) -> List[str]:
        """
        Get a list of development behavior packs.
        """
        ...

    @abstractmethod
    def get_development_resource_packs(self) -> List[str]:
        """
        Get a list of development resource packs.
        """
        ...

    @abstractmethod
    def get_development_skin_packs(self) -> List[str]:
        """
        Get a list of development skin packs.
        """
        ...

    @abstractmethod
    def get_screenshots(self) -> List[str]:
        """
        Get a list of screenshots.
        """
        ...


class BedrockGDKProtocol(BedrockProtocol):

    @abstractmethod
    def get_users(self) -> List[str]:
        """
        Get a list of all users.
        """
        ...

    @abstractmethod
    def get_root_dir(self) -> Optional[str]:
        """
        Get the path to the `Minecraft Bedrock` folder.
        """
        ...

    @abstractmethod
    def get_game_dir(self, user: Optional[str] = None, *paths: str) -> Optional[str]:
        """
        Get the path to the com.mojang folder.
        """
        ...

    @abstractmethod
    def get_worlds_dir(self, user: Optional[str] = None) -> Optional[str]:
        """
        Get the path of the directory holding world files.
        """
        ...

    @abstractmethod
    def get_world_templates_dir(self, user: Optional[str] = None) -> Optional[str]:
        """
        Get the path of the directory holding world template files.
        """
        ...

    @abstractmethod
    def get_resource_packs_dir(self, user: Optional[str] = None) -> Optional[str]:
        """
        Get the path of the directory holding resource pack files.
        """
        ...

    @abstractmethod
    def get_behavior_packs_dir(self, user: Optional[str] = None) -> Optional[str]:
        """
        Get the path of the directory holding behavior pack files.
        """
        ...

    @abstractmethod
    def get_skin_packs_dir(self, user: Optional[str] = None) -> Optional[str]:
        """
        Get the path of the directory holding skin pack files.
        """
        ...

    @abstractmethod
    def get_development_resource_packs_dir(
        self, user: Optional[str] = None
    ) -> Optional[str]:
        """
        Get the path of the directory holding development resource pack files.
        """
        ...

    @abstractmethod
    def get_development_behavior_packs_dir(
        self, user: Optional[str] = None
    ) -> Optional[str]:
        """
        Get the path of the directory holding development behavior pack files.
        """
        ...

    @abstractmethod
    def get_development_skin_packs_dir(
        self, user: Optional[str] = None
    ) -> Optional[str]:
        """
        Get the path of the directory holding development skin pack files.
        """
        ...

    @abstractmethod
    def get_custom_skins_dir(self, user: Optional[str] = None) -> Optional[str]:
        """
        Get the path of the directory holding custom skin files.
        """
        ...

    @abstractmethod
    def get_screenshots_dir(self, user: Optional[str] = None) -> Optional[str]:
        """
        Get the path of the directory holding screenshot files.
        """
        ...

    # Helpers

    @abstractmethod
    def get_worlds(self) -> List[str]:
        """
        Get a list of all world paths.
        """
        ...

    @abstractmethod
    def get_behavior_packs(self) -> List[str]:
        """
        Get a list of all behavior packs.
        """
        ...

    @abstractmethod
    def get_resource_packs(self) -> List[str]:
        """
        Get a list of all resource packs.
        """
        ...

    @abstractmethod
    def get_development_behavior_packs(self) -> List[str]:
        """
        Get a list of all development behavior packs.
        """
        ...

    @abstractmethod
    def get_development_resource_packs(self) -> List[str]:
        """
        Get a list of all development resource packs.
        """
        ...

    @abstractmethod
    def get_development_skin_packs(self) -> List[str]:
        """
        Get a list of all development skin packs.
        """
        ...

    @abstractmethod
    def get_screenshots(self) -> List[str]:
        """
        Get a list of all screenshots.
        """
        ...


class PreviewUWPProtocol(BedrockUWPProtocol):
    pass


class PreviewGDKProtocol(BedrockGDKProtocol):
    pass


class EducationUWPProtocol(BedrockUWPProtocol):
    pass


class EducationGDKProtocol(BedrockGDKProtocol):
    pass
