"""
MacOS X Education Edition
"""

from mcpath.facades import EducationUWP


class OSXEducationUWP(EducationUWP):
    pass


def instance():
    return OSXEducationUWP()
