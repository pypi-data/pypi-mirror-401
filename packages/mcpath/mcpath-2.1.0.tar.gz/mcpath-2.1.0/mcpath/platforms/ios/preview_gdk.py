"""
iOS Preview Edition
"""

from typing import List
from .preview_uwp import iOSPreviewUWP


class iOSPreviewGDK(iOSPreviewUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return iOSPreviewGDK()
