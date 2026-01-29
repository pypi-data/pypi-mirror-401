"""
Prompt XMLifier - Enterprise-grade prompt structuring tool for Claude.

Converts plain text prompts into XML-tagged prompts following
Anthropic's official best practices for prompt engineering.

Supports multiple Claude platforms:
- Claude webUI (claude.ai)
- Claude Code webUI (claude.ai/code)
- Claude Code CLI (terminal)
- Claude Code VS Extension

Reference: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
"""

__version__ = "1.0.0"
__author__ = "Fuad Oñate"

from .xmlifier import PromptXMLifier, ParserConfig
from .models import XMLTag, PromptSection, TagCategory
from .platforms import (
    Platform,
    PlatformConfig,
    get_platform_config,
    get_template,
    list_templates,
    format_for_platform,
    get_recommended_tags,
)
from .cli import main as cli_main

__all__ = [
    # Core
    "PromptXMLifier",
    "ParserConfig",
    "XMLTag",
    "PromptSection",
    "TagCategory",
    # Platforms
    "Platform",
    "PlatformConfig",
    "get_platform_config",
    "get_template",
    "list_templates",
    "format_for_platform",
    "get_recommended_tags",
    # CLI
    "cli_main",
]
