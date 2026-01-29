"""
Core XMLifier engine for converting prompts to XML-tagged format.

Implements intelligent parsing and tagging following Anthropic's
official prompt engineering best practices.

Reference: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from .models import (
    XMLTag,
    PromptSection,
    TagCategory,
    STANDARD_TAGS,
    get_tag_by_name,
)


@dataclass
class ParserConfig:
    """Configuration options for the prompt parser."""

    min_section_length: int = 10          # Minimum chars for a section
    confidence_threshold: float = 0.3     # Minimum confidence to assign tag
    preserve_whitespace: bool = False     # Keep original whitespace
    auto_detect_code: bool = True         # Detect code blocks automatically
    nest_related_tags: bool = True        # Create hierarchical structure
    custom_tags: Optional[list[XMLTag]] = field(default=None)  # Additional custom tags


class PromptXMLifier:
    """
    Enterprise-grade prompt to XML converter.

    Parses plain text prompts and converts them to structured
    XML-tagged prompts optimized for Claude.

    Usage:
        xmlifier = PromptXMLifier()
        result = xmlifier.convert(plain_prompt)
        print(result.to_xml())

    Attributes:
        config: Parser configuration options
        tags: Available XML tags for matching
    """

    # Patterns for detecting explicit sections in prompts
    SECTION_PATTERNS = [
        # Markdown-style headers
        (r"^#{1,6}\s+(.+?)$", "header"),
        # Labeled sections (e.g., "Context:", "Task:")
        (r"^([A-Z][a-zA-Z_]+)\s*:\s*$", "label_line"),
        (r"^([A-Z][a-zA-Z_]+)\s*:\s*(.+)$", "label_inline"),
        # Numbered lists
        (r"^\d+\.\s+", "numbered"),
        # Bullet points
        (r"^[-*]\s+", "bullet"),
        # Code blocks
        (r"^```(\w*)\n([\s\S]*?)```$", "code_block"),
        # Inline code
        (r"`([^`]+)`", "inline_code"),
    ]

    # Common section labels that map to tags
    LABEL_TO_TAG = {
        "task": "task",
        "tarea": "task",
        "objetivo": "task",
        "goal": "task",
        "context": "context",
        "contexto": "context",
        "background": "background",
        "instructions": "instructions",
        "instrucciones": "instructions",
        "steps": "instructions",
        "pasos": "instructions",
        "input": "input",
        "entrada": "input",
        "data": "data",
        "datos": "data",
        "output": "output",
        "salida": "output",
        "format": "format",
        "formato": "format",
        "constraints": "constraints",
        "restricciones": "constraints",
        "rules": "rules",
        "reglas": "rules",
        "do": "do",
        "hacer": "do",
        "do_not": "do_not",
        "do not": "do_not",
        "dont": "do_not",
        "don't": "do_not",
        "no_hacer": "do_not",
        "no hacer": "do_not",
        "role": "role",
        "rol": "role",
        "persona": "role",
        "tone": "tone",
        "tono": "tone",
        "audience": "audience",
        "audiencia": "audience",
        "example": "example",
        "ejemplo": "example",
        "examples": "examples",
        "ejemplos": "examples",
        "thinking": "thinking",
        "pensamiento": "thinking",
        "analysis": "analysis",
        "analisis": "analysis",
        "document": "document",
        "documento": "document",
        "code": "code",
        "codigo": "code",
    }

    def __init__(self, config: Optional[ParserConfig] = None):
        """Initialize the XMLifier with optional configuration."""
        self.config = config or ParserConfig()
        self.tags = list(STANDARD_TAGS)
        if self.config.custom_tags:
            self.tags.extend(self.config.custom_tags)
        # Sort by priority (highest first)
        self.tags.sort(key=lambda t: t.priority, reverse=True)

    def convert(self, prompt: str) -> "XMLifiedPrompt":
        """
        Convert a plain text prompt to XML-tagged format.

        Args:
            prompt: The plain text prompt to convert

        Returns:
            XMLifiedPrompt object with structured sections
        """
        # Normalize line endings
        prompt = prompt.replace("\r\n", "\n").replace("\r", "\n")

        # Step 1: Detect explicit sections (labeled, headers, etc.)
        sections = self._detect_explicit_sections(prompt)

        # Step 2: If no explicit sections, analyze content semantically
        if not sections:
            sections = self._analyze_semantic_sections(prompt)

        # Step 3: Assign tags to sections based on content
        for section in sections:
            if section.confidence == 0:
                self._assign_tag_by_content(section)

        # Step 4: Build hierarchical structure if enabled
        if self.config.nest_related_tags:
            sections = self._build_hierarchy(sections)

        return XMLifiedPrompt(sections=sections, original=prompt)

    def _detect_explicit_sections(self, prompt: str) -> list[PromptSection]:
        """Detect explicitly labeled sections in the prompt."""
        sections = []
        lines = prompt.split("\n")
        current_section = None
        current_content = []
        current_tag = None

        for line in lines:
            # Check for label patterns (e.g., "Context:" or "<context>")
            label_match = re.match(r"^<(\w+)>$", line.strip())
            if label_match:
                # XML tag opening
                tag_name = label_match.group(1).lower()
                if current_section:
                    sections.append(self._create_section(
                        "\n".join(current_content),
                        current_tag,
                        confidence=0.95
                    ))
                current_tag = get_tag_by_name(tag_name) or self._create_custom_tag(tag_name)
                current_section = tag_name
                current_content = []
                continue

            close_match = re.match(r"^</(\w+)>$", line.strip())
            if close_match and current_section:
                tag_name = close_match.group(1).lower()
                if tag_name == current_section:
                    sections.append(self._create_section(
                        "\n".join(current_content),
                        current_tag,
                        confidence=0.95
                    ))
                    current_section = None
                    current_content = []
                    current_tag = None
                continue

            # Check for labeled sections (e.g., "Context:", "Do Not:")
            label_line_match = re.match(r"^([A-Za-z_]+(?:\s+[A-Za-z_]+)?)\s*:\s*$", line.strip())
            if label_line_match:
                if current_section and current_content:
                    sections.append(self._create_section(
                        "\n".join(current_content),
                        current_tag,
                        confidence=0.85
                    ))
                label = label_line_match.group(1).lower()
                tag_name = self.LABEL_TO_TAG.get(label, label)
                current_tag = get_tag_by_name(tag_name) or self._create_custom_tag(tag_name)
                current_section = tag_name
                current_content = []
                continue

            # Check for inline labeled sections (e.g., "Context: some text", "Do Not: something")
            label_inline_match = re.match(r"^([A-Za-z_]+(?:\s+[A-Za-z_]+)?)\s*:\s*(.+)$", line.strip())
            if label_inline_match and not current_section:
                label = label_inline_match.group(1).lower()
                content = label_inline_match.group(2)
                if label in self.LABEL_TO_TAG:
                    tag_name = self.LABEL_TO_TAG[label]
                    tag = get_tag_by_name(tag_name) or self._create_custom_tag(tag_name)
                    sections.append(self._create_section(content, tag, confidence=0.8))
                    continue

            if current_section:
                current_content.append(line)
            elif line.strip():
                # Unstructured content - will be analyzed semantically
                if not current_content or (current_content and current_tag):
                    if current_content and current_tag:
                        sections.append(self._create_section(
                            "\n".join(current_content),
                            current_tag,
                            confidence=0.5
                        ))
                    current_content = [line]
                    current_tag = None
                else:
                    current_content.append(line)

        # Handle remaining content
        if current_content:
            if current_tag:
                sections.append(self._create_section(
                    "\n".join(current_content),
                    current_tag,
                    confidence=0.85 if current_section else 0.5
                ))
            elif current_content:
                # Untagged content at the end
                sections.append(self._create_section(
                    "\n".join(current_content),
                    None,
                    confidence=0.0
                ))

        return sections

    def _analyze_semantic_sections(self, prompt: str) -> list[PromptSection]:
        """Analyze prompt semantically to identify sections."""
        sections = []

        # Split by paragraph breaks
        paragraphs = re.split(r"\n\s*\n", prompt)

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(para) < self.config.min_section_length:
                continue

            section = self._create_section(para, None, confidence=0.0)
            sections.append(section)

        return sections if sections else [self._create_section(prompt, None, confidence=0.0)]

    def _assign_tag_by_content(self, section: PromptSection) -> None:
        """Assign an appropriate tag based on content analysis."""
        content_lower = section.content.lower()
        best_tag = None
        best_score = 0.0

        for tag in self.tags:
            score = self._calculate_tag_score(content_lower, tag)
            if score > best_score:
                best_score = score
                best_tag = tag

        if best_tag and best_score >= self.config.confidence_threshold:
            section.tag = best_tag
            section.confidence = best_score
        else:
            # Default to task if it looks like an instruction
            if self._looks_like_instruction(content_lower):
                section.tag = get_tag_by_name("task")
                section.confidence = 0.4
            else:
                # Default to context for informational content
                section.tag = get_tag_by_name("context")
                section.confidence = 0.3

    def _calculate_tag_score(self, content: str, tag: XMLTag) -> float:
        """Calculate how well content matches a tag."""
        if not tag.keywords:
            return 0.0

        score = 0.0
        matches = 0

        for keyword in tag.keywords:
            if keyword.lower() in content:
                matches += 1
                # Bonus for keyword at start
                if content.startswith(keyword.lower()):
                    score += 0.2

        if matches > 0:
            # Base score from keyword matches
            score += min(matches * 0.15, 0.6)
            # Priority bonus
            score += (tag.priority / 100) * 0.2

        return min(score, 1.0)

    def _looks_like_instruction(self, content: str) -> bool:
        """Check if content looks like an instruction or command."""
        instruction_patterns = [
            r"^(please|could you|can you|i want|i need|help me)",
            r"^(create|write|generate|make|build|implement)",
            r"^(analyze|review|check|evaluate|assess)",
            r"^(explain|describe|summarize|list)",
            r"\?$",  # Questions
        ]
        return any(re.search(p, content) for p in instruction_patterns)

    def _build_hierarchy(self, sections: list[PromptSection]) -> list[PromptSection]:
        """Build hierarchical structure from flat sections."""
        # Group related sections (e.g., multiple examples under examples tag)
        result = []
        example_sections = []

        for section in sections:
            if section.tag and section.tag.name == "example":
                example_sections.append(section)
            else:
                if example_sections:
                    # Wrap collected examples
                    examples_tag = get_tag_by_name("examples")
                    parent = PromptSection(
                        content="",
                        tag=examples_tag,
                        confidence=0.9,
                        nested_sections=example_sections
                    )
                    result.append(parent)
                    example_sections = []
                result.append(section)

        if example_sections:
            examples_tag = get_tag_by_name("examples")
            parent = PromptSection(
                content="",
                tag=examples_tag,
                confidence=0.9,
                nested_sections=example_sections
            )
            result.append(parent)

        return result

    def _create_section(
        self,
        content: str,
        tag: Optional[XMLTag],
        confidence: float = 0.0
    ) -> PromptSection:
        """Create a PromptSection with the given parameters."""
        return PromptSection(
            content=content.strip(),
            tag=tag,
            confidence=confidence
        )

    def _create_custom_tag(self, name: str) -> XMLTag:
        """Create a custom tag for unrecognized labels."""
        return XMLTag(
            name=name,
            category=TagCategory.CONTEXT,
            description=f"Custom tag: {name}",
            priority=40
        )

    def convert_with_template(
        self,
        prompt: str,
        template: dict[str, str]
    ) -> "XMLifiedPrompt":
        """
        Convert a prompt using a predefined template mapping.

        Args:
            prompt: The prompt text
            template: Dict mapping section identifiers to tag names

        Returns:
            XMLifiedPrompt with sections tagged per template
        """
        sections = []
        for key, tag_name in template.items():
            if key in prompt:
                tag = get_tag_by_name(tag_name) or self._create_custom_tag(tag_name)
                sections.append(PromptSection(
                    content=prompt,
                    tag=tag,
                    confidence=1.0
                ))
                break

        if not sections:
            return self.convert(prompt)

        return XMLifiedPrompt(sections=sections, original=prompt)


@dataclass
class XMLifiedPrompt:
    """
    Result of prompt XMLification.

    Contains structured sections and provides methods for
    outputting in various formats.
    """

    sections: list[PromptSection]
    original: str

    def to_xml(self, include_wrapper: bool = False) -> str:
        """
        Convert to XML string format.

        Args:
            include_wrapper: Wrap all content in <prompt> tags

        Returns:
            XML-formatted prompt string
        """
        parts = [section.to_xml() for section in self.sections if section.tag]

        result = "\n\n".join(parts)

        if include_wrapper:
            return f"<prompt>\n{result}\n</prompt>"

        return result

    def to_dict(self) -> dict:
        """Convert to dictionary format."""
        return {
            "original": self.original,
            "sections": [
                {
                    "tag": s.tag.name if s.tag else None,
                    "category": s.tag.category.value if s.tag else None,
                    "content": s.content,
                    "confidence": s.confidence,
                    "nested": [
                        {"tag": n.tag.name, "content": n.content}
                        for n in s.nested_sections
                    ] if s.nested_sections else []
                }
                for s in self.sections
            ]
        }

    def get_sections_by_category(self, category: TagCategory) -> list[PromptSection]:
        """Get all sections of a specific category."""
        return [s for s in self.sections if s.tag and s.tag.category == category]

    def has_tag(self, tag_name: str) -> bool:
        """Check if a specific tag is present."""
        return any(s.tag and s.tag.name == tag_name for s in self.sections)
