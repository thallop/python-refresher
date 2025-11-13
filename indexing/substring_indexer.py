"""
Tutorial: Recursive substring indexing and search

Recursively explores a directory, indexes all substrings found in text files, and allows the user to search for any character sequence. Displays matching files and lines (found on demand).
"""

import os
import sys
import string


def explore(rep, file_list):
    """Recursively explore directory 'rep' and collect text file paths."""
    try:
        items = os.listdir(rep)
    except PermissionError:
        return

    for item in items:
        path = os.path.join(rep, item)
        if os.path.isdir(path):
            explore(path, file_list)
        else:
            if path.endswith((".txt", ".py", ".md", ".csv", ".ipynb")):
                file_list.append(path)


def add_word(index, word, filename):
    """Add a string fragment into the index tree."""
    node = index
    for letter in word:
        if letter not in node:
            node[letter] = {}
        node = node[letter]

    if "files" not in node:
        node["files"] = []
    if filename not in node["files"]:
        node["files"].append(filename)


def build_index_from_files(file_list):
    """Build index of all substrings from text content of files."""
    index = {}
    for fname in file_list:
        try:
            with open(fname, "r", encoding="utf-8") as f:
                text = f.read().lower()
                for ch in string.punctuation:
                    text = text.replace(ch, " ")
                words = text.split()
                unique_words = set(words)
                for word in unique_words:
                    # add all possible substrings of the word
                    for i in range(len(word)):
                        for j in range(i + 1, len(word) + 1):
                            fragment = word[i:j]
                            add_word(index, fragment, fname)
        except (UnicodeDecodeError, FileNotFoundError):
            continue
    return index


def search_word(index, fragment):
    """Return files that contain the given substring fragment."""
    node = index
    for letter in fragment:
        if letter not in node:
            return []
        node = node[letter]
    return node.get("files", [])


def search_in_files(fragment, files):
    """Search for the fragment inside the listed files and print matches."""
    for fname in files:
        try:
            with open(fname, "r", encoding="utf-8") as f:
                for num, line in enumerate(f, start=1):
                    if fragment in line.lower():
                        print(f"- {fname} (line {num}): {line.strip()}")
        except Exception:
            pass


root = sys.argv[1]

print(f"Exploring directory: {root}")
file_list = []
explore(root, file_list)
print(f"Found {len(file_list)} text files.")
print("Building substring index...")

index = build_index_from_files(file_list)
print("Index built successfully.")

while True:
    query = input("\nEnter a string to search (or 'quit' to exit): ").lower()
    if query == "quit":
        break

    files = search_word(index, query)
    if not files:
        print(f"No occurrences of '{query}' found.")
    else:
        print(f"\n'{query}' found in {len(files)} file(s):")
        search_in_files(query, files)