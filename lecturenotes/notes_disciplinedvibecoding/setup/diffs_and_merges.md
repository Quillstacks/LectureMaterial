# Diffs and Merge Conflicts — A Vibe Coder's Survival Guide

The agent will write code. You decide whether to keep it. The interface
between those two acts is the **diff**. Once two streams of changes touch the
same line, you also get the **merge conflict**. Both are reading skills before
they are typing skills.

## Reading a unified diff

```diff
--- a/greet.py
+++ b/greet.py
@@ -1,2 +1,2 @@
-def greet(name):
-    return "Hello, " + name + "!"
+def greet(name, lang="en"):
+    return f"Hello, {name}!"
```

| Symbol | Meaning |
|---|---|
| `--- a/...` | the *old* file |
| `+++ b/...` | the *new* file |
| `@@ -1,2 +1,2 @@` | hunk header: old starts at line 1 (2 lines), new starts at line 1 (2 lines) |
| line starting with `-` | removed |
| line starting with `+` | added |
| line starting with ` ` (space) | unchanged context |

**Reading order matters.** Don't scan top-to-bottom looking for `+`; pair each
`-`/`+` block and ask *what was the old contract, what is the new one, and
does anything outside this hunk depend on the old one?* That last question is
the one the model cannot answer for you.

### opencode and git speak the same dialect

`opencode` shows you a unified diff before applying any change; `git diff`
shows you the same format on disk. Once you can read one, you can read the
other.

## What a conflict looks like

When two branches touch the same line, git surrenders and writes both
versions into the file with markers:

```
<<<<<<< HEAD
return f"Hello, {name}!"
=======
greeting = {"en": "Hello", "de": "Hallo"}[lang]
return greeting + ", " + name + "!"
>>>>>>> feature/i18n
```

- `<<<<<<< HEAD` — *ours*, what is on the current branch.
- `=======`      — divider.
- `>>>>>>> X`    — *theirs*, what you are merging in.

The file is now broken Python *and* broken git. Both must be fixed.

## Three resolution strategies

| Situation | Command |
|---|---|
| Their version is correct, drop yours | `git checkout --theirs FILE` |
| Your version is correct, drop theirs | `git checkout --ours   FILE` |
| Both are partly right — combine them | open the file, delete the markers, write the union by hand |

Most real conflicts need the third option. The first two are usually wrong
when applied reflexively — they discard work, which is exactly the failure
mode `git-guardrails-claude-code` is designed to prevent.

## The four diffs you can ask git for during a conflict

```bash
git diff                  # unified diff: working tree vs. index
git diff --ours   FILE    # what you had before the merge
git diff --theirs FILE    # what is being merged in
git diff --base   FILE    # vs. the common ancestor (the three-way base)
```

The **base** is the surprising one. A clean three-way merge is a function of
*ours*, *theirs*, and *base*; if you only look at *ours* vs *theirs* you are
solving the problem with one eye closed.

## Finishing the merge

```bash
git add FILE          # tells git "I have resolved this"
git commit            # default message describes the merge; fine to keep
git merge --abort     # escape hatch: throws away the in-progress merge
```

A merge commit lands only after **every** conflicted file is resolved and
added. `git status` lists the remaining ones under "Unmerged paths".

## Vibe-coding-specific failure modes

1. **Accepting a diff without reading the hunk header.** The model removed a
   function call you did not notice because it was three lines above the
   `+++` marker. Always glance at the line numbers in `@@`.
2. **Letting the agent resolve the conflict for you.** Conflicts encode
   *intent collisions* — two humans (or one human and one earlier model run)
   wanted different things on the same line. The model has no idea which
   intent should win. You do.
3. **`git checkout --theirs .` to "make it go away".** This is the merge-time
   equivalent of `rm -rf`. It silently discards an entire side of the merge.
   Run it only when you are certain.
4. **Committing with conflict markers still in the file.** Pre-commit hooks
   (see `setup-pre-commit`) catch this; without them, the markers ship.

## Practice

`bash diffs_and_merges.sh` builds a sandbox repo with an engineered conflict
between an f-string refactor and an i18n parameter addition. Both changes are
correct in isolation; only the hand-merge is correct overall. Resolve it,
verify with `python3 greet.py`, and commit.

The sandbox lives at `/tmp/vibe-merge-demo` and is safe to delete.
