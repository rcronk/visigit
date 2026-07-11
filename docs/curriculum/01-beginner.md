[Curriculum index](README.md) | [<- Setup](00-setup.md) | [Intermediate ->](02-intermediate.md)

---

## Tier 1 — Beginner: Git Fundamentals

---

### EP 02 — Beginner — Your First Repository: Watching the Graph Appear

**visigit mode:** normal
**Target length:** 10–12 min
**Commands covered:** git init, git status, git add, git commit, git log

#### Why This Matters

git's data model is deceptively simple: a commit is a snapshot with a pointer to its parent, a branch is a movable label pointing at a commit, and HEAD is a label pointing at whichever branch (or commit) you're standing on. Every other git command in this series is just a variation on moving or creating these three kinds of pointers. Understanding this three-tier structure from the very first commit is what makes reset, rebase, and detached HEAD make sense later instead of feeling like separate tricks to memorize.

#### YouTube Title
> git init, add, commit — Watch the Commit Graph Build Itself in Real Time

#### YouTube Description
> You've run git init and git commit a hundred times. But do you know what they actually create? This video uses visigit to show you the moment HEAD, a branch ref, and your first commit node appear in the graph — and how the chain grows with every new commit. By the end you'll understand exactly what git status and git log are reporting.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Start the monitor: `visigit --monitor --viewer html` in Terminal A |
| 0:45 | `git init -b main` — graph is empty, why? |
| 1:30 | Create a file, `git status` — untracked, nothing in graph yet |
| 2:15 | `git add README.md` — still nothing? (staging doesn't create a commit) |
| 3:00 | `git commit -m "initial"` — HEAD, main, and the first commit node appear at once |
| 4:30 | Explain the three nodes: HEAD ref → branch ref → commit node |
| 5:30 | Second commit: `echo "hello" > app.py && git add -A && git commit -m "add app"` |
| 6:30 | Parent edge appears: newer commit → older commit |
| 7:30 | Third commit: the chain grows — `git log` matches exactly what's in the graph |
| 8:30 | Boring chain collapse: add 5 quick commits and watch them become one summary node |
| 10:00 | `--commit-details` flag: author, message, date appear on each node |
| 11:00 | Recap: what the three-tier HEAD → branch → commit structure means |

#### Key Visual Moments
- Empty graph before first commit
- Simultaneous appearance of HEAD, branch ref, and commit node on first `git commit`
- Parent edge direction (newest commit on the right with default RL layout)
- Boring chain collapsing into `a1b2c3 (N) f4e5d6` summary node

---

### EP 03 — Beginner — Ignoring and Cleaning: What .gitignore and git clean Actually Touch

**visigit mode:** verbose
**Target length:** 9–11 min
**Commands covered:** git status, .gitignore, git check-ignore, git rm --cached, git clean -n/-fd, git status --ignored

#### Why This Matters

Git tracks files it already knows about and reports everything else as untracked — .gitignore only controls which NEW files get offered up for tracking; it has no opinion about files git has already committed. This is the single most common .gitignore misunderstanding, and it matters because people routinely assume adding a file to .gitignore will make a secret or a build artifact "go away," when it actually does nothing until you explicitly untrack it with git rm --cached.

#### YouTube Title
> .gitignore Doesn't Untrack Files — Here's What It Actually Does (and What git clean Does Instead)

#### YouTube Description
> Everyone's first .gitignore mistake is the same: adding a file to it and expecting git to stop tracking it. .gitignore only stops NEW files from being tracked — it has zero effect on files git already knows about. This video uses visigit's verbose-mode Untracked box to show exactly what .gitignore prevents, what git rm --cached does to actually untrack a file, and what git clean deletes that .gitignore doesn't.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "why is this file still following me around?" |
| 1:00 | Start `visigit --mode verbose --monitor` |
| 1:30 | Create build noise: `app.log`, `__pycache__/cache.pyc`, `secrets.env` |
| 2:15 | `git status` — a wall of untracked files; the Untracked box mirrors every one of them |
| 3:00 | `echo -e "*.log\n__pycache__/" > .gitignore` |
| 3:45 | `git status` again — the ignored files vanish from the untracked list; the Untracked box shrinks to just `secrets.env` and `.gitignore` |
| 4:30 | `git check-ignore -v build/app.log` — shows exactly which .gitignore line matched, and from which file |
| 5:15 | The trap: `secrets.env` was committed BEFORE it was added to .gitignore — adding it now does nothing, it's still tracked |
| 6:00 | `git rm --cached secrets.env` — removes it from the index only; the file stays on disk and reappears in the Untracked box |
| 6:45 | Add `secrets.env` to `.gitignore` now that it's untracked — this time it actually sticks |
| 7:30 | `git clean -n` — dry run, lists exactly what would be deleted (ignored files are NOT included by default) |
| 8:15 | `git clean -fd` — deletes every untracked file and directory; the Untracked box empties completely |
| 9:00 | `git status --ignored` — see ignored files explicitly, since normal `git status` hides them |
| 9:45 | Recap: .gitignore prevents future tracking, `rm --cached` stops tracking a file that's already tracked, `clean` deletes untracked files from disk — three separate jobs |

#### Key Visual Moments
- The Untracked box (verbose mode) shrinking the instant `.gitignore` takes effect
- A previously-tracked file staying fully tracked — still reachable through the committed tree — even after being listed in `.gitignore`, until `git rm --cached` runs
- `git rm --cached` moving a file's node out of the tracked-tree path and into the Untracked box without touching the working copy on disk
- `git clean -fd` wiping the entire Untracked box in one shot

---

### EP 04 — Beginner — Branches Aren't Copies: What Branching Really Does

**visigit mode:** normal
**Target length:** 10–13 min
**Commands covered:** git branch, git checkout -b, git switch -c, git switch, git checkout

#### Why This Matters

A branch is not a copy of your code — it's a pointer to a single commit, which is why creating one is instant regardless of repository size. The entire concept of "lightweight branching" that makes git workflows fast and cheap depends on this fact, and once you've seen a branch created as nothing but a new label on an existing commit, phrases like "check out a branch" stop sounding like file operations and start sounding like what they are: pointer moves.

#### YouTube Title
> git branch Doesn't Copy Anything — Here's What It Actually Does to Your Repository

#### YouTube Description
> Most people think creating a branch copies their code. It doesn't — it creates a single pointer to an existing commit. Watch visigit show you the exact moment a branch label appears in the graph and how it splits from its sibling when you make your first commit. This one diagram will change how you think about branches forever.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Misconception: "branching makes a copy" — let's disprove it visually |
| 1:00 | Make two commits on main, watch the chain form |
| 2:00 | `git checkout -b feature` — only a new label appears on the same commit |
| 3:00 | HEAD moves to feature; main stays exactly where it was |
| 4:00 | `git switch` / `git checkout` — HEAD label moves between branch refs |
| 5:00 | First commit on feature: NOW the branches diverge — main left behind |
| 6:30 | Switch back to main — HEAD moves; feature tip stays |
| 7:30 | First commit on main: two branches pointing to different commits from the same parent |
| 8:30 | `git branch -v` output compared to what the graph shows |
| 9:30 | Deleting a branch: `git branch -d feature` — label disappears, commit still exists |
| 11:00 | Orphaned commits: when is it safe to delete? |

#### Key Visual Moments
- New branch label appearing on the same commit node as main
- HEAD arrow moving when you switch branches
- The moment of divergence: each branch gets its own commit
- Branch deletion removing the label but leaving the commit node until GC

---

### EP 05 — Beginner — The Merge Diamond: Fast-Forward vs No-Fast-Forward

**visigit mode:** normal (commit chain) + branch (topology)
**Target length:** 12–15 min
**Commands covered:** git merge, git merge --no-ff

#### Why This Matters

"Merge" is really two different operations wearing one name: a fast-forward, which just slides a pointer forward with no new commit, and a true merge, which creates a new commit with two parents. Knowing which one you're about to get — and that --no-ff can force the second even when the first would work — is the difference between a history that shows exactly when features were integrated and one that quietly erases that information.

#### YouTube Title
> git merge --no-ff Creates a Diamond — Here's What That Means and Why It Matters

#### YouTube Description
> There are two completely different graph shapes that can result from a merge: a straight line (fast-forward) or a diamond (no-fast-forward). This video shows both side by side in visigit so you can see exactly when git moves a pointer vs when it creates a real merge commit — and why that choice affects your project history permanently.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Two types of merge: set the stage |
| 1:00 | Build a diverged repo: main + feature both ahead of a common base |
| 2:30 | Fast-forward scenario: feature is strictly ahead of main |
| 3:30 | `git merge feature` — main label jumps to feature tip; no new commit node |
| 4:30 | Why it's called "fast-forward": the pointer simply advances |
| 5:30 | Reset and rebuild: diverged scenario where both branches have unique commits |
| 6:30 | `git merge feature --no-ff` — a merge commit appears with TWO parent edges |
| 7:30 | The diamond: base → left path → merge commit ← right path ← base |
| 8:30 | Switch to `--mode branch`: see the topology in branch view |
| 9:30 | When to use each: open-source vs team workflows |
| 11:00 | Merge conflicts: what they look like (brief; deep dive in EP06) |
| 12:30 | Merge commit has two parents — show the edges in the graph |

#### Key Visual Moments
- Fast-forward: branch label teleports, no new commit node
- No-FF: merge commit node with two inbound parent edges
- Branch mode: diamond becomes a fork-point node connecting two branch labels
- `--commit-details` showing "Merge branch 'feature' into main" message on the merge commit

---

### EP 06 — Beginner — Resolving Merge Conflicts: What MERGE_HEAD Shows You

**visigit mode:** normal
**Target length:** 10–12 min
**Commands covered:** git merge (conflict), git status, git add, git commit, git merge --abort

#### Why This Matters

A merge conflict isn't git being broken, it's git being honest that it can't guess which change you want — and it pauses by writing MERGE_HEAD, a real ref pointing at the commit you're merging in, so both you and git can keep track of what's being combined. Understanding that MERGE_HEAD is just an ordinary pointer, not a special error state, is what turns "I'm scared of conflicts" into "I know exactly what git is waiting on me to do."

#### YouTube Title
> Merge Conflicts Aren't Scary: git Writes MERGE_HEAD and visigit Shows You Exactly Where You Are

#### YouTube Description
> A merge conflict stops git mid-merge and leaves you in a state most people find terrifying. It shouldn't be. When a merge conflicts, git writes a ref called MERGE_HEAD pointing at the commit you're merging in — and visigit shows it right in the graph, so you can always see both sides of the merge and exactly what you're resolving. This video walks a conflict from start to finish: what MERGE_HEAD is, how to resolve it, and how to bail out with --abort.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The fear: "CONFLICT (content): Merge conflict in ..." |
| 1:00 | Set up two branches that edit the same line |
| 2:00 | `git merge feature` — it stops; the working tree is now mid-merge |
| 2:45 | visigit shows MERGE_HEAD pointing at the feature commit — both sides visible |
| 3:45 | `git status` — "Unmerged paths"; what the index looks like during a conflict |
| 4:45 | Open the file: the `<<<<<<<`, `=======`, `>>>>>>>` markers explained |
| 5:45 | Resolve, then `git add` the file — the conflict is staged |
| 6:45 | `git commit` — the merge commit appears with TWO parents; MERGE_HEAD disappears |
| 7:45 | The escape hatch: `git merge --abort` — back to before the merge, MERGE_HEAD gone |
| 8:45 | Why MERGE_HEAD matters: it's how git (and you) remember what's being merged |
| 10:00 | Recap: a conflict is just a paused merge; MERGE_HEAD marks the other side |

#### Key Visual Moments
- MERGE_HEAD node appearing the moment a merge conflicts, pointing at the merged commit
- Both merge parents visible simultaneously while the conflict is unresolved
- The merge commit forming (two parent edges) and MERGE_HEAD vanishing on `git commit`
- `git merge --abort` removing MERGE_HEAD and returning HEAD to the pre-merge tip

---

### EP 07 — Beginner — Reset Demystified: Three Pointer Moves, Not Three Commands

**visigit mode:** normal
**Target length:** 12–14 min
**Commands covered:** git reset --soft, git reset --mixed, git reset --hard

#### Why This Matters

All three flavors of git reset do the exact same first step — move the current branch's pointer to a different commit — and only differ in how much of the index and working tree they drag along with it. Once you see that --soft, --mixed, and --hard are one operation with three levels of "and also," reset stops being three commands to memorize and becomes one mental model with a dial on it.

#### YouTube Title
> git reset --soft vs --mixed vs --hard: Watch the Branch Pointer Move Three Different Ways

#### YouTube Description
> git reset is one of the most feared commands in git — and the most misunderstood. All three modes do the same thing to the branch pointer (move it back), so in normal mode they produce an identical graph; what they differ on is how much of your work they preserve, which you see in verbose mode. And the commit you reset past does not vanish — ORIG_HEAD still points to it. Watch visigit show you all of this, and you'll never confuse the three modes again.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The fear: "I ran git reset and lost my work" |
| 1:00 | Build up a chain: three commits, HEAD → main → C3 → C2 → C1 |
| 2:00 | What all three modes share: the branch pointer moves back |
| 3:00 | `git reset --soft HEAD~1` — main moves back to C2; C3 stays visible via the ORIG_HEAD ref (git's safety net); files are staged |
| 4:30 | Verify: `git status` shows staged changes; working tree unchanged |
| 5:30 | `git reset --mixed HEAD~1` — pointer moves again; staged changes cleared |
| 6:30 | Verify: `git status` shows unstaged changes; working tree still unchanged |
| 7:30 | `git reset --hard HEAD~1` — pointer moves; index AND working tree wiped |
| 8:30 | Verify: `git status` is clean; the files are gone |
| 9:30 | The unreachable commit: it still exists in `.git/objects` — show in verbose mode |
| 10:30 | When to use each: fixing the last commit vs recovering from disaster |
| 12:00 | Teaser: Episode 18 shows you how to recover from --hard with reflog |

#### Key Visual Moments
- Branch pointer moving back one commit with each reset
- The reset commit staying visible via the ORIG_HEAD ref (git keeps it — it is not lost), even though main no longer points to it
- The working tree / staging area state NOT visible in normal mode (point to verbose for that)
- Commit node that's "gone" from graph but visible again when you detach HEAD at its SHA

---

### EP 08 — Beginner — Undo Without Fear: revert vs amend (vs reset)

**visigit mode:** normal
**Target length:** 11–13 min
**Commands covered:** git revert, git commit --amend, (contrast with git reset)

#### Why This Matters

git doesn't have one "undo," it has three, and they do fundamentally different things to history: revert adds a new commit, amend replaces the last commit with a new one, and reset moves the pointer without changing any commit's content. Picking the wrong one is exactly how people rewrite history they've already shared with a team — this episode exists so "how do I undo this" always leads to the right tool instead of a reflexive git reset --hard.

#### YouTube Title
> git revert vs git commit --amend vs git reset: Three Ways to Undo, Three Different Graphs

#### YouTube Description
> "Undo" in git isn't one thing. revert ADDS a new commit that cancels an old one (safe to share). amend REWRITES your last commit (new SHA, the old one orphaned). reset MOVES the branch pointer back. They look similar in the terminal but do completely different things to the graph — and visigit makes the difference impossible to miss. By the end you'll always pick the right one.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Three "undos" that are nothing alike |
| 1:00 | Build a small history: a couple of commits |
| 2:00 | `git revert HEAD` — a NEW commit appears on top; the chain GROWS |
| 3:00 | Why revert is safe on shared branches: it doesn't rewrite anything |
| 4:00 | Contrast: `git reset` moves the pointer back (the EP07 mechanic) |
| 5:00 | `git commit --amend` — fix the last commit's message or content |
| 5:45 | Watch: the old commit VANISHES; a new SHA replaces it |
| 6:30 | The catch: amend writes NO ORIG_HEAD — the old commit is only in the reflog |
| 7:30 | Why the SHA changes: the message and content are part of the commit object |
| 8:30 | When to use each: revert (shared), amend (last local commit), reset (move the tip) |
| 9:30 | The golden rule: never amend or reset commits you've already pushed and shared |
| 11:00 | Recap: revert ADDS, amend REPLACES, reset MOVES |

#### Key Visual Moments
- revert: a new commit node appended (graph grows by one), the original commit untouched
- amend: the old commit node disappearing and a new-SHA node taking its place
- The absence of ORIG_HEAD after amend (unlike reset/rebase) — its old commit is truly gone from the graph
- Side-by-side mental model: ADD (revert) vs REPLACE (amend) vs MOVE (reset)

---

### EP 09 — Beginner — Don't Panic: Detached HEAD Explained and Escaped

**visigit mode:** normal
**Target length:** 10–12 min
**Commands covered:** git checkout SHA, git switch --detach, git checkout -b recovery, git switch -

#### Why This Matters

HEAD is normally two hops from a commit — HEAD points at a branch, and the branch points at the commit — but git also allows HEAD to point directly at a commit, skipping the branch entirely. That's all "detached HEAD" is: a missing middle link, not a broken repository. Knowing this means the scariest sentence in git's output ("you are in 'detached HEAD' state") becomes a state you can calmly read off the graph and walk out of.

#### YouTube Title
> "You are in 'detached HEAD' state" — What It Means and How to Escape

#### YouTube Description
> "You are in 'detached HEAD' state" is one of the most alarming messages in git. But it's not dangerous — it just means HEAD is pointing directly at a commit instead of through a branch. Watch visigit show you exactly what detached HEAD looks like in the graph, what happens to commits you make in that state, and the two ways to safely get back.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The scary message — read it aloud |
| 1:00 | Normal state: HEAD → branch → commit (three-tier) |
| 2:00 | `git checkout <sha>` on an older commit — HEAD now points directly at commit |
| 3:00 | Graph: HEAD → commit (two-tier; branch ref visible but disconnected from HEAD) |
| 4:00 | What happens if you make a commit in detached HEAD: orphan commit node |
| 5:30 | `git switch -` or `git checkout main` — HEAD reattaches to branch |
| 6:30 | The orphan commit: unreachable now but still in the object store |
| 7:30 | Escape route 2: `git checkout -b recovery` from detached HEAD |
| 8:30 | Graph: recovery branch label appears; the work is preserved |
| 9:30 | Common trigger: `git checkout <tag>` — same mechanism |
| 10:30 | Recap: detached HEAD = missing branch label, not corrupted repo |

#### Key Visual Moments
- Normal: HEAD → refs/heads/main → commit (HEAD node edges to branch node)
- Detached: HEAD → commit directly (branch ref is in graph but not connected to HEAD)
- Orphan commit made in detached HEAD state — unreachable after re-attaching
- New branch node appearing when you run `git checkout -b recovery`

---

### EP 10 — Beginner — Orphan Branches: Commits With No Parents, On Purpose

**visigit mode:** normal + branch
**Target length:** 9–10 min
**Commands covered:** git checkout --orphan, git switch --orphan, git rm -rf ., git merge-base

#### Why This Matters

Every commit in this series so far has had a parent — but git doesn't require that, and --orphan is how you deliberately create another commit with zero parents inside a repo that already has history. This is exactly the mechanism behind real-world patterns like a gh-pages branch living beside your source code with no shared history at all, and seeing it happen on purpose demystifies what would otherwise look like a broken or corrupted graph.

#### YouTube Title
> git checkout --orphan: Two Branches, One Repo, Zero Shared History

#### YouTube Description
> Every commit you've made in this series so far has had a parent — except the very first. git checkout --orphan lets you deliberately create ANOTHER parentless commit, on a brand-new branch, inside a repo that already has history. That's exactly how gh-pages branches and "start clean" branches work. This video shows the disconnected commit forming live in visigit, and proves with git merge-base that it truly shares nothing with main.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: two branches, same repo, zero shared commits — how? |
| 1:00 | Recap: every commit we've made so far has had a parent, except the very first (EP02) |
| 1:45 | `git switch --orphan gh-pages` (or `git checkout --orphan gh-pages`) — HEAD moves to a brand-new, commit-less branch |
| 2:30 | Graph before the first commit: `gh-pages` label exists with NO commit underneath — an "unborn" branch, same as right after `git init` |
| 3:15 | `git rm -rf .` clears the carried-over working tree; then `echo "<html>hi</html>" > index.html && git add index.html` |
| 4:00 | `git commit -m "Initial gh-pages commit"` — a brand new commit node appears with ZERO parent edges, sitting completely apart from main's chain |
| 5:00 | `--mode branch`: two fully disconnected trees rendered in the same repo |
| 5:45 | `git log --graph --oneline --all` in the terminal — two separate histories, no shared ancestor |
| 6:30 | `git merge-base main gh-pages` — no output / error: no common ancestor exists, confirming the disconnection |
| 7:15 | Real-world uses: gh-pages docs sites, deliberately dropping sensitive history into a fresh start, vendor-reset branches |
| 8:00 | The catch: normal merges are meaningless between orphaned trees; you push/pull the branch like any other ref |
| 9:00 | Recap: `--orphan` is the third way (besides `init` and the very first commit) a parentless commit enters your repo |

#### Key Visual Moments
- A branch label with no commit node underneath it — an "unborn" branch, identical in shape to right after `git init`
- The first orphan commit appearing with zero inbound parent edges, floating separately from every other node in the graph
- Branch-mode topology showing two completely disconnected trees inside one repository

---

[Curriculum index](README.md) | [<- Setup](00-setup.md) | [Intermediate ->](02-intermediate.md)
