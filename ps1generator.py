try:
    from readchar import readkey, key
except ModuleNotFoundError:
    print("\033[31m\033[7mERROR\033[0m Module \033[36mreadchar\033[0m is not installed. Install it using \033[36mpython3 -m pip install readchar\033[0m")
    exit(1)

import getpass
import os
import string
from datetime import datetime

def addstr(string):
    print(string, end="", flush=True)

entered = ""
x = 0
y = 0
k = ""

MAP = {
    "bold": (r"\[\033[1m\]", "\033[1m"),
    "dim": (r"\[\033[2m\]", "\033[2m"),
    "italic": (r"\[\033[3m\]", "\033[3m"),
    "underline": (r"\[\033[4m\]", "\033[4m"),
    "blinking": (r"\[\033[5m\]", "\033[5m"),
    "inverse": (r"\[\033[7m\]", "\033[7m"),
    "hidden": (r"\[\033[8m\]", "\033[8m"),
    "strikethrough": (r"\[\033[9m\]", "\033[9m"),
    "blackfg": (r"\[\033[30m\]", "\033[30m"),
    "redfg": (r"\[\033[31m\]", "\033[31m"),
    "greenfg": (r"\[\033[32m\]", "\033[32m"),
    "yellowfg": (r"\[\033[33m\]", "\033[33m"),
    "bluefg": (r"\[\033[34m\]", "\033[34m"),
    "magentafg": (r"\[\033[35m\]", "\033[35m"),
    "cyanfg": (r"\[\033[36m\]", "\033[36m"),
    "whitefg": (r"\[\033[37m\]", "\033[37m"),
    "defaultfg": (r"\[\033[39m\]", "\033[39m"),
    "blackbg": (r"\[\033[40m\]", "\033[40m"),
    "redbg": (r"\[\033[41m\]", "\033[41m"),
    "greenbg": (r"\[\033[42m\]", "\033[42m"),
    "yellowbg": (r"\[\033[43m\]", "\033[43m"),
    "bluebg": (r"\[\033[44m\]", "\033[44m"),
    "magentabg": (r"\[\033[45m\]", "\033[45m"),
    "cyanbg": (r"\[\033[46m\]", "\033[46m"),
    "whitebg": (r"\[\033[47m\]", "\033[47m"),
    "defaultbg": (r"\[\033[49m\]", "\033[49m"),
    "username": (r"\u", getpass.getuser()),
    "hostname-short": (r"\h", "mycomputer"),
    "hostname-full": (r"\H", "mycomputer.example"),
    "shellname": (r"\v", "bash"),
    "reset": (r"\[\033[0m\]", "\033[0m"),
    "cwd": (r"\w", os.getcwd()),
    "time": (r"\t", datetime.now().strftime("%H:%M:%S")),
    "date": (r"\d", datetime.now().strftime("%Y-%m-%d")),
    "exitstatus": (r"$?", "0"),
    "newline": (r"\n", "\n"),
    "[": (r"[", "["),
    "]": (r"]", "]"),
}

OPTIONS = [
    ["", "Type>"],
    ["style", "bold", "dim", "italic", "underline", "blinking", "inverse", "hidden", "strikethrough"],
    ["colorfg", "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "default"],
    ["colorbg", "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white", "default"],
    ["name", "username", "hostname-short", "hostname-full", "shellname"],
    ["misc", "reset", "cwd", "time", "date", "exitstatus"],
    ["chars", "newline", "[", "]"]
]

def process(string):
    raw = preview = ""
    opened = False
    escape = ""
    for char in string:
        if opened:
            if char == "]":
                opened = False
                if escape in MAP:
                    raw += MAP[escape][0]
                    preview += MAP[escape][1]
                else:
                    raw += "[" + escape + "]"
                    preview += "[" + escape + "]"
                continue
            escape += char
        else:
            if char == "[":
                opened = True
                escape = ""
                continue
            raw += char
            preview += char
    return raw, preview

addstr("\033c")
try:
    while True:
        if y == 0:
            if k == key.DOWN:
                y += 1
            elif k in string.printable and k != key.ENTER:
                entered += k
            elif k == key.BACKSPACE:
                entered = entered[:-1]
        else:
            if k == key.UP:
                y -= 1
            elif k == key.RIGHT:
                x += 1
            elif k == key.LEFT:
                x -= 1
            elif k == key.DOWN:
                y += 1
            y = max(0, min(len(OPTIONS)-1, y))
            x = max(0, min(len(OPTIONS[y])-2, x))
            if k in (key.ENTER, key.SPACE):
                entered += f"[{OPTIONS[y][x+1]}{OPTIONS[y][0][-2:] if y in range(2, 4) else ''}]"
        save = "PS1 Generator\n"
            
        for _y, row in enumerate(OPTIONS):
            save += "\n"
            for _x, col in enumerate(row):
                if _x - 1 == x and _y == y:
                    save += "\033[7m"
                save += col+"\033[0m"
                save += "\t" if _x == 0 and _y != 0 else "  "

        p = process(entered)
        save += f"""

\033[33mCopy:\033[0m
PS1="{p[0]}"

\033[32mPreview:\033[0m
{p[1]}"""

        save += "\033[3;8H\033[0m"+entered
        addstr("\033c"+save)
        k = readkey()
        if k in (key.ESC, key.CTRL_C): # Windows
            raise KeyboardInterrupt

except KeyboardInterrupt:
    addstr("\033c")
    exit(0)
