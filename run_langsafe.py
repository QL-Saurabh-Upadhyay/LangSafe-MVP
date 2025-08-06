#!/usr/bin/env python3
"""
Simple startup script for LangSafe API server.
"""
import sys
import os

# Add src to a Python path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == "__main__":
    from langsafe.main import main
    main() 