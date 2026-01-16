"""
MacOS X Preview Edition
"""

from mcpath.facades import PreviewUWP


class OSXPreviewUWP(PreviewUWP):
    pass


def instance():
    return OSXPreviewUWP()
