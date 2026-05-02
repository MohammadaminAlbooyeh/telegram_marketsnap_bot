#!/usr/bin/env python3
"""Handler module entry point: python3 -m handlers"""

import sys
from pathlib import Path

# Ensure project root is in path
sys.path.insert(0, str(Path(__file__).parent))

if __name__ == "__main__":
    from handlers import *
    print("Handler modules loaded:", __all__)
