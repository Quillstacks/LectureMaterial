#!/usr/bin/env bash
# Diffs & Merge Conflicts — hands-on sandbox.
#
# Builds a throwaway git repo at /tmp/vibe-merge-demo with a deliberately
# engineered three-way merge conflict, then walks you through resolving it.
# Safe to delete the directory afterwards.

set -euo pipefail

DEMO="${DEMO:-/tmp/vibe-merge-demo}"

echo "[demo] Building sandbox at $DEMO"
rm -rf "$DEMO"
mkdir -p "$DEMO"
cd "$DEMO"

git init -q -b main
git config user.email "student@example.com"
git config user.name  "Student"

# --- baseline ---------------------------------------------------------------
cat >greet.py <<'EOF'
def greet(name):
    return "Hello, " + name + "!"

if __name__ == "__main__":
    print(greet("world"))
EOF
git add greet.py
git commit -qm "baseline greeter"

# --- branch A: f-strings ----------------------------------------------------
git checkout -q -b feature/fstring
cat >greet.py <<'EOF'
def greet(name):
    return f"Hello, {name}!"

if __name__ == "__main__":
    print(greet("world"))
EOF
git commit -qam "use f-string"

# --- branch B: i18n on the same line ---------------------------------------
git checkout -q main
git checkout -q -b feature/i18n
cat >greet.py <<'EOF'
def greet(name, lang="en"):
    greeting = {"en": "Hello", "de": "Hallo"}[lang]
    return greeting + ", " + name + "!"

if __name__ == "__main__":
    print(greet("world"))
EOF
git commit -qam "add language parameter"

# --- engineer the conflict --------------------------------------------------
git checkout -q main
git merge -q --no-edit feature/fstring
echo
echo "[demo] About to merge feature/i18n into main — this will conflict."
echo "[demo] Press Enter to trigger the conflict ..."
read -r _

set +e
git merge --no-edit feature/i18n
set -e

echo
echo "[demo] Conflict produced. greet.py now contains conflict markers:"
echo "----------------------------------------------------------------"
cat greet.py
echo "----------------------------------------------------------------"
cat <<'EOF'

How to read the markers:

  <<<<<<< HEAD               <- "ours"   (what is on the branch you are on)
  ...your version...
  =======                    <- the divider
  ...their version...
  >>>>>>> feature/i18n       <- "theirs" (what you are merging in)

Three resolution strategies, in increasing order of brain required:

  1. Take ours:    git checkout --ours   greet.py
  2. Take theirs:  git checkout --theirs greet.py
  3. Hand-merge:   open the file, delete the markers, write the union.

For this demo the *correct* answer is the hand-merge — both changes (f-string
AND the lang parameter) need to coexist. Open the file and combine them:

    micro greet.py        # or: zed . / code .

Target body for greet():

    def greet(name, lang="en"):
        greeting = {"en": "Hello", "de": "Hallo"}[lang]
        return f"{greeting}, {name}!"

After editing, finish the merge:

    git add greet.py
    git commit              # default merge message is fine
    python3 greet.py        # should print: Hello, world!

Useful diff commands during a conflict:

    git diff                       # unified diff of unstaged changes
    git diff --ours   greet.py     # what you had before the merge
    git diff --theirs greet.py     # what is being merged in
    git diff --base   greet.py     # against the common ancestor
    git mergetool                  # launches a 3-way GUI if configured

Bail out without resolving:

    git merge --abort

EOF
