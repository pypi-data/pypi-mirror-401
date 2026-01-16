import argparse
from . import greet

def main() -> None:
    parser = argparse.ArgumentParser(prog="packaging_workshop_pmat")
    parser.add_argument("name", help="Name to greet")
    args = parser.parse_args()
    print(greet(args.name))
