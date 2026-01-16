"""
Linux Education Edition
"""

from typing import List
from .education_uwp import LinuxEducationUWP


class LinuxEducationGDK(LinuxEducationUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return LinuxEducationGDK()
