import asyncio
import sys
import os

# Ensure the package directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from devai import run

def main():
    try:
        # Use Windows Proactor loop / Selector loop fix if needed
        if sys.platform == "win32":
             asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(run())
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
