# Visible Git — YouTube Series Curriculum

**Series tagline:** *Stop memorizing commands. Start seeing what they do.*

Almost every episode runs `visigit --monitor` in one terminal while git commands run in another.
The diagram updates live. Viewers watch the DAG change rather than guessing what happened.
(The one exception is EP35, a terminal-only reference episode on `git config` — there's no
graph to watch because config doesn't touch the object store or refs.)

The full curriculum is split by tier to keep each file a manageable size:

- [00-setup.md](00-setup.md) — Tier 0: Setup (EP01)
- [01-beginner.md](01-beginner.md) — Tier 1: Beginner (EP02–EP10)
- [02-intermediate.md](02-intermediate.md) — Tier 2: Intermediate (EP11–EP21)
- [03-advanced.md](03-advanced.md) — Tier 3: Advanced (EP22–EP28)
- [04-internals.md](04-internals.md) — Tier 4: Internals (EP29–EP34)
- [05-reference.md](05-reference.md) — Tier 5: Reference (EP35–EP39)

---

## Series Overview

| # | Tier | Title | Mode | Commands |
|---|------|-------|------|----------|
| 01 | Setup | [See Your Git: Setting Up a Live Repository Visualizer](00-setup.md) | all | install |
| 02 | Beginner | [Your First Repository: Watching the Graph Appear](01-beginner.md) | normal | init, add, commit |
| 03 | Beginner | [Ignoring and Cleaning: What .gitignore and git clean Actually Touch](01-beginner.md) | verbose | gitignore, check-ignore, rm --cached, clean |
| 04 | Beginner | [Branches Aren't Copies: What Branching Really Does](01-beginner.md) | normal | branch, checkout -b, switch |
| 05 | Beginner | [The Merge Diamond: Fast-Forward vs No-Fast-Forward](01-beginner.md) | normal + branch | merge, merge --no-ff |
| 06 | Beginner | [Resolving Merge Conflicts: What MERGE_HEAD Shows You](01-beginner.md) | normal | merge (conflict), add, commit, merge --abort |
| 07 | Beginner | [Reset Demystified: Three Pointer Moves, Not Three Commands](01-beginner.md) | normal | reset --soft/--mixed/--hard |
| 08 | Beginner | [Undo Without Fear: revert vs amend (vs reset)](01-beginner.md) | normal | revert, commit --amend |
| 09 | Beginner | [Don't Panic: Detached HEAD Explained and Escaped](01-beginner.md) | normal | checkout SHA, checkout -b |
| 10 | Beginner | [Orphan Branches: Commits With No Parents, On Purpose](01-beginner.md) | normal + branch | checkout --orphan |
| 11 | Intermediate | [Merge vs Rebase: Same Code, Completely Different History](02-intermediate.md) | normal | merge, rebase |
| 12 | Intermediate | [Rebase Conflicts: --continue, --skip, --abort](02-intermediate.md) | normal | rebase (conflict), rebase --continue/--skip/--abort |
| 13 | Intermediate | [origin/main Is Not main: Remote Tracking Branches](02-intermediate.md) | normal | remote, fetch, pull, push |
| 14 | Intermediate | [Two Repos, One Screen: Watching local and origin Together](02-intermediate.md) | all | clone, push, fetch, pull (bare origin) |
| 15 | Intermediate | [One Remote Isn't Enough: origin, upstream, and the Fork Workflow](02-intermediate.md) | normal | remote add upstream, fetch upstream, merge/rebase |
| 16 | Intermediate | [Stash Is a Secret Commit: What git stash Actually Creates](02-intermediate.md) | verbose | stash, stash pop, stash list |
| 17 | Intermediate | [Cherry-Pick: Copying a Commit (and Why the SHA Changes)](02-intermediate.md) | normal | cherry-pick |
| 18 | Intermediate | [You Didn't Lose It: Finding Commits with git reflog](02-intermediate.md) | normal | reflog, reset --hard, checkout SHA |
| 19 | Intermediate | [Git's Safety Nets: ORIG_HEAD, FETCH_HEAD, and Friends](02-intermediate.md) | normal | (observe pseudo-refs) |
| 20 | Intermediate | [Finding the Needle: git blame, log -S, and log --grep](02-intermediate.md) | normal | log --grep/-S/-G, blame |
| 21 | Intermediate | [Partial Commits: What git add -p Actually Stages](02-intermediate.md) | verbose | add -p, restore -p |
| 22 | Advanced | [Rewrite History: Interactive Rebase, Squash, and Fixup](03-advanced.md) | normal | rebase -i |
| 23 | Advanced | [Two Kinds of Squash: merge --squash vs rebase -i squash](03-advanced.md) | normal + verbose | merge --squash, merge -X ours/theirs |
| 24 | Advanced | [Moving a Branch's Base: git rebase --onto](03-advanced.md) | normal | rebase --onto |
| 25 | Advanced | [Tags Are Just Pointers (Until They Aren't): Annotated vs Lightweight](03-advanced.md) | normal | tag, tag -a |
| 26 | Advanced | [Binary Search Your Bug: git bisect and the Commit Graph](03-advanced.md) | normal | bisect start/good/bad/reset, --no-checkout |
| 27 | Advanced | [Two Branches, One Checkout: git worktree Explained](03-advanced.md) | branch | worktree add/list/remove |
| 28 | Advanced | [Force Push Is Destroying Someone's History: Here's the Proof](03-advanced.md) | normal | push --force, push --force-with-lease |
| 29 | Internals | [Inside a Commit: blob, tree, commit — Git's Four Object Types](04-internals.md) | verbose | commit (step through) |
| 30 | Internals | [Submodules vs Subtrees: Pointer or Merged Files?](04-internals.md) | verbose | submodule add, subtree add |
| 31 | Internals | [Same File, Same SHA: How Git Never Stores the Same Content Twice](04-internals.md) | verbose | add, commit (cross-commit reuse) |
| 32 | Internals | [The Staging Area Exposed: What git add Actually Does to the Object Store](04-internals.md) | verbose | add, restore --staged, rm --cached |
| 33 | Internals | [All the Way Down: git cat-file, .git/objects, and Pack Files](04-internals.md) | verbose + terminal | cat-file -p/-t, ls .git/objects/ |
| 34 | Internals | [Thin Slices: Shallow Clones and Grafted History](04-internals.md) | normal | clone --depth, fetch --unshallow |
| 35 | Reference | [Making Git Yours: git config, Aliases, and .gitconfig](05-reference.md) | terminal | config --global, alias |
| 36 | Reference | [Line Endings and .gitattributes: Taming Cross-Platform Diffs](05-reference.md) | verbose | gitattributes, autocrlf, add --renormalize |
| 37 | Reference | [Never Resolve the Same Conflict Twice: git rerere](05-reference.md) | normal | rerere.enabled, rerere diff/status |
| 38 | Reference | [Proving It Was You: Signing Commits and Tags](05-reference.md) | verbose | commit -S, tag -s, verify-commit |
| 39 | Reference | [Big Repos, Small Checkouts: Sparse Checkout and Partial Clone](05-reference.md) | verbose | clone --filter, sparse-checkout |

---

## Integration Test Notes

Three companion test layers keep every lesson diagram accurate:

- [tests/test_lessons.py](../../tests/test_lessons.py) — **key** node/edge presence per episode
  (survives cosmetic layout changes).
- [tests/test_lessons_full.py](../../tests/test_lessons_full.py) — **exhaustive** per-step checks:
  the exact, complete node + edge + label set for each lesson state, hand-derived from git
  semantics. An autouse fixture also cross-checks every step against the independent oracle.
- [tests/git_oracle.py](../../tests/git_oracle.py) + [tests/test_oracle_differential.py](../../tests/test_oracle_differential.py)
  — an **independent** oracle that re-derives the expected graph straight from `git` plumbing
  (a different algorithm) and is compared against visigit over fixed scenarios and randomly
  generated repos, in normal / verbose / branch modes (including bare "origin" repos).

Running them:
```bash
pytest tests/test_lessons.py tests/test_lessons_full.py tests/test_oracle_differential.py -v
```

When a test fails it almost always means a visigit bug would make the diagram in that lesson
wrong. Git behaviour varies across versions (e.g. auto-creating `refs/remotes/origin/HEAD`),
so the CI matrix runs the suite on multiple OS and Python versions; record lessons on a recent
stable git and state the version on-screen.

**Coverage status for the 15 new episodes added in this pass (EP03, EP10, EP12, EP15, EP20,
EP21, EP23, EP24, EP26 bonus segment, EP34, EP35–EP39):** episodes whose key visual moment is a
concrete, deterministic change to the rendered graph (EP03, EP10, EP12, EP15, EP21, EP23, EP24,
EP34, and EP26's `--no-checkout` bonus segment) have `test_lessons.py` coverage — see the
`TestLesson03...` through `TestLesson34...` classes added alongside this curriculum update.
Episodes that are query-only or config-only and never change the DOT output at all (EP20 blame/
pickaxe, EP35 config/aliases, EP36 gitattributes-as-workflow, EP37 rerere, EP38 signing) do not
get dedicated lesson tests, for the same reason EP01 (setup) doesn't: there's no graph-shape
claim to regression-test. EP39 (sparse checkout / partial clone) is exercised indirectly by the
existing shallow/partial-object handling in `repo.py` but doesn't yet have a dedicated lesson
test — local `--filter=blob:none` support varies by git version, so add one deliberately with a
version guard before filming rather than as a blanket addition here.

None of the 15 new episodes yet have `test_lessons_full.py` (exact node/edge set) or
`git_oracle.py` differential coverage. That tier hand-derives the *complete* expected output and
cross-checks it against an independent plumbing-based oracle — a substantially larger effort per
episode than the presence checks above. Recommend adding it episode-by-episode as each one is
actually scripted for filming, the same way the existing 25 episodes accumulated that coverage
over time (see PR #56).
