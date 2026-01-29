import argparse
from .project import cre_prj

def main():
    parser = argparse.ArgumentParser(prog="tyc-e")
    sub = parser.add_subparsers(dest="command")

    sp = sub.add_parser("cre_prj")
    sp.add_argument("name")

    args = parser.parse_args()

    if args.command == "cre_prj":
        cre_prj(args.name)
