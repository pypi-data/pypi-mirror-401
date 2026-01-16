"""
MacOS X Bedrock Edition
"""

from mcpath.facades import BedrockUWP


class OSXBedrockUWP(BedrockUWP):
    pass


def instance():
    return OSXBedrockUWP()
