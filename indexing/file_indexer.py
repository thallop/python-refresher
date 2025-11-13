"""
Tutorial: File indexing and search

Recursively explores a directory, indexes files by extension, and lets the user search for text in selected file types.
"""

import os
import sys


def explore(rep):
    """Recursive function that explores a directory and prints its files."""
    print("I am in " + rep)
    items = os.listdir(rep)
    
    for item in items:
        path = os.path.join(rep, item)
        if os.path.isdir(path):
            explore(path)
        else:
            print("  File:", path)


os.system('clear')
explore(sys.argv[1])


def explore(rep, index):
    """Recursive function that explores a directory and indexes files by extension."""
    print("I am in " + rep)
    items = os.listdir(rep)

    for item in items:
        path = os.path.join(rep, item)
        if os.path.isdir(path):
            explore(path, index)
        else:
            parts = item.split(".")
            if len(parts) == 1:
                ext = "no suffix"
            else:
                ext = "." + parts[-1]

            if ext not in index:
                index[ext] = [path]
            else:
                index[ext].append(path)


index = {}
explore(sys.argv[1], index)

total = 0
print("\n--- File index by extension ---")
for ext, files in sorted(index.items()):
    print(f"{ext} : {len(files)} file(s)")
    for f in files:
        print(f"  - {f}")
    total += len(files)
print(f"TOTAL: {total}")


while True:
    pattern = input("\nEnter a search string (or 'quit' to stop): ")
    if pattern.lower() == "quit":
        break

    exts = input("Enter file extensions to search (e.g. .py .txt .java): ").split()
    if not exts:
        print("No extensions given.")
        continue

    print(f"\nSearching for '{pattern}' in files with extensions {exts}...\n")

    for ext in exts:
        if ext not in index:
            continue
        for file_path in index[ext]:
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f, start=1):
                        if pattern in line:
                            print(f"{file_path} (line {i}): {line.strip()}")
            except Exception:
                pass

    print("\nSearch finished.")