"""
MacOS X Preview Edition
"""

from typing import List
from .preview_uwp import OSXPreviewUWP


class OXSPreviewGDK(OSXPreviewUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return OXSPreviewGDK()
