#!/usr/bin/env python3
"""Module entry point: python3 -m app"""

import sys
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import main

if __name__ == "__main__":
    main()
