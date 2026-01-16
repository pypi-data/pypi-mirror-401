import sys
from zoulib import __version__

def main():
    args = sys.argv[1:]
    if args and args[0] in ("--version", "--v", "--ver"):
        print(f"zoulib version {__version__}")
    else:
        print("Использование: zoulib [--version | --v | --ver]")
