def del_garbage(text: str) -> str:
    out = ""

    for i, char in enumerate(text):
        if not char in "\t\n ":
            out += text[i:]
            break

    i = len(out)
    while i > 1:
        i -= 1
        char = out[i]
        if not char in "\n\t ":
            return out[:i + 1]
    return out

def sum_paths(*paths: str) -> str:
    out = ""
    for path in paths:
        if len(path) > 0:
            if del_garbage(path).replace("/", "\\")[-1] == "\\":
                out += del_garbage(path).replace("/", "\\")
            else:
                out += del_garbage(path).replace("/", "\\") + "\\"
    return out[:-1]

def split_first(text: str, char: str) -> tuple[str, str]:
    return text.split(char)[0], char.join(text.split(char)[1:])

def split_last(text: str, char: str) -> tuple[str, str]:
    return char.join(text.split(char)[:-1]), text.split(char)[-1]