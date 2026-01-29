"""
MacOS X Education Edition
"""

from typing import List
from .education_uwp import OSXEducationUWP


class OSXEducationGDK(OSXEducationUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return OSXEducationGDK()
