"""
Linux Education Edition
"""

from mcpath.facades import EducationUWP


class LinuxEducationUWP(EducationUWP):
    pass


def instance():
    return LinuxEducationUWP()
