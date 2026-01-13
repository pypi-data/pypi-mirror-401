import os.path
from inspect import currentframe, getframeinfo
import inspect

# Configuration dictionary; just tweak values here
config = {
    "DEBUG": True,
    "COLORSFORDEBUG": True,
    "SEP": False,
    "SEPSTYLE": "|",
    "MSGFORDEBUG": True,
    "MESSAGE": "INFO:",
    "COLOR": "",
    "TIMESTAMP": False,
    "FILELINE": False,
    "FILELINEARGS": 1
}

_start_message_shown = False

def colorize(text, color):
    # Simple ANSI color wrapper.
    colors = {
        # Standard colors
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",

        # Bright colors
        "bright_black": "\033[90m",
        "bright_red": "\033[91m",
        "bright_green": "\033[92m",
        "bright_yellow": "\033[93m",
        "bright_blue": "\033[94m",
        "bright_magenta": "\033[95m",
        "bright_cyan": "\033[96m",
        "bright_white": "\033[97m",

        # Additional accent colors
        "orange": "\033[38;5;208m",
        "pink": "\033[38;5;213m",
        "purple": "\033[38;5;141m",
        "light_blue": "\033[38;5;81m",
        "teal": "\033[38;5;37m",
        "lime": "\033[38;5;118m",
        "light_gray": "\033[38;5;250m",
        "dark_gray": "\033[38;5;239m",

        # Reset
        "reset": "\033[0m"
    }
    return f"{colors.get(color,'')}{text}{colors.get('reset','')}" if color else text

def current_time():
    """Return current HH:MM:SS string."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

def get_line(frames_back=2, folders=7):
    # Go up the stack
    frame = currentframe()
    for _ in range(frames_back):
        frame = frame.f_back

    info = getframeinfo(frame)
    path_parts = os.path.normpath(info.filename).split(os.sep)

    # Take only the last folders parts
    displayed_path = os.path.join(*path_parts[-folders:])

    return f"{displayed_path}:{info.lineno}"

def tprint(*args, message=None):
    global _start_message_shown

    # Get variable names from the call
    frame = inspect.currentframe().f_back
    line = inspect.getframeinfo(frame).code_context[0]
    inside = line[line.find("(")+1 : line.rfind(")")]
    names = [x.strip() for x in inside.split(",")]

    # Pull config values once
    DEBUG = config.get("DEBUG", True)
    COLORSFORDEBUG = config.get("COLORSFORDEBUG", True)
    SEP = config.get("SEP", False)
    SEPSTYLE = config.get("SEPSTYLE", "|")
    MSGFORDEBUG = config.get("MSGFORDEBUG", True)
    MESSAGE = config.get("MESSAGE", "INFO:")
    GLOBALCOLOR = config.get("COLOR", "")
    TIMESTAMP = config.get("TIMESTAMP", False)
    FILELINE = config.get("FILELINE", False)
    FILELINEARGS = config.get("FILELINEARGS", (2, 7))

    # Build variable/value strings
    parts = [f"{name} = {value}" if DEBUG else str(value) for name, value in zip(names, args)]

    # Join with separator
    sep_str = f" {SEPSTYLE} " if SEP else " "
    output = sep_str.join(parts)

    # Prepend message once at the start
    final_message = message if message is not None else (MESSAGE if MSGFORDEBUG and not _start_message_shown else "")
    if final_message:
        output = f"{final_message} {output}"
        if MSGFORDEBUG:
            _start_message_shown = True

    # Optional timestamp
    if TIMESTAMP:
        output = f"[{current_time()}] {output}"

    if FILELINE:
        output = f"[{get_line(*FILELINEARGS)}] {output}"

    if COLORSFORDEBUG:
        if DEBUG:
            output = colorize(output, "bright_yellow")

    # Optional color
    output = colorize(output, GLOBALCOLOR)

    # Print the final string
    print(output)
