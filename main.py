import asyncio
import sys
import os
from pathlib import Path

from modules.search import search

if __name__ == "__main__":
    modules = ["search"]

    if len(sys.argv) <= 1 or sys.argv[1].lower() not in modules:
        print("Please choose a module.\n")
        print("Available modules :")
        for module in modules:
            print(f"- {module}")
        exit()

    with open('token.txt', 'r', encoding='utf-8') as f:
        token = f.read().strip()

    module = sys.argv[1].lower()
    if len(sys.argv) >= 3:
        data = sys.argv[2]
    else:
        data = None

    loop = asyncio.get_event_loop()
    if module == "search":
        loop.run_until_complete(search(data, token))
