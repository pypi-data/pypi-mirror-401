"""
Platform-specific configurations for Prompt XMLifier.

Provides optimized output formats and templates for different Claude platforms:
- Claude webUI (claude.ai)
- Claude Code webUI (claude.ai/code)
- Claude Code CLI (terminal)
- Claude Code VS Extension (VSCode)

Reference: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .models import XMLTag, TagCategory, STANDARD_TAGS, get_tag_by_name


class Platform(Enum):
    """Supported Claude platforms."""

    CLAUDE_WEB = "claude_web"           # claude.ai web interface
    CLAUDE_CODE_WEB = "claude_code_web" # claude.ai/code web interface
    CLAUDE_CODE_CLI = "claude_code_cli" # Claude Code terminal
    CLAUDE_CODE_VSCODE = "claude_code_vscode"  # VS Code extension


@dataclass
class PlatformConfig:
    """
    Platform-specific configuration for prompt formatting.

    Attributes:
        platform: Target platform
        recommended_tags: Tags most effective for this platform
        tag_order: Preferred order of tags in output
        include_wrapper: Whether to wrap in <prompt> tags
        include_metadata: Whether to add platform hints
        max_sections: Maximum recommended sections
        code_block_style: How to format code blocks
        supports_artifacts: Whether platform supports artifacts
        supports_thinking: Whether platform supports thinking tags
    """

    platform: Platform
    recommended_tags: list[str] = field(default_factory=list)
    tag_order: list[str] = field(default_factory=list)
    include_wrapper: bool = False
    include_metadata: bool = False
    max_sections: int = 10
    code_block_style: str = "xml"  # "xml", "markdown", "both"
    supports_artifacts: bool = False
    supports_thinking: bool = True
    custom_instructions: str = ""


# Platform-specific configurations
PLATFORM_CONFIGS: dict[Platform, PlatformConfig] = {
    Platform.CLAUDE_WEB: PlatformConfig(
        platform=Platform.CLAUDE_WEB,
        recommended_tags=[
            "task", "context", "instructions", "example", "format",
            "constraints", "role", "tone", "audience"
        ],
        tag_order=[
            "role", "context", "task", "instructions", "input",
            "constraints", "rules", "format", "example", "output"
        ],
        include_wrapper=False,
        supports_artifacts=True,
        supports_thinking=True,
        code_block_style="markdown",
        custom_instructions="""
Best practices for Claude webUI:
- Use clear, descriptive tag names
- Place role/persona at the beginning
- Group related instructions together
- Use <example> for few-shot learning
- Keep prompts focused and concise
"""
    ),

    Platform.CLAUDE_CODE_WEB: PlatformConfig(
        platform=Platform.CLAUDE_CODE_WEB,
        recommended_tags=[
            "task", "context", "code", "instructions", "do", "do_not",
            "output", "constraints", "thinking"
        ],
        tag_order=[
            "role", "context", "task", "code", "instructions",
            "do", "do_not", "constraints", "output", "thinking"
        ],
        include_wrapper=False,
        supports_artifacts=True,
        supports_thinking=True,
        code_block_style="both",
        custom_instructions="""
Best practices for Claude Code webUI:
- Include code context in <code> tags
- Use <do> and <do_not> for clear boundaries
- Specify file paths and languages
- Request step-by-step reasoning with <thinking>
- Be explicit about expected output format
"""
    ),

    Platform.CLAUDE_CODE_CLI: PlatformConfig(
        platform=Platform.CLAUDE_CODE_CLI,
        recommended_tags=[
            "task", "context", "code", "instructions", "do", "do_not",
            "constraints", "rules", "output"
        ],
        tag_order=[
            "role", "context", "task", "code", "input",
            "instructions", "do", "do_not", "constraints",
            "rules", "format", "output"
        ],
        include_wrapper=False,
        include_metadata=True,
        supports_artifacts=False,
        supports_thinking=True,
        code_block_style="xml",
        max_sections=8,
        custom_instructions="""
Best practices for Claude Code CLI:
- Be concise - terminal context is limited
- Use <code> for file contents
- Specify exact file paths
- Use <do_not> for safety constraints
- Request specific actions, not general guidance
- Avoid redundant sections
"""
    ),

    Platform.CLAUDE_CODE_VSCODE: PlatformConfig(
        platform=Platform.CLAUDE_CODE_VSCODE,
        recommended_tags=[
            "task", "context", "code", "instructions", "do", "do_not",
            "constraints", "output", "thinking"
        ],
        tag_order=[
            "role", "context", "task", "code", "input",
            "instructions", "do", "do_not", "constraints",
            "rules", "format", "output", "thinking"
        ],
        include_wrapper=False,
        include_metadata=True,
        supports_artifacts=False,
        supports_thinking=True,
        code_block_style="xml",
        custom_instructions="""
Best practices for Claude Code VS Extension:
- Reference files by path (extension can read them)
- Use <code> for relevant snippets
- Be specific about edit locations
- Use <do_not> for code style constraints
- Request inline edits when possible
- Leverage IDE context (current file, selection)
"""
    ),
}


# Platform-specific prompt templates
PLATFORM_TEMPLATES: dict[Platform, dict[str, str]] = {
    Platform.CLAUDE_WEB: {
        "code_review": """
<role>
You are a senior software engineer conducting a code review.
</role>

<context>
{context}
</context>

<task>
Review the following code for bugs, security issues, and improvements.
</task>

<code>
{code}
</code>

<instructions>
1. Identify bugs and potential issues
2. Check for security vulnerabilities
3. Suggest performance improvements
4. Recommend code style improvements
</instructions>

<format>
Provide findings in a structured list with severity ratings (Critical/High/Medium/Low).
</format>
""",
        "explain_code": """
<role>
You are a patient teacher explaining code to a developer.
</role>

<context>
{context}
</context>

<task>
Explain how the following code works.
</task>

<code>
{code}
</code>

<instructions>
1. Start with a high-level overview
2. Explain each major section
3. Highlight important patterns or techniques
4. Note any potential issues or edge cases
</instructions>

<audience>
{audience}
</audience>
""",
        "generate_code": """
<task>
{task}
</task>

<context>
{context}
</context>

<instructions>
{instructions}
</instructions>

<constraints>
{constraints}
</constraints>

<format>
Provide complete, working code with comments explaining key decisions.
</format>
""",
    },

    Platform.CLAUDE_CODE_CLI: {
        "fix_bug": """
<task>
Fix the bug in the specified file.
</task>

<context>
{context}
</context>

<code>
{code}
</code>

<instructions>
1. Identify the root cause
2. Implement the fix
3. Verify the fix doesn't break other functionality
</instructions>

<do>
- Make minimal changes to fix the issue
- Preserve existing code style
- Add error handling if needed
</do>

<do_not>
- Refactor unrelated code
- Change public interfaces
- Remove existing comments
</do_not>
""",
        "implement_feature": """
<task>
{task}
</task>

<context>
{context}
</context>

<instructions>
{instructions}
</instructions>

<do>
- Follow existing code patterns
- Add appropriate error handling
- Write clean, readable code
</do>

<do_not>
- Over-engineer the solution
- Add unnecessary dependencies
- Break existing functionality
</do_not>

<output>
Create or modify the necessary files to implement the feature.
</output>
""",
        "refactor": """
<task>
Refactor the following code while preserving functionality.
</task>

<context>
{context}
</context>

<code>
{code}
</code>

<instructions>
{instructions}
</instructions>

<constraints>
- Maintain backward compatibility
- Preserve all existing tests
- Keep the same public API
</constraints>
""",
    },

    Platform.CLAUDE_CODE_VSCODE: {
        "edit_selection": """
<task>
{task}
</task>

<context>
File: {file_path}
Language: {language}
</context>

<code>
{selected_code}
</code>

<instructions>
{instructions}
</instructions>

<do>
- Make precise edits to the selection
- Maintain consistent style with surrounding code
</do>

<do_not>
- Modify code outside the selection unless necessary
- Change indentation style
</do_not>
""",
        "generate_tests": """
<task>
Generate unit tests for the following code.
</task>

<context>
File: {file_path}
Testing framework: {test_framework}
</context>

<code>
{code}
</code>

<instructions>
1. Test all public methods
2. Include edge cases
3. Test error conditions
4. Use descriptive test names
</instructions>

<constraints>
- Follow existing test patterns in the project
- Use the project's testing framework
- Keep tests focused and independent
</constraints>
""",
    },

    Platform.CLAUDE_CODE_WEB: {
        "architecture_design": """
<role>
You are a senior software architect.
</role>

<context>
{context}
</context>

<task>
Design the architecture for: {task}
</task>

<instructions>
1. Analyze requirements
2. Propose architecture options
3. Recommend the best approach with justification
4. Provide implementation plan
</instructions>

<thinking>
Walk through your design decisions step by step, explaining tradeoffs.
</thinking>

<format>
Include diagrams (mermaid format) where helpful.
</format>
""",
        "debug_issue": """
<task>
Debug and fix the following issue: {issue}
</task>

<context>
{context}
</context>

<code>
{code}
</code>

<instructions>
1. Analyze the error/issue
2. Identify root cause
3. Propose and implement fix
4. Explain why the fix works
</instructions>

<thinking>
Reason through the problem step by step before implementing the fix.
</thinking>
""",
    },
}


def get_platform_config(platform: Platform) -> PlatformConfig:
    """Get the configuration for a specific platform."""
    return PLATFORM_CONFIGS.get(platform, PLATFORM_CONFIGS[Platform.CLAUDE_CODE_CLI])


def get_template(platform: Platform, template_name: str) -> Optional[str]:
    """Get a specific template for a platform."""
    templates = PLATFORM_TEMPLATES.get(platform, {})
    return templates.get(template_name)


def list_templates(platform: Platform) -> list[str]:
    """List available templates for a platform."""
    return list(PLATFORM_TEMPLATES.get(platform, {}).keys())


def get_recommended_tags(platform: Platform) -> list[XMLTag]:
    """Get recommended tags for a platform."""
    config = get_platform_config(platform)
    tags = []
    for tag_name in config.recommended_tags:
        tag = get_tag_by_name(tag_name)
        if tag:
            tags.append(tag)
    return tags


def format_for_platform(
    xml_content: str,
    platform: Platform,
    include_tips: bool = False
) -> str:
    """
    Format XML content optimized for a specific platform.

    Args:
        xml_content: The XML-tagged prompt
        platform: Target platform
        include_tips: Whether to include platform tips

    Returns:
        Formatted prompt string
    """
    config = get_platform_config(platform)
    output_parts = []

    if include_tips:
        output_parts.append(f"# Platform: {platform.value}")
        output_parts.append(config.custom_instructions.strip())
        output_parts.append("")
        output_parts.append("# Prompt:")
        output_parts.append("")

    if config.include_wrapper:
        output_parts.append("<prompt>")
        output_parts.append(xml_content)
        output_parts.append("</prompt>")
    else:
        output_parts.append(xml_content)

    return "\n".join(output_parts)


def get_platform_help(platform: Platform) -> str:
    """Get help text for a specific platform."""
    config = get_platform_config(platform)

    help_text = f"""
Platform: {platform.value}
{'=' * 50}

Recommended Tags:
{', '.join(f'<{tag}>' for tag in config.recommended_tags)}

Tag Order (optimal):
{' -> '.join(config.tag_order[:5])}...

Features:
- Artifacts: {'Yes' if config.supports_artifacts else 'No'}
- Thinking tags: {'Yes' if config.supports_thinking else 'No'}
- Code style: {config.code_block_style}
- Max sections: {config.max_sections}

Available Templates:
{chr(10).join(f'  - {t}' for t in list_templates(platform)) or '  (none)'}

{config.custom_instructions}
"""
    return help_text.strip()
