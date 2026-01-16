"""
Android Education Edition
"""

from typing import List
from education_uwp import AndroidEducationUWP


class AndroidEducationGDK(AndroidEducationUWP):
    def get_users(self) -> List[str]:
        return []


def instance():
    return AndroidEducationGDK()
