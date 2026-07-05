import sys
from astra.core.dispatcher import dispatch

def main():
    if len(sys.argv) < 2:
        print("AstraCLI: No command provided.")
        dispatch("help", [])
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    dispatch(command, args)
