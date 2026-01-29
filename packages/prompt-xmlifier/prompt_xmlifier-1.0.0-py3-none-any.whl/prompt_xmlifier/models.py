"""
Data models for Prompt XMLifier.

Defines core structures for XML tags and prompt sections
following Anthropic's official prompt engineering guidelines.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TagCategory(Enum):
    """Categories of XML tags based on their purpose in prompts."""

    DIRECTIVE = "directive"      # What to do: task, instructions, do, do_not
    CONTEXT = "context"          # Background: context, background, situation
    INPUT = "input"              # Data to process: input, data, document, code
    OUTPUT = "output"            # Expected results: output, format, structure
    CONSTRAINT = "constraint"    # Limitations: constraints, rules, boundaries
    PERSONA = "persona"          # Identity: role, tone, audience
    LEARNING = "learning"        # Examples: example, examples, few_shot
    REASONING = "reasoning"      # Thinking: thinking, reasoning, analysis


@dataclass
class XMLTag:
    """
    Represents an XML tag for prompt structuring.

    Attributes:
        name: The tag name (e.g., 'task', 'context', 'instructions')
        category: The functional category of the tag
        description: What content this tag should contain
        keywords: Trigger words that indicate this tag should be used
        priority: Higher priority tags are matched first (0-100)
    """

    name: str
    category: TagCategory
    description: str
    keywords: list[str] = field(default_factory=list)
    priority: int = 50

    def wrap(self, content: str, indent: int = 0) -> str:
        """Wrap content in this XML tag with optional indentation."""
        indent_str = "  " * indent
        lines = content.strip().split("\n")
        indented_content = "\n".join(f"{indent_str}  {line}" if line.strip() else "" for line in lines)
        return f"{indent_str}<{self.name}>\n{indented_content}\n{indent_str}</{self.name}>"


@dataclass
class PromptSection:
    """
    Represents a detected section within a prompt.

    Attributes:
        content: The raw text content of the section
        tag: The XML tag assigned to this section
        confidence: How confident we are in the tag assignment (0.0-1.0)
        start_pos: Starting position in original text
        end_pos: Ending position in original text
        nested_sections: Child sections for hierarchical structure
    """

    content: str
    tag: Optional["XMLTag"] = None
    confidence: float = 0.0
    start_pos: int = 0
    end_pos: int = 0
    nested_sections: list["PromptSection"] = field(default_factory=list)

    def to_xml(self, indent: int = 0) -> str:
        """Convert this section to XML format."""
        if self.tag is None:
            return self.content
        if self.nested_sections:
            indent_str = "  " * indent
            nested_xml = "\n".join(
                section.to_xml(indent + 1)
                for section in self.nested_sections
            )
            return f"{indent_str}<{self.tag.name}>\n{nested_xml}\n{indent_str}</{self.tag.name}>"
        return self.tag.wrap(self.content, indent)


# Standard XML tags based on Anthropic documentation and best practices
STANDARD_TAGS: list[XMLTag] = [
    # Directive tags (what to do)
    XMLTag(
        name="task",
        category=TagCategory.DIRECTIVE,
        description="The main task or objective to accomplish",
        keywords=["task", "goal", "objective", "want to", "need to", "please", "help me"],
        priority=90
    ),
    XMLTag(
        name="instructions",
        category=TagCategory.DIRECTIVE,
        description="Step-by-step directions for completing the task",
        keywords=["instructions", "steps", "directions", "how to", "procedure", "process"],
        priority=85
    ),
    XMLTag(
        name="do",
        category=TagCategory.DIRECTIVE,
        description="Actions that should be performed",
        keywords=["do", "must", "should", "always", "ensure", "make sure"],
        priority=70
    ),
    XMLTag(
        name="do_not",
        category=TagCategory.DIRECTIVE,
        description="Actions that should be avoided",
        keywords=["don't", "do not", "never", "avoid", "must not", "should not", "forbidden"],
        priority=75
    ),

    # Context tags (background information)
    XMLTag(
        name="context",
        category=TagCategory.CONTEXT,
        description="Background information and situational context",
        keywords=["context", "background", "situation", "scenario", "given that", "considering"],
        priority=80
    ),
    XMLTag(
        name="background",
        category=TagCategory.CONTEXT,
        description="Historical or explanatory background",
        keywords=["background", "history", "previously", "before this"],
        priority=60
    ),

    # Input tags (data to process)
    XMLTag(
        name="input",
        category=TagCategory.INPUT,
        description="Data or content to be processed",
        keywords=["input", "data", "given", "provided", "here is", "following"],
        priority=70
    ),
    XMLTag(
        name="document",
        category=TagCategory.INPUT,
        description="Document content to analyze or process",
        keywords=["document", "text", "article", "content", "file", "source"],
        priority=65
    ),
    XMLTag(
        name="code",
        category=TagCategory.INPUT,
        description="Code snippets or programming content",
        keywords=["code", "script", "function", "class", "program", "snippet"],
        priority=75
    ),
    XMLTag(
        name="data",
        category=TagCategory.INPUT,
        description="Raw data for processing",
        keywords=["data", "dataset", "records", "values", "numbers"],
        priority=60
    ),

    # Output tags (expected results)
    XMLTag(
        name="output",
        category=TagCategory.OUTPUT,
        description="Expected output structure or content",
        keywords=["output", "result", "response", "return", "produce", "generate"],
        priority=70
    ),
    XMLTag(
        name="format",
        category=TagCategory.OUTPUT,
        description="Formatting rules for the output",
        keywords=["format", "formatting", "structure", "layout", "style", "template"],
        priority=65
    ),

    # Constraint tags (limitations)
    XMLTag(
        name="constraints",
        category=TagCategory.CONSTRAINT,
        description="Limitations and boundaries to respect",
        keywords=["constraints", "limitations", "limits", "boundaries", "restrictions", "bounds"],
        priority=70
    ),
    XMLTag(
        name="rules",
        category=TagCategory.CONSTRAINT,
        description="Mandatory rules to follow",
        keywords=["rules", "requirements", "mandatory", "required", "must follow"],
        priority=75
    ),

    # Persona tags (identity and style)
    XMLTag(
        name="role",
        category=TagCategory.PERSONA,
        description="The role or persona to assume",
        keywords=["role", "act as", "you are", "persona", "character", "expert"],
        priority=85
    ),
    XMLTag(
        name="tone",
        category=TagCategory.PERSONA,
        description="The writing style and tone to use",
        keywords=["tone", "style", "voice", "manner", "approach", "writing style"],
        priority=60
    ),
    XMLTag(
        name="audience",
        category=TagCategory.PERSONA,
        description="The target audience for the output",
        keywords=["audience", "reader", "user", "target", "for whom", "intended for"],
        priority=55
    ),

    # Learning tags (examples)
    XMLTag(
        name="example",
        category=TagCategory.LEARNING,
        description="A single example for few-shot learning",
        keywords=["example", "for example", "such as", "like this", "instance"],
        priority=70
    ),
    XMLTag(
        name="examples",
        category=TagCategory.LEARNING,
        description="Multiple examples for few-shot learning",
        keywords=["examples", "samples", "demonstrations", "cases"],
        priority=75
    ),

    # Reasoning tags
    XMLTag(
        name="thinking",
        category=TagCategory.REASONING,
        description="Request for step-by-step reasoning",
        keywords=["thinking", "think", "reason", "analyze", "consider", "step by step"],
        priority=65
    ),
    XMLTag(
        name="analysis",
        category=TagCategory.REASONING,
        description="Analytical breakdown or evaluation",
        keywords=["analysis", "analyze", "evaluate", "assess", "examine"],
        priority=60
    ),
]


def get_tag_by_name(name: str) -> Optional[XMLTag]:
    """Retrieve a standard tag by its name."""
    for tag in STANDARD_TAGS:
        if tag.name == name:
            return tag
    return None


def get_tags_by_category(category: TagCategory) -> list[XMLTag]:
    """Retrieve all standard tags in a given category."""
    return [tag for tag in STANDARD_TAGS if tag.category == category]
