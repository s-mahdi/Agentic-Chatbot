#!/usr/bin/env python3
"""Simple startup script for the agentic chatbot."""

import sys
from pathlib import Path

# Add src to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

# Import and run the main function
from agentic_chatbot.__main__ import main

if __name__ == "__main__":
    main()
