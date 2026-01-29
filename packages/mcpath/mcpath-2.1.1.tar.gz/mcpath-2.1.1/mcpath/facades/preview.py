"""
Supported Platforms
-------------------
iOS, Windows
"""

__all__ = ["PreviewUWP", "PreviewGDK"]

from .bedrock import BedrockUWP, BedrockGDK


class PreviewUWP(BedrockUWP):
    """
    Preview Edition UWP facade.
    """

    pass


class PreviewGDK(BedrockGDK):
    """
    Preview Edition GDK facade.
    """

    pass
