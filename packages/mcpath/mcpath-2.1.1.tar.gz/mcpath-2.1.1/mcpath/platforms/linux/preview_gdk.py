"""
Linux Preview Edition
"""

from typing import List
from .preview_uwp import LinuxPreviewUWP


class LinuxPreviewGDK(LinuxPreviewUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return LinuxPreviewGDK()
