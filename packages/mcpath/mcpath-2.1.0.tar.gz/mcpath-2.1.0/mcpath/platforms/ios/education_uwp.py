"""
iOS Education Edition
"""

from typing import Optional
from os import path
from mcpath.facades import EducationUWP
from mcpath.utils import _get_app
import os


class iOSEducationUWP(EducationUWP):
    def _get_game_dir(self, *paths: str) -> Optional[str]:
        id = "12330300-C946-4B6D-9CFA-13935A828E9A"
        p = path.join(
            "/private",
            "var",
            "mobile",
            "Containers",
            "Data",
            "Application",
            id,
            "Documents",
            "games",
            "com.mojang",
        )
        if os.access(p, os.R_OK):
            return p
        app = _get_app()
        match app:
            case "pyto":
                import file_system

                while True:
                    d = file_system.pick_directory()
                    if id in d:
                        return p
                    print("Invalid directory!")

            case "pythonista":
                # 1. Tap the hamburger menu at the top left
                # 2. Under "EXTERNAL FILES" tap "Open..."
                # 3. Then tap "Folder..."
                # 5. Navigate to your Minecraft folder and tap "Open"
                # 6. Finally, run the script again.
                pass
        raise PermissionError()

    def _get_executable(self):
        return "minecraftEdu://"


def instance():
    return iOSEducationUWP()
