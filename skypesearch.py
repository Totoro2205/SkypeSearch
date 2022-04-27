import asyncio
import sys
import os

from modules.search import search

if __name__ == "__main__":

    if len(sys.argv) < 2:
        data = None
    else:
        data = ' '.join(sys.argv[1:])

    with open('token.txt', 'r') as f:
        token = f.read().strip()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(search(data, token))
