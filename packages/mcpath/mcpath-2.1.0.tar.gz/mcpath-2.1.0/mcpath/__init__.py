"""
Get paths to Minecraft Java, Bedrock, Preview, and Education Edition folders.
"""

__all__ = [
    "java",
    "bedrock",
    "preview",
    "education",
    "platform",
    "get_edition",
    "has_edition",
]
__version__ = "2.1.0"

from typing import cast
from mcpath import facades
from mcpath.utils import platform, Proxy

java: facades.JavaProtocol = cast(facades.JavaProtocol, Proxy("java", facades.Java))

bedrockUWP: facades.BedrockUWPProtocol = cast(
    facades.BedrockUWPProtocol, Proxy("bedrock_uwp", facades.BedrockUWP)
)
bedrockGDK: facades.BedrockGDKProtocol = cast(
    facades.BedrockGDKProtocol, Proxy("bedrock_gdk", facades.BedrockGDK)
)

previewUWP: facades.PreviewUWPProtocol = cast(
    facades.PreviewUWPProtocol, Proxy("preview_uwp", facades.PreviewUWP)
)
previewGDK: facades.PreviewGDKProtocol = cast(
    facades.PreviewGDKProtocol, Proxy("preview_gdk", facades.PreviewGDK)
)

educationUWP: facades.EducationUWPProtocol = cast(
    facades.EducationUWPProtocol, Proxy("education_uwp", facades.EducationUWP)
)
educationGDK: facades.EducationGDKProtocol = cast(
    facades.EducationGDKProtocol, Proxy("education_gdk", facades.EducationGDK)
)

# Deprecated
bedrock: facades.BedrockUWPProtocol = cast(
    facades.BedrockUWPProtocol, Proxy("bedrock_uwp", facades.BedrockUWP)
)
preview: facades.PreviewUWPProtocol = cast(
    facades.PreviewUWPProtocol, Proxy("preview_uwp", facades.PreviewUWP)
)
education: facades.EducationUWPProtocol = cast(
    facades.EducationUWPProtocol, Proxy("education_uwp", facades.EducationUWP)
)


def get_edition(
    name: str,
) -> (
    facades.JavaProtocol
    | facades.BedrockUWPProtocol
    | facades.BedrockGDKProtocol
    | facades.PreviewUWPProtocol
    | facades.PreviewGDKProtocol
    | facades.EducationUWPProtocol
    | facades.EducationGDKProtocol
):
    name = name.lower()
    match name:
        case "java":
            return java

        case "bedrock":
            return bedrock
        case "bedrockUWP":
            return bedrockUWP
        case "bedrockGDK":
            return bedrockGDK
        case "preview":
            return preview
        case "previewUWP":
            return previewUWP
        case "previewGDK":
            return previewGDK
        case "education":
            return education
        case "educationUWP":
            return educationUWP
        case "educationGDK":
            return educationGDK
    raise ValueError(f"{name} is not a valid edition")


def has_edition(name: str) -> bool:
    return get_edition(name) is not None
