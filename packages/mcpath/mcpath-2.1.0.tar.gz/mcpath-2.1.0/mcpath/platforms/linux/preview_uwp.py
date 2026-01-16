"""
Linux Preview Edition
"""

from mcpath.facades import PreviewUWP


class LinuxPreviewUWP(PreviewUWP):
    pass


def instance():
    return LinuxPreviewUWP()
