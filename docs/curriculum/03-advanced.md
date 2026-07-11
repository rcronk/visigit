[Curriculum index](README.md) | [<- Intermediate](02-intermediate.md) | [Internals ->](04-internals.md)

---

## Tier 3 — Advanced: Power User Git

---

### EP 22 — Advanced — Rewrite History: Interactive Rebase, Squash, and Fixup

**visigit mode:** normal
**Target length:** 13–15 min
**Commands covered:** git rebase -i HEAD~N, squash, fixup, reword, drop, reorder

#### Why This Matters

Every commit you've made in this series has been permanent the moment you made it — until now. Interactive rebase is git handing you an editable transcript of recent history: reorder lines, merge lines, delete lines, and git replays the result as if you'd committed it that way from the start. The one rule that makes this safe is the one this episode hammers on: only rewrite history nobody else has built on yet.

#### YouTube Title
> git rebase -i: Squash, Reorder, and Rewrite Commits

#### YouTube Description
> Interactive rebase lets you rewrite your local commit history before sharing it: squash five "WIP" commits into one, fix a typo in a commit message, drop a commit entirely, or reorder them. This video walks through each operation in visigit so you can see exactly which commit nodes change SHA, which disappear, and which survive untouched.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Why clean history matters before a PR |
| 1:00 | Build a messy branch: five commits including WIP, typos, and one accidental commit |
| 2:00 | `git rebase -i HEAD~5` — walk through the editor |
| 3:30 | `squash`: merge commit N into N-1 — two nodes become one, new SHA |
| 5:00 | `fixup`: same as squash but discard the squashed commit's message |
| 6:00 | `reword`: change a commit message — same content, new SHA because message is in the object |
| 7:00 | `drop`: remove a commit from the branch — it stays visible via ORIG_HEAD (the pre-rebase tip) until git gc |
| 8:00 | Reorder: swap two commit lines — graph order changes, SHAs change |
| 9:00 | After rebase: graph shows clean, linear history with new SHAs for every modified commit |
| 10:00 | Why ALL downstream SHAs change when you modify one commit in a chain |
| 11:30 | The golden rule: never rebase commits already pushed to a shared branch |
| 13:00 | `git push --force-with-lease` if you must — covered more in EP28 |

#### Key Visual Moments
- Before: messy chain of 5 commit nodes
- During: new-SHA nodes appearing as operations apply; the original commits staying visible via ORIG_HEAD (the pre-rebase tip)
- After squash/fixup: fewer nodes, different SHAs
- Every commit after the rebased point has a new SHA (child SHAs change when parent SHA changes)

---

### EP 23 — Advanced — Two Kinds of Squash: merge --squash vs rebase -i squash

**visigit mode:** normal + verbose
**Target length:** 12–14 min
**Commands covered:** git merge --squash, git merge -X ours, git merge -X theirs

#### Why This Matters

"Squash" is a single English word covering two git operations with opposite mechanics: rebase -i squash rewrites commits before you ever merge, while merge --squash discards a branch's commit boundaries entirely at merge time and never even creates a merge commit. Conflating the two is an easy mistake with real consequences for what your history looks like afterward, and this episode exists specifically to make the difference impossible to un-see.

#### YouTube Title
> git merge --squash vs rebase -i squash: Not the Same Thing

#### YouTube Description
> "Squash" means two completely different things depending on which command you say it to. Interactive rebase's squash rewrites commits INSIDE your branch before you merge. git merge --squash discards your branch's commit boundaries entirely at merge time and produces a single-parent commit with no merge commit at all — this is exactly what GitHub's "Squash and merge" button does. This video shows both, side by side, plus the -X ours/-X theirs merge strategy options for auto-resolving conflicts in one direction.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "squash" means two completely different things depending on which command you say it to |
| 1:00 | Recap EP22 (interactive rebase squash): combines commits WITHIN a branch before it's shared |
| 1:45 | New scenario: feature branch has 4 messy commits, ready to land on main |
| 2:30 | `git merge --squash feature` from main — nothing is committed yet; all of feature's changes land in the index as ONE staged changeset |
| 3:30 | `git status` — "Squash commit — not updating HEAD"; verbose graph shows the Staged Changes box full, but no merge commit, no diamond |
| 4:15 | `git commit -m "Add feature"` — ONE new commit appears on main with ONE parent (main's previous tip) — feature's branch history is NOT preserved, no merge commit, no diamond at all |
| 5:15 | Side-by-side contrast: `rebase -i` squash rewrites commits INSIDE feature and still produces a normal fast-forward or diamond merge afterward; `merge --squash` discards feature's commit boundaries entirely and never creates a merge commit |
| 6:15 | When to use which: `rebase -i` squash to clean up your own branch commit-by-commit; `merge --squash` when you don't care about the branch's internal history at all — land one commit (this is what GitHub's "Squash and merge" PR button does) |
| 7:15 | `-X ours` / `-X theirs`: a real (non-squash) `git merge -X ours feature` — a normal two-parent merge commit, but conflicting hunks auto-resolve favoring main's side |
| 8:15 | Danger: `-X ours` is NOT the same as `--strategy=ours` (which discards feature's changes entirely, keeping only main's tree) — demonstrate the difference briefly |
| 9:15 | `-X theirs` — same mechanism, favoring feature's side on conflicts |
| 10:00 | Recap: rebase -i squash (rewrite, then merge normally) vs merge --squash (a merge that produces no merge commit) vs -X ours/theirs (a real merge, auto-resolving conflicts in one direction) |

#### Key Visual Moments
- `merge --squash` filling the Staged Changes box without any new commit node appearing at all
- The resulting squash commit: ONE parent edge only, despite four commits' worth of changes being folded in — no diamond, unlike EP05/EP11's --no-ff merges
- Side-by-side graphs: interactive-rebase-then-merge (diamond intact) vs `merge --squash` (single-parent commit, feature branch commits invisible in the graph)

---

### EP 24 — Advanced — Moving a Branch's Base: git rebase --onto

**visigit mode:** normal
**Target length:** 10–12 min
**Commands covered:** git rebase --onto, git log --graph --all

#### Why This Matters

A plain git rebase always means "replay everything not already on the target," which only works if you want to keep every one of your branch's commits. --onto exists for the case that comes up constantly in real projects — your branch was built on the wrong foundation — by letting you name the exact exclusion boundary yourself instead of accepting whatever rebase would replay by default.

#### YouTube Title
> git rebase --onto: Fix a Branch Built on the Wrong Base

#### YouTube Description
> Plain git rebase replays every commit not already on your target. But what if your branch was built on top of ANOTHER branch you now want to skip entirely? git rebase --onto lets you name the exact exclusion boundary yourself. This video builds a three-branch chain, then replants the tip branch directly onto main — skipping the middle branch's commits completely — and shows exactly which commits get new SHAs and which vanish from the new history.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "my branch is based on the WRONG branch — do I have to start over?" |
| 1:00 | Recap: plain `git rebase main` replays ALL commits not on main — what if you only want SOME of them? |
| 1:45 | Scenario: `topic` was branched from `feature` (not main); `feature` was branched from main; you want topic's commits directly on main, skipping feature's commits entirely |
| 3:00 | Build it: main → feature (2 commits) → topic (2 more commits) |
| 4:00 | `git log --graph --oneline --all` — the three-tier chain visible in both terminal and visigit |
| 4:45 | The goal stated visually: point at feature's tip (the commits to exclude) and topic's tip (the commits to keep) |
| 5:30 | `git rebase --onto main feature topic` — read it right-to-left: take topic, exclude everything up to feature, replant onto main |
| 6:30 | Watch: only topic's 2 commits get new SHAs and reappear directly on top of main; feature's 2 commits are completely skipped |
| 7:30 | ORIG_HEAD still points at topic's pre-rebase tip — the original commits aren't gone |
| 8:15 | Second use case: cutting one bad commit permanently out of a chain — `git rebase --onto <sha>~1 <sha> branch` removes exactly that commit |
| 9:15 | Recap: plain rebase replays "everything not on the target"; --onto lets you name the exact exclusion boundary yourself |

#### Key Visual Moments
- The three-branch chain (main → feature → topic) fully visible before the rebase
- Topic's commits reappearing with new SHAs attached directly to main's tip, with feature's commits nowhere in the new chain
- ORIG_HEAD preserving topic's original (feature-based) position even though the new topic looks completely different

---

### EP 25 — Advanced — Tags Are Just Pointers (Until They Aren't): Annotated vs Lightweight

**visigit mode:** normal
**Target length:** 10–12 min
**Commands covered:** git tag, git tag -a, git tag -l, git push --tags, git describe

#### Why This Matters

A lightweight tag is structurally identical to a branch that never moves — just a named pointer at a commit. An annotated tag adds a whole extra object in between, with its own SHA, message, and signature support. Most people reach for lightweight tags out of habit; understanding what annotated tags actually buy you is what makes "always use -a for releases" a reasoned choice instead of a rule someone told you to follow.

#### YouTube Title
> git tag vs git tag -a: Lightweight vs Annotated Tags

#### YouTube Description
> A lightweight tag is just a ref that points to a commit — exactly like a branch, except it doesn't move. An annotated tag is a full git object with its own SHA, author, and message, sitting between the tag ref and the commit. This video shows you both in visigit's graph so you can see exactly what you're creating and why annotated tags are preferred for releases.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | What tags are for: marking releases and milestones |
| 1:00 | `git tag v1.0` (lightweight) — a new tag ref appears directly pointing to the commit |
| 2:00 | One node: tag ref → commit (same as a branch, just doesn't move) |
| 3:00 | `git tag -a v2.0 -m "Release 2.0"` — two nodes: tag ref → tag object → commit |
| 4:30 | The tag object: it has its own SHA, tagger identity, timestamp, message |
| 5:30 | Why annotated tags are preferred: contain metadata, can be signed, shown by `git describe` |
| 6:30 | `git tag -l` — list all tags; cross-reference with graph |
| 7:30 | `git push --tags` — push all tags to remote |
| 8:30 | `git describe --tags` — finds nearest tag and measures distance in commits |
| 9:30 | Deleting a tag vs deleting a branch: same `git tag -d` / `git push origin :v1.0` |
| 10:30 | Signed tags: full treatment in EP38 |

#### Key Visual Moments
- Lightweight tag: single extra ref node pointing straight to commit
- Annotated tag: two nodes — tag ref node + tag object node with intermediate SHA
- Side-by-side in graph: v1.0 (lightweight) with one hop; v2.0 (annotated) with two hops

---

### EP 26 — Advanced — Binary Search Your Bug: git bisect and the Commit Graph

**visigit mode:** normal
**Target length:** 12–14 min
**Commands covered:** git bisect start, git bisect good, git bisect bad, git bisect reset, git bisect run, git bisect start --no-checkout

#### Why This Matters

A bug hiding somewhere in 500 commits sounds like a linear search problem, but git bisect turns it into a logarithmic one — roughly 9 tests instead of 500. The mechanism is nothing more exotic than checking out the midpoint commit and asking a yes/no question, repeated; seeing HEAD jump to that midpoint in the graph is what makes the halving concrete instead of theoretical.

#### YouTube Title
> git bisect: Binary Search Your History to Find a Bug

#### YouTube Description
> A bug exists now that didn't exist six months ago. git bisect performs a binary search through your commit history, halving the search space at each step. This video shows the process in visigit: watch HEAD move through the graph as bisect narrows in on the exact commit that introduced the bug — often in just 7-10 steps through hundreds of commits. We also cover the --no-checkout variant, which is the only mode where git actually writes a BISECT_HEAD ref instead of just moving HEAD.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The problem: something broke, you don't know when |
| 1:00 | Build a history with 16 commits; introduce a bug at commit 10 |
| 2:00 | `git bisect start` |
| 2:30 | `git bisect bad` — mark current HEAD as bad |
| 3:00 | `git bisect good <old-sha>` — mark a known good commit |
| 3:30 | HEAD moves to the midpoint — watch visigit show HEAD directly at the middle commit (default bisect detaches HEAD; no BISECT_HEAD ref appears here) |
| 4:30 | Test, mark good or bad; HEAD moves again — bisect halves the range |
| 6:00 | After log2(16) = 4 steps: bisect identifies the exact commit |
| 7:00 | `git bisect log` — see the search path |
| 8:00 | `git bisect reset` — HEAD returns to original position |
| 9:00 | `git bisect run <test-script>` — fully automated bisect |
| 10:00 | Bonus: `git bisect start --no-checkout` — this time the working tree never moves; instead a BISECT_HEAD ref appears in the graph pointing at the candidate commit (callback to EP19) |
| 11:30 | Why `--no-checkout` exists: useful when checking out every candidate is expensive (huge working trees, build steps) |
| 12:30 | Real-world tip: use `--max-commit-depth N` in visigit to limit graph depth during bisect |

#### Key Visual Moments
- Default bisect: HEAD node jumping to the midpoint commit after `git bisect start` + good/bad — no BISECT_HEAD, because the working tree is being checked out directly
- Each test step: HEAD moves to a new midpoint in the graph
- `--no-checkout` bisect: a distinct BISECT_HEAD ref node appears pointing at the candidate commit while HEAD itself stays put
- `git bisect reset` moving HEAD back to its original position

---

### EP 27 — Advanced — Two Branches, One Checkout: git worktree Explained

**visigit mode:** branch
**Target length:** 10–12 min
**Commands covered:** git worktree add, git worktree list, git worktree remove, git worktree prune

#### Why This Matters

git's working tree and its object store are conceptually separate, and worktree is the feature that makes that separation visible: multiple working trees, each with their own checked-out branch, all sharing the exact same underlying object database. Once you've seen two directories on disk both reading from one .git, "I need to stash to switch branches" stops being a fact of life and becomes an avoidable workaround.

#### YouTube Title
> git worktree: Check Out Two Branches Without Stashing

#### YouTube Description
> Normally you can only have one branch checked out at a time. git worktree lets you check out additional branches into separate directories on disk — each with its own working tree. You can run a server on main while developing on a feature branch, without stashing or switching. This video uses visigit's branch mode to show all active worktrees alongside the branch topology.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The problem: you're mid-feature and need to test something on main |
| 1:00 | The old way: stash, switch, work, switch back, pop |
| 2:00 | `git worktree add ../hotfix-work hotfix/critical` — new directory, new checkout |
| 3:30 | Branch mode: both main and hotfix/critical shown; each has its own path label |
| 4:30 | Work in each directory independently — no stashing needed |
| 5:30 | `git worktree list` — all active worktrees with their paths |
| 6:30 | Branch mode updates as you commit in each worktree |
| 7:30 | `git worktree remove ../hotfix-work` — path disappears |
| 8:30 | `git worktree prune` — clean up stale entries |
| 9:30 | Constraint: same branch can't be checked out in two worktrees simultaneously |
| 10:30 | When worktrees shine: long-running builds, parallel reviews, CI environments |

#### Key Visual Moments
- Branch mode showing multiple branch nodes with their checked-out paths
- Topology updating as commits land in separate worktrees
- Worktree removal: branch node remains, path annotation gone

---

### EP 28 — Advanced — Force Push Is Destroying Someone's History: Here's the Proof

**visigit mode:** normal
**Target length:** 11–13 min
**Commands covered:** git push --force, git push --force-with-lease, git reflog (on remote)

#### Why This Matters

A normal push is git refusing to lose information — it rejects any update that isn't a fast-forward. --force is you explicitly telling git that's fine, replace whatever's there. The danger isn't the command itself, it's that "whatever's there" might be a teammate's work you never fetched, which is exactly what this episode makes visible before it becomes a real incident.

#### YouTube Title
> git push --force: How It Destroys Your Team's History

#### YouTube Description
> Force push rewrites the remote ref to point at your local commit chain, discarding everything the remote had that you don't. If a teammate pushed after you last pulled, their commits are simply gone from the remote. This video makes the danger concrete by showing you exactly what the graph looks like before and after a force push — and why --force-with-lease is a safer alternative.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | How force push looks safe from your local graph — and why it isn't |
| 1:00 | Build the scenario: you and a teammate both push to main |
| 2:00 | Teammate's commit: origin/main has advanced past your last fetch |
| 3:00 | `git push` fails: non-fast-forward rejection |
| 3:30 | The temptation: `git push --force` |
| 4:00 | Show what force push does: origin/main jumps to your commit; the teammate's commit is now unreachable from origin/main, though visigit still shows it via FETCH_HEAD (last fetched) |
| 5:00 | The teammate's commits are gone from the remote ref — locally still shown via FETCH_HEAD until your next fetch, and recoverable from their reflog |
| 6:00 | Safer alternative: `git push --force-with-lease` |
| 7:00 | force-with-lease: push fails if origin/main has moved since your last fetch |
| 8:00 | Legitimate uses of force push: rebased personal feature branches before PR merge |
| 9:00 | The rule: force push only to branches no one else has checked out |
| 10:00 | `--force-with-lease=refs/heads/main:<known-sha>`: the most surgical form |
| 11:30 | Recap: force push changes where a ref points; it does not delete objects (yet) |

#### Key Visual Moments
- Before force push: origin/main points to teammate's commit; your commit is behind
- After force push: origin/main jumps to your commit; the teammate's commit is orphaned from origin/main (still visible via FETCH_HEAD until the next fetch)
- force-with-lease rejection: no graph change because the push was blocked

---

[Curriculum index](README.md) | [<- Intermediate](02-intermediate.md) | [Internals ->](04-internals.md)
