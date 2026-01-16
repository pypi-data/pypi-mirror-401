"""
Supported Platforms
-------------------
iOS, Windows
"""

__all__ = ["EducationUWP", "EducationGDK"]

from .bedrock import BedrockUWP, BedrockGDK


class EducationUWP(BedrockUWP):
    """
    Education Edition UWP facade.
    """

    pass


class EducationGDK(BedrockGDK):
    """
    Education Edition GDK facade.
    """

    pass
