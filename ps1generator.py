try:
    from readchar import readkey, key
except ModuleNotFoundError:
    print("\033[31m\033[7mERROR\033[0m Module \033[36mreadchar\033[0m is not installed. Install it using \033[36mpython3 -m pip install readchar\033[0m")
    exit(1)

import string
def addstr(string):
    print(string, end="", flush=True)

save = ""
entered = ""
mode = 0 # 0=input 1=menu
x = 0
y = 0
k = ""

MAP = {
    "bold": r"\[\033[1m\]",
    "dim\]": r"\[\033[2m\]",
    "italic": r"\[\033[3m\]",
    "underline": r"\[\033[4m\]",
    "blinking": r"\[\033[5m\]",
    "inverse": r"\[\033[7m\]",
    "hidden": r"\[\033[8m\]",
    "strikethrough": r"\[\033[9m\]",
    "blackfg": r"\[\033[30m\]",
    "redfg": r"\[\033[31m\]",
    "greenfg": r"\[\033[32m\]",
    "yellowfg": r"\[\033[33m\]",
    "bluefg": r"\[\033[34m\]",
    "magentafg": r"\[\033[35m\]",
    "cyanfg": r"\[\033[36m\]",
    "whitefg": r"\[\033[37m\]",
    "defaultbg": r"\[\033[49m\]",
    "blackbg": r"\[\033[40m\]",
    "redbg": r"\[\033[41m\]",
    "greenbg": r"\[\033[42m\]",
    "yellowbg": r"\[\033[43m\]",
    "bluebg": r"\[\033[44m\]",
    "magentabg": r"\[\033[45m\]",
    "cyanbg": r"\[\033[46m\]",
    "whitebg": r"\[\033[47m\]",
    "defaultbg": r"\[\033[49m\]",
    "username": r"\u",
    "hostname-short": r"\h",
    "hostname-full": r"\H",
    "shellname": r"\v",
    "reset": r"\[\033[0m\]",
    "cwd": r"\w",
    "time": r"\t",
    "date": r"\d",
    "exitstatus": r"$?",
    "newline": r"\n",
    "[": "[",
    "]": "]"
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
    res = ""
    opened = False
    escape = ""
    for char in string:
        if opened:
            if char == "]":
                opened = False
                res += MAP[escape]
                continue
            escape += char
        else:
            if char == "[":
                opened = True
                escape = ""
                continue
            res += char
    return res

addstr("\033c")
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
    if k == key.ESC:
        exit(0)
        
    for _y, row in enumerate(OPTIONS):
        save += "\n"
        for _x, col in enumerate(row):
            if _x - 1 == x and _y == y:
                save += "\033[7m"
            save += col+"\033[0m"
            save += "\t" if _x == 0 and _y != 0 else "  "

    p = process(entered)
    save += "\nCopy:\n" + p
    save += "\n\nPreview (inaccurate):\n"

    exec(f"globals()['save'] += '{p}'")

    save += "\033[3;8H\033[0m"+entered
    addstr("\033c"+save)
    k = readkey()
