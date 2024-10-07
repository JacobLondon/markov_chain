from collections import defaultdict
import textwrap
import re
import itertools
import random
import sys

class MarkovChain:
    def __init__(self, text):
        self.text: str = text

        # Remove punctuation
        REMOVE = r"'*`()"
        for ch in REMOVE:
            self.text = self.text.replace(ch, "")

        # Lowercase it all
        self.text = self.text.lower()

        # Separate words
        self.words = self.text.split()

        # Group
        self.groupings = defaultdict(list)
        for a, b in itertools.pairwise(self.words):
            self.groupings[a].append(b)

    def get(self, a):
        hitlist = self.groupings.get(a, None)
        if hitlist is None: return ""
        return random.choice(hitlist)

# https://stackoverflow.com/questions/66086822/how-to-justify-text-right-alignment-in-python
def justify(txt:str, width:int) -> str:
    prev_txt = txt
    while((l:=width-len(txt))>0):
        txt = re.sub(r"(\s+)", r"\1 ", txt, count=l)
        if(txt == prev_txt): break
    return txt.rjust(width)

def arg_get(search, container, default):
    for i, value in enumerate(container):
        if search == value and i+1 < len(container):
            return container[i+1]
    return default

def main():
    filename = arg_get("-f", sys.argv, None)
    if filename is None:
        print("ERROR: -f FILENAME required")
        exit(1)

    start = arg_get("--search", sys.argv, "oh")
    start = start.lower()

    count = arg_get("--count", sys.argv, "10")
    count = int(count)

    lines = arg_get("--lines", sys.argv, "1")
    lines = int(lines)

    with open(filename, "r") as fp:
        text = fp.read()

    # Generate next words based on the initial from the text
    m = MarkovChain(text)
    builder = []
    current = start
    for _ in range(lines):
        for _ in range(count):
            builder.append(current)
            current = m.get(current)

    # for spacing
    WORD_LENGTH_FUDGE = 1.33
    average_word_length = int(sum(map(lambda word: len(word), builder)) / len(builder) * WORD_LENGTH_FUDGE)

    # And pretty print :)
    formatted = textwrap.fill(" ".join(builder), width=count * average_word_length)
    for line in formatted.splitlines():
        print(justify(line, count * average_word_length))

    exit(0)

if __name__ == '__main__':
    main()
