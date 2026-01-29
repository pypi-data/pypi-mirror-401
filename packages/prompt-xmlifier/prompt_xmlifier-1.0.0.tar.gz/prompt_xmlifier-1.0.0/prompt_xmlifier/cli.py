"""
Command-line interface for Prompt XMLifier.

Provides CLI commands for converting prompts to XML-tagged format
following Anthropic's official best practices.

Supports multiple Claude platforms:
- Claude webUI (claude.ai)
- Claude Code webUI (claude.ai/code)
- Claude Code CLI (terminal)
- Claude Code VS Extension

Usage:
    python -m prompt_xmlifier "Your prompt here"
    python -m prompt_xmlifier --platform claude_code_cli "Your prompt"
    python -m prompt_xmlifier --file prompt.txt --platform claude_web
    python -m prompt_xmlifier --interactive
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

from .xmlifier import PromptXMLifier, ParserConfig
from .models import XMLTag, TagCategory
from .platforms import (
    Platform,
    get_platform_config,
    get_platform_help,
    get_template,
    list_templates,
    format_for_platform,
    get_recommended_tags,
)


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        prog="prompt-xmlifier",
        description="Convert plain text prompts to XML-tagged format for Claude platforms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported Platforms:
  claude_web        - Claude webUI (claude.ai)
  claude_code_web   - Claude Code webUI (claude.ai/code)
  claude_code_cli   - Claude Code CLI (terminal)
  claude_code_vscode - Claude Code VS Extension

Examples:
  %(prog)s "Please analyze this code and find bugs"
  %(prog)s --platform claude_code_cli "Fix the bug in main.py"
  %(prog)s --file my_prompt.txt --platform claude_web --output structured.xml
  %(prog)s --platform claude_code_vscode --template edit_selection
  %(prog)s --list-platforms
  %(prog)s --list-templates claude_code_cli

Reference:
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
        """
    )

    # Input options
    input_group = parser.add_argument_group("Input Options")
    input_group.add_argument(
        "prompt",
        nargs="?",
        help="The prompt text to convert (or use --file)"
    )
    input_group.add_argument(
        "-f", "--file",
        type=Path,
        help="Read prompt from file"
    )
    input_group.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Interactive mode: enter prompt via stdin"
    )

    # Platform options
    platform_group = parser.add_argument_group("Platform Options")
    platform_group.add_argument(
        "-p", "--platform",
        choices=[p.value for p in Platform],
        default=Platform.CLAUDE_CODE_CLI.value,
        help="Target Claude platform (default: claude_code_cli)"
    )
    platform_group.add_argument(
        "-t", "--template",
        help="Use a platform-specific template (use --list-templates to see options)"
    )
    platform_group.add_argument(
        "--tips",
        action="store_true",
        help="Include platform-specific tips in output"
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "-o", "--output",
        type=Path,
        help="Write output to file (default: stdout)"
    )
    output_group.add_argument(
        "--format",
        choices=["xml", "json", "both"],
        default="xml",
        help="Output format (default: xml)"
    )
    output_group.add_argument(
        "--wrap",
        action="store_true",
        help="Wrap output in <prompt> tags"
    )

    # Parser options
    parser_group = parser.add_argument_group("Parser Options")
    parser_group.add_argument(
        "--min-length",
        type=int,
        default=10,
        help="Minimum section length (default: 10)"
    )
    parser_group.add_argument(
        "--confidence",
        type=float,
        default=0.3,
        help="Minimum confidence threshold (default: 0.3)"
    )
    parser_group.add_argument(
        "--no-nesting",
        action="store_true",
        help="Disable hierarchical tag nesting"
    )

    # Utility options
    parser.add_argument(
        "--list-tags",
        action="store_true",
        help="List all available XML tags and exit"
    )
    parser.add_argument(
        "--list-platforms",
        action="store_true",
        help="List all supported platforms with details"
    )
    parser.add_argument(
        "--list-templates",
        metavar="PLATFORM",
        nargs="?",
        const="all",
        help="List templates for a platform (or all platforms)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed processing information"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    return parser


def list_tags(platform: Optional[Platform] = None) -> None:
    """Print all available XML tags organized by category."""
    from .models import STANDARD_TAGS

    if platform:
        recommended = get_recommended_tags(platform)
        recommended_names = {t.name for t in recommended}
        print(f"Recommended XML Tags for {platform.value}")
    else:
        recommended_names = set()
        print("Available XML Tags for Claude Prompts")

    print("=" * 50)
    print()

    # Group by category
    by_category: dict[TagCategory, list[XMLTag]] = {}
    for tag in STANDARD_TAGS:
        if tag.category not in by_category:
            by_category[tag.category] = []
        by_category[tag.category].append(tag)

    for category in TagCategory:
        if category in by_category:
            print(f"{category.value.upper()}")
            print("-" * 30)
            for tag in sorted(by_category[category], key=lambda t: -t.priority):
                marker = "*" if tag.name in recommended_names else " "
                keywords = ", ".join(tag.keywords[:3])
                print(f" {marker}<{tag.name}>")
                print(f"    {tag.description}")
                print(f"    Keywords: {keywords}...")
                print()
            print()

    if platform:
        print("* = Recommended for this platform")


def list_all_platforms() -> None:
    """Print information about all supported platforms."""
    print("Supported Claude Platforms")
    print("=" * 60)
    print()

    for platform in Platform:
        config = get_platform_config(platform)
        templates = list_templates(platform)

        print(f"{platform.value}")
        print("-" * 40)
        print(f"  Recommended tags: {', '.join(config.recommended_tags[:5])}...")
        print(f"  Supports artifacts: {'Yes' if config.supports_artifacts else 'No'}")
        print(f"  Supports thinking: {'Yes' if config.supports_thinking else 'No'}")
        print(f"  Templates: {len(templates)} available")
        print()

    print("Use --list-templates <platform> to see available templates")
    print("Use --platform <name> to optimize output for a specific platform")


def list_platform_templates(platform_name: str) -> None:
    """Print templates for a specific platform or all platforms."""
    if platform_name == "all":
        print("Available Templates by Platform")
        print("=" * 50)
        print()
        for platform in Platform:
            templates = list_templates(platform)
            if templates:
                print(f"{platform.value}:")
                for template in templates:
                    print(f"  - {template}")
                print()
    else:
        try:
            platform = Platform(platform_name)
            templates = list_templates(platform)
            print(f"Templates for {platform.value}")
            print("=" * 40)
            if templates:
                for template in templates:
                    print(f"  - {template}")
            else:
                print("  (no templates available)")
            print()
            print(get_platform_help(platform))
        except ValueError:
            print(f"Error: Unknown platform '{platform_name}'", file=sys.stderr)
            print(f"Valid platforms: {', '.join(p.value for p in Platform)}", file=sys.stderr)


def read_input(args: argparse.Namespace) -> Optional[str]:
    """Read prompt input from the specified source."""
    if args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return None
        return args.file.read_text(encoding="utf-8")

    if args.prompt:
        return args.prompt

    if args.interactive or not sys.stdin.isatty():
        print("Enter your prompt (Ctrl+D or Ctrl+Z to finish):", file=sys.stderr)
        return sys.stdin.read()

    return None


def format_output(
    result,
    output_format: str,
    wrap: bool,
    platform: Optional[Platform] = None,
    include_tips: bool = False
) -> str:
    """Format the XMLified result based on requested format."""
    if output_format == "json":
        data = result.to_dict()
        if platform:
            data["platform"] = platform.value
        return json.dumps(data, indent=2, ensure_ascii=False)
    elif output_format == "both":
        xml_content = result.to_xml(include_wrapper=wrap)
        if platform and include_tips:
            xml_content = format_for_platform(xml_content, platform, include_tips=True)
        output = {
            "platform": platform.value if platform else None,
            "xml": xml_content,
            "structured": result.to_dict()
        }
        return json.dumps(output, indent=2, ensure_ascii=False)
    else:
        xml_content = result.to_xml(include_wrapper=wrap)
        if platform and include_tips:
            xml_content = format_for_platform(xml_content, platform, include_tips=True)
        return xml_content


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Handle --list-platforms
    if args.list_platforms:
        list_all_platforms()
        return 0

    # Handle --list-templates
    if args.list_templates:
        list_platform_templates(args.list_templates)
        return 0

    # Parse platform
    platform = Platform(args.platform)

    # Handle --list-tags
    if args.list_tags:
        list_tags(platform)
        return 0

    # Handle --template
    if args.template:
        template_content = get_template(platform, args.template)
        if template_content:
            print(f"# Template: {args.template} for {platform.value}")
            print(template_content)
            return 0
        else:
            print(f"Error: Template '{args.template}' not found for {platform.value}", file=sys.stderr)
            print(f"Available templates: {', '.join(list_templates(platform))}", file=sys.stderr)
            return 1

    # Read input
    prompt = read_input(args)
    if not prompt:
        parser.print_help()
        return 1

    # Get platform config
    platform_config = get_platform_config(platform)

    # Configure parser
    config = ParserConfig(
        min_section_length=args.min_length,
        confidence_threshold=args.confidence,
        nest_related_tags=not args.no_nesting
    )

    # Process prompt
    xmlifier = PromptXMLifier(config)

    if args.verbose:
        print(f"Platform: {platform.value}", file=sys.stderr)
        print(f"Processing prompt ({len(prompt)} chars)...", file=sys.stderr)

    result = xmlifier.convert(prompt)

    if args.verbose:
        print(f"Detected {len(result.sections)} sections", file=sys.stderr)
        recommended_tags = {t.name for t in get_recommended_tags(platform)}
        for section in result.sections:
            tag_name = section.tag.name if section.tag else "untagged"
            marker = "*" if tag_name in recommended_tags else " "
            print(f" {marker}<{tag_name}> (confidence: {section.confidence:.2f})", file=sys.stderr)
        print(file=sys.stderr)
        if recommended_tags:
            print("* = Recommended for this platform", file=sys.stderr)
            print(file=sys.stderr)

    # Determine wrap setting
    wrap = args.wrap or platform_config.include_wrapper

    # Format output
    output = format_output(result, args.format, wrap, platform, args.tips)

    # Write output
    if args.output:
        args.output.write_text(output, encoding="utf-8")
        if args.verbose:
            print(f"Output written to: {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
