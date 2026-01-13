import sys
from src.TYC_ENGINE.assets.lib_assets.py_assets.core import render, run

def main():
    if len(sys.argv) < 2:
        print("Usage: tyc-engine run")
        return

    if sys.argv[1] == "run":
        render()
        run()
