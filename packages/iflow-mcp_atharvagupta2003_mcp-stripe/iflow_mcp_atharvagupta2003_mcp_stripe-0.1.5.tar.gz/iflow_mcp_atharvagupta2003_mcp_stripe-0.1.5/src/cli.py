#!/usr/bin/env python3
"""CLI entry point for the MCP Stripe server"""
import asyncio
from server import main

def main_cli():
    """Entry point for the MCP server"""
    asyncio.run(main())

if __name__ == "__main__":
    main_cli()