"""
iOS Education Edition
"""

from typing import List
from .education_uwp import iOSEducationUWP


class iOSEducationGDK(iOSEducationUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return iOSEducationGDK()
