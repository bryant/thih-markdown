from textwrap import dedent
import re

UNCOMMENTED = open("_thih_ref.lhs").read()

def hash_to_uline(src):
    STYLES = ["=", "=", "-", "-"]

    def subit(m):
        newhd = m.group(0).strip("#").strip(" ")
        lvl = len(m.group(1)) - 1
        if lvl < len(STYLES):
            return underline_header(newhd, char=STYLES[lvl])
        return m.group(0)

    return re.sub(r"^(#+).*$", subit, src, flags=re.MULTILINE)

def trim_lines(src):
    return re.sub(r"[ \t]+$", "", src, flags=re.MULTILINE)

def shrink_empty_lines(src):
    return re.sub(r"\n{3,}", "\n\n", src, flags=re.MULTILINE)

def bye_dos(src): return src.replace("\r", "")

def lhsify(src):
    def lhs(m):
        code = dedent(m.group(0)).strip()
        bird = "> " if code in UNCOMMENTED else ""
        code = re.sub("^", bird, code, flags=re.MULTILINE)
        return "\n\n```lhs\n\n" + code + "\n\n```\n\n"

    return re.sub(r"\n(?:(?:^[ ]{6}.*\n)+\n)+", lhs, src, flags=re.MULTILINE)

def underline_header(hd, char="-"):
    return hd + "\n" + char*len(hd)

if __name__ == "__main__":
    from html2text import HTML2Text
    from sys import stdin

    h = HTML2Text()
    h.body_width = 0
    src = h.handle(stdin.read().decode('windows-1252'))
    passes = (
        bye_dos,
        trim_lines,
        shrink_empty_lines,
        hash_to_uline,
        lhsify
    )

    for pass_ in passes:
        src = pass_(src)
    print src.encode('utf-8')
