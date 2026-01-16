"""
Android Preview Edition
"""

from mcpath.facades import PreviewUWP


class AndroidPreviewUWP(PreviewUWP):
    pass


def instance():
    return AndroidPreviewUWP()
