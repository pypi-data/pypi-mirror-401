import argparse
from .project import startproject

def main():
    parser = argparse.ArgumentParser(prog="tyc-engine")
    sub = parser.add_subparsers(dest="command")

    sp = sub.add_parser("startproject")
    sp.add_argument("name")

    args = parser.parse_args()

    if args.command == "startproject":
        startproject(args.name)
