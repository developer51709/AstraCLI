import sys
import shlex
from astra.core.dispatcher import dispatch
from astra.utils import logger


def _repl():
    logger.info("Entering interactive mode. Type 'exit' or 'quit' to leave.")
    try:
        while True:
            try:
                line = input(_prompt())
            except EOFError:
                break
            if not line:
                continue
            parts = shlex.split(line)
            if not parts:
                continue
            cmd = parts[0]
            if cmd in ("exit", "quit"):
                break
            dispatch(cmd, parts[1:])
    except KeyboardInterrupt:
        logger.info("Exiting interactive mode.")


def _prompt():
    return "astra> "


def main():
    if len(sys.argv) < 2:
        logger.info("AstraCLI: No command provided.")
        dispatch("help", [])
        return

    if sys.argv[1] in ("interactive", "-i", "--interactive"):
        _repl()
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    dispatch(command, args)
