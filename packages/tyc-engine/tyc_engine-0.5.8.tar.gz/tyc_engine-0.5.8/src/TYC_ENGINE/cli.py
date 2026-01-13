import sys
from .window import render, run

def main():
    if len(sys.argv) < 2:
        print("Usage: tyc-engine run")
        return

    if sys.argv[1] == "run":
        render()
        run()
