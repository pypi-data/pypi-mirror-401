"""
Android Preview Edition
"""

from typing import List
from .preview_uwp import AndroidPreviewUWP


class AndroidPreviewGDK(AndroidPreviewUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return AndroidPreviewGDK()
