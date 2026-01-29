#!/usr/bin/env python3
import asyncio
import sys
import os

# Add current directory to path to import server module
sys.path.insert(0, os.path.dirname(__file__))

from server import main

asyncio.run(main())