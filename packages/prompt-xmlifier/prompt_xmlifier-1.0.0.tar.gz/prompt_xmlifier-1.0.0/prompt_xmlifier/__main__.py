"""
Entry point for running prompt_xmlifier as a module.

Usage:
    python -m prompt_xmlifier "Your prompt here"
    python -m prompt_xmlifier --file prompt.txt
    python -m prompt_xmlifier --interactive
"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
