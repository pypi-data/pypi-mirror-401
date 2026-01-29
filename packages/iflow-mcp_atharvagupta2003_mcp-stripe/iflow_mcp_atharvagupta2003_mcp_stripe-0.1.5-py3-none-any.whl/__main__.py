#!/usr/bin/env python3
import asyncio
import sys
import os

# Add current directory to path to import server module
sys.path.insert(0, os.path.dirname(__file__))

from server import main as _main

def main():
    """Entry point for the MCP server"""
    asyncio.run(_main())

if __name__ == "__main__":
    main()