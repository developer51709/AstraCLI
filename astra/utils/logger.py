import os
import sys

try:
    import colorama
    colorama.init()
    COLORAMA = True
except Exception:
    COLORAMA = False

USE_COLOR = os.environ.get("ASTRA_NO_COLOR", "0") != "1"

RESET = "\x1b[0m"
COLORS = {
    "grey": "\x1b[90m",
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "blue": "\x1b[34m",
    "magenta": "\x1b[35m",
    "cyan": "\x1b[36m",
    "white": "\x1b[37m",
}


def _color(text, color):
    if not USE_COLOR:
        return text
    code = COLORS.get(color, "")
    return f"{code}{text}{RESET}"


def info(msg):
    print(_color("[astra] ", "cyan") + str(msg))


def success(msg):
    print(_color("[astra] ", "green") + str(msg))


def warn(msg):
    print(_color("[astra] ", "yellow") + str(msg))


def error(msg):
    print(_color("[astra] ERROR: ", "red") + str(msg), file=sys.stderr)


def debug(msg):
    if os.environ.get("ASTRA_DEBUG"):
        print(_color("[astra DEBUG] ", "magenta") + str(msg))
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("astra")
