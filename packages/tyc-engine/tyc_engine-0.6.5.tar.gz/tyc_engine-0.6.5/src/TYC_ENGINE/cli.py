import argparse
from .project import startproject

def main():
    parser = argparse.ArgumentParser(prog="tyc-eng")
    sub = parser.add_subparsers(dest="command")

    sp = sub.add_parser("cre_proj")
    sp.add_argument("name")

    args = parser.parse_args()

    if args.command == "startproject":
        startproject(args.name)
