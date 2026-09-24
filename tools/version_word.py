#!/usr/bin/env python3
"""Map a git short hash to a deterministic <adjective fruit Tier> triple.

Usage: version_word.py <git-hash> <adjectives.txt> <fruits.txt> <tiere.txt>
Prints the triple separated by spaces, no trailing newline.
"""
import hashlib
import sys


def pick(words: list[str], hash_str: str, salt: str) -> str:
    digest = hashlib.md5((salt + hash_str).encode("utf-8")).hexdigest()
    return words[int(digest, 16) % len(words)]


def load(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def main() -> int:
    if len(sys.argv) != 5:
        print(__doc__, file=sys.stderr)
        return 2
    hash_str, adj_path, fruit_path, animal_path = sys.argv[1:]
    adjs = load(adj_path)
    fruits = load(fruit_path)
    animals = load(animal_path)
    # Write UTF-8 bytes directly. The word lists hold German names with
    # umlauts; relying on sys.stdout's text encoding emits cp1252 on Windows
    # (a lone 0xe4 for "ä"), which inputenc then rejects as invalid UTF-8.
    sys.stdout.buffer.write(
        (
            f"{pick(adjs, hash_str, 'adj')} "
            f"{pick(fruits, hash_str, 'fruit')} "
            f"{pick(animals, hash_str, 'animal')}"
        ).encode("utf-8")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
