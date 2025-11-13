"""
Tutorial: Word indexing (step 1)

Builds a tree-based index (nested dictionaries) from a list of words.
Usage:
    python script.py chat canard cane
"""

import sys


def add_word(index, word):
    """Add a single word into the index tree."""
    node = index
    for letter in word:
        if letter not in node:
            node[letter] = {}
        node = node[letter]


def build_index(words):
    """Build the full index tree from a list of words."""
    index = {}
    for word in words:
        add_word(index, word)
    return index


words = sys.argv[1:]
index = build_index(words)
print(index)


"""
Tutorial: Word indexing (step 2)

Reads one or more text files, extracts words, and builds a tree-based index (nested dictionaries) referencing which files contain each word.
Then allows the user to search for a word interactively.

Usage:
    python script.py file1.txt file2.txt ...
"""

import sys
import string


def add_word(index, word, filename):
    """Add a word into the index tree, referencing the file that contains it."""
    node = index
    for letter in word:
        if letter not in node:
            node[letter] = {}
        node = node[letter]

    # At the end of the word, record the filename
    if "files" not in node:
        node["files"] = []
    if filename not in node["files"]:
        node["files"].append(filename)


def build_index_from_files(filenames):
    """Read all files and build the full index tree."""
    index = {}
    for fname in filenames:
        try:
            with open(fname, "r", encoding="utf-8") as f:
                text = f.read().lower()
                for ch in string.punctuation:
                    text = text.replace(ch, " ")
                words = text.split()
                for word in words:
                    add_word(index, word, fname)
        except FileNotFoundError:
            print(f"File not found: {fname}")
    return index


def search_word(index, word):
    """Return the list of files containing a given word, or None if not found."""
    node = index
    for letter in word:
        if letter not in node:
            return None
        node = node[letter]
    return node.get("files", [])


files = sys.argv[1:]
index = build_index_from_files(files)


while True:
    query = input("\nEnter a word to search (or 'quit' to exit): ").lower()
    if query == "quit":
        break

    result = search_word(index, query)
    if not result:
        print(f"'{query}' not found in any file.")
    else:
        print(f"'{query}' found in: {result}")