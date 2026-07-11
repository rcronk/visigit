[Curriculum index](README.md) | [<- Beginner](01-beginner.md) | [Advanced ->](03-advanced.md)

---

## Tier 2 — Intermediate: Git Workflows

---

### EP 11 — Intermediate — Merge vs Rebase: Same Code, Completely Different History

**visigit mode:** normal
**Target length:** 13–15 min
**Commands covered:** git merge --no-ff, git rebase, git log --oneline --graph

#### Why This Matters

Merge and rebase solve the identical problem — integrating diverged work — with opposite philosophies: merge preserves exactly what happened (including the diamond shape), while rebase rewrites what happened into a story that never diverged in the first place. Neither is "correct"; they're a tradeoff between historical honesty and readability, and the rest of the advanced tier (interactive rebase, --onto, rerere) only makes sense once this tradeoff is clear.

#### YouTube Title
> git merge vs git rebase: Watch Two Different Graphs

#### YouTube Description
> Merge and rebase both get your changes integrated, but they leave completely different histories behind. This video runs both operations on identical repos and shows you the graphs side by side: a merge creates a diamond with a merge commit; a rebase replays your commits with new SHAs onto a straight line. By the end you'll know which to choose and why.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Same goal, different tools — why this matters |
| 1:00 | Build the diverged scenario: main has a hotfix; feature has a new commit |
| 2:30 | Path A: `git merge feature --no-ff` — diamond shape, merge commit, two parents |
| 4:00 | Pros: preserves the true history; merge commit is explicit |
| 5:00 | Cons: noisy graph in a large project; every integration adds a node |
| 6:00 | Reset to diverged state; Path B: `git rebase main` from feature branch |
| 7:30 | Watch: NEW commit nodes appear with different SHAs; the original feature commit stays visible via ORIG_HEAD (git keeps it — rebase does not delete it) |
| 8:30 | The key insight: rebase does NOT move commits — it creates new ones |
| 9:30 | Linear history: feature replay sits directly on main's tip — clean `git log` |
| 10:30 | When to use merge: shared branches, open-source PRs, preserve context |
| 11:30 | When to use rebase: local feature cleanup, keeping a team's main branch linear |
| 12:30 | The golden rule of rebase: never rebase commits already on a shared branch |

#### Key Visual Moments
- Merge: diamond with merge commit node, two parent edges
- Rebase: new SHA nodes appear; the original (pre-rebase) commit stays reachable via the ORIG_HEAD ref — git's safety net, not deleted
- Linear history after rebase: single parent chain with no diamond
- `git log --oneline --graph` terminal output matching the visigit diagram exactly

---

### EP 12 — Intermediate — Rebase Conflicts: --continue, --skip, --abort

**visigit mode:** normal
**Target length:** 12–14 min
**Commands covered:** git rebase (conflict), git status, git add, git rebase --continue, git rebase --skip, git rebase --abort

#### Why This Matters

Because rebase replays your commits one at a time instead of integrating them all at once like a merge, a single line of disputed code can produce a conflict on every commit that touches it — which is why rebase conflicts feel repetitive in a way merge conflicts don't. Understanding that each replay is its own mini-merge is what turns "why do I keep hitting the same conflict" into an expected, manageable part of the process instead of a sign something's gone wrong.

#### YouTube Title
> git rebase Conflicts: Watch Why They Keep Repeating

#### YouTube Description
> A merge conflict stops you once. A rebase conflict can stop you once PER COMMIT being replayed, because rebase applies your commits one at a time. This video walks a real two-commit rebase conflict start to finish — resolving, continuing, resolving again — and shows the three escape hatches: --continue, --skip, and --abort. You'll see exactly why the same conflict can reappear and what visigit shows you while it's happening.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "rebase conflicts feel like whack-a-mole — here's why" |
| 1:00 | Recap EP11: rebase replays commits one commit at a time, not all at once |
| 1:45 | Build the scenario: main and feature both edit the same line; feature has TWO commits |
| 2:30 | `git rebase main` from feature — the first commit replay conflicts immediately |
| 3:15 | `git status` mid-rebase: "You are currently rebasing... could not apply \<sha\>" |
| 4:00 | visigit: the original feature commits are untouched and still reachable via ORIG_HEAD (the pre-rebase tip); the in-progress rebase state itself lives in `.git/rebase-merge/`, a plain directory git checks for — not a ref visigit tracks, unlike MERGE_HEAD |
| 4:45 | Resolve the conflict in the file, `git add <file>` |
| 5:30 | `git rebase --continue` — the first commit replays successfully with a NEW SHA |
| 6:15 | The second commit replay ALSO conflicts (it touches the same region) — same dance again |
| 7:00 | Resolve, `git add`, `git rebase --continue` again |
| 7:45 | Rebase finishes: linear history, two new-SHA commits, ORIG_HEAD still points at the original pre-rebase tip |
| 8:30 | The escape hatches: `git rebase --skip` (drop this commit's changes entirely and move on) vs `git rebase --abort` (undo everything, back to the pre-rebase state) |
| 9:30 | Why this differs from a merge conflict: merge is one conflict for the whole integration; rebase is one potential conflict PER commit being replayed |
| 10:30 | Practical tip: if the same conflict keeps recurring on every commit, `--abort` and reach for a merge instead |
| 11:15 | Recap: `--continue` after each fix, `--skip` to drop a commit, `--abort` to bail completely |

#### Key Visual Moments
- The pre-rebase feature tip staying fully intact and visible via ORIG_HEAD while the rebase is paused mid-conflict
- A new-SHA commit node appearing after the first `--continue`, while the second commit is still pending replay
- `git rebase --abort` snapping the graph back exactly to its pre-rebase shape, as if the rebase never started
- Side-by-side terminal + diagram: a merge conflict's single `CONFLICT` message vs. a rebase's repeated "could not apply" messages

---

### EP 13 — Intermediate — origin/main Is Not main: Remote Tracking Branches

**visigit mode:** normal
**Target length:** 12–14 min
**Commands covered:** git remote add, git fetch, git pull, git push, git branch -vv

#### Why This Matters

Your local main and origin/main are two separate, independently-moving pointers, and the second one is nothing but a cached snapshot of what the remote looked like at your last fetch — it does not update itself. This distinction is the root of most "but I thought I had the latest code" confusion, and once origin/* refs are visibly separate objects in the graph instead of an abstract idea, fetch/pull/push stop being magic syncing and become exactly what they are: explicit pointer updates you control.

#### YouTube Title
> origin/main Is Not main: Watch fetch, pull, push Work

#### YouTube Description
> There are actually two "main" branches in a typical repo: your local main and origin/main (the remote tracking ref). Most people conflate them until something goes wrong. This video uses visigit to show you both refs in the same graph, what happens when they drift apart, and exactly what fetch, pull, and push do to each pointer.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Clone a repo: two mains appear in the graph immediately |
| 1:30 | origin/main is a local snapshot of the remote — it doesn't update automatically |
| 2:30 | `git fetch` — origin/main pointer moves; local main stays behind |
| 3:30 | Graph: origin/main has moved ahead; local main trails |
| 4:30 | `git merge origin/main` (or `git pull`) — local main catches up |
| 5:30 | Ahead/behind: make a local commit, see main drift ahead of origin/main |
| 6:30 | `git push` — origin/main jumps to match local main |
| 7:30 | Diverged: both local and remote have unique commits (common team scenario) |
| 8:30 | `git pull --rebase` vs `git pull` (merge): different graph shapes |
| 9:30 | `--exclude-remotes` flag: hide remote refs when the graph gets busy |
| 11:00 | `git branch -vv`: read the ahead/behind numbers from the graph |

#### Key Visual Moments
- Clone: refs/remotes/origin/main and refs/heads/main both visible from the start
- Fetch: only origin/main moves; local main unchanged
- Push: origin/main catches up to local main
- Diverged: origin/main and main pointing to different commits on the same chain

---

### EP 14 — Intermediate — Two Repos, One Screen: Watching local and origin Together

**visigit mode:** all (two monitor sessions)
**Target length:** 11–13 min
**Commands covered:** git clone, git push, git fetch, git pull (with a bare "origin" on the same machine)

#### Why This Matters

Every push, fetch, and pull you've run so far has been a black box — you've seen your side of the exchange but never the other end. Watching a real bare repository update live, side by side with your working copy, turns "the remote" from an abstract concept into a second, equally real graph that commits move between, which is the mental model every later remote-workflow episode assumes you already have.

#### YouTube Title
> git push and fetch: Watch Your Repo AND origin Update Live

#### YouTube Description
> origin/main is a snapshot inside your repo — but where's the ACTUAL origin? In this video we put a bare "origin" repository on the same machine and run a second `visigit --monitor` on it, so you watch BOTH graphs at once. Now push, fetch, and pull aren't mysterious: you see commits leave your repo and land in origin, and origin/main catch up — live, side by side.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The missing half: you've seen origin/main, but never origin itself |
| 1:00 | Make a bare origin: `git init --bare ../origin.git` (no working tree) |
| 2:00 | Terminal layout: `visigit --monitor` on your repo (left), on the bare origin (right) |
| 3:00 | `git push` — watch the commit appear in the origin graph; origin/main advances |
| 4:30 | Teammate simulation: commit in a second clone and push to origin |
| 5:30 | `git fetch` — origin/main moves in YOUR graph to match the origin graph |
| 6:30 | `git pull` (fetch + merge) — local main catches up; both graphs converge |
| 7:30 | A bare repo has no working tree: no Staged/Unstaged boxes, just the commit graph |
| 8:30 | Diverged: local and origin each advance — see it on both screens at once |
| 9:30 | Why bare: pushing to a non-bare repo's checked-out branch is rejected by default |
| 11:00 | Recap: push/fetch/pull are just commits moving between two real graphs |

#### Key Visual Moments
- Two visigit windows: your repo and the bare origin, updating independently
- A commit appearing in the origin graph the instant you push
- origin/main in your graph jumping to match origin after fetch
- The bare origin rendering as a pure commit graph (no index boxes — it has no working tree)

---

### EP 15 — Intermediate — One Remote Isn't Enough: origin, upstream, and the Fork Workflow

**visigit mode:** normal
**Target length:** 11–13 min
**Commands covered:** git remote add upstream, git remote -v, git fetch upstream, git merge upstream/main (or rebase), git push origin, git switch -c, git branch -vv

#### Why This Matters

The single-remote model from EP13 breaks down the moment you contribute to a project you don't have write access to — you need one remote that receives your work (origin, your fork) and a separate one that's the actual source of truth (upstream). This episode exists because the fork workflow is how most real open-source contribution happens, and conflating origin with "the project" is the single most common point of confusion for anyone's first pull request.

#### YouTube Title
> Git Fork Workflow: origin vs upstream, Visualized

#### YouTube Description
> Contributing to an open-source project means juggling TWO remotes: origin (your fork) and upstream (the real project). Most tutorials gloss over this. This video shows both full sets of remote-tracking refs in one visigit graph, keeps your fork's main in sync with upstream, and walks through the exact commands for a clean feature-branch contribution — without ever pushing directly to upstream.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "origin" isn't always the real project — meet upstream |
| 1:00 | Recap EP13 (origin/main) mechanics with a single remote |
| 1:45 | Scenario: clone your fork as `origin`; the real project is a second bare repo you add as `upstream` |
| 2:30 | `git remote add upstream ../upstream.git` |
| 3:15 | `git remote -v` — origin (fetch/push) vs upstream (fetch/push) listed side by side |
| 4:00 | Graph: refs/remotes/origin/main AND refs/remotes/upstream/main both visible at once |
| 4:45 | Someone else pushes to upstream directly (simulate a teammate) — upstream/main is now ahead of origin/main |
| 5:30 | `git fetch upstream` — only upstream/main moves; origin/main and local main stay untouched |
| 6:15 | `git merge upstream/main` (or `git rebase upstream/main`) — local main catches up to the real project |
| 7:00 | `git push origin main` — sync your fork's main with what you just pulled from upstream |
| 7:45 | Feature-branch workflow: `git switch -c feature/thing`, commit, `git push -u origin feature/thing` |
| 8:30 | `git branch -vv` — reads ahead/behind against `origin`, never `upstream`, for your feature branch |
| 9:15 | Why you never push directly to upstream in a fork workflow — you open a PR from origin instead |
| 10:00 | Recap: two remotes, two sets of tracking refs, one job each — upstream feeds you, origin receives your work |

#### Key Visual Moments
- Two full sets of remote-tracking refs (`origin/*` and `upstream/*`) rendered simultaneously in one graph
- upstream/main advancing on its own while origin/main and local main stay frozen, until you explicitly fetch and merge
- local main catching up to upstream/main, then origin/main catching up to local main — three pointers converging in sequence
- A feature branch's remote-tracking ref appearing only under origin/*, never under upstream/*

---

### EP 16 — Intermediate — Stash Is a Secret Commit: What git stash Actually Creates

**visigit mode:** verbose
**Target length:** 10–12 min
**Commands covered:** git stash, git stash list, git stash pop, git stash drop, git stash apply

#### Why This Matters

git stash doesn't have its own storage mechanism — it creates a genuine commit object, just one that most tools (and normal-mode visigit) don't show you by default. Realizing that a stash is a commit like any other, hanging off a ref called refs/stash, explains everything about how it behaves: why it has a SHA, why multiple stashes stack like a list, and why it isn't magic.

#### YouTube Title
> git stash Creates a Real Commit — Watch It Appear

#### YouTube Description
> git stash feels like a magic shelf that saves your work temporarily. What it actually does is create a special commit hanging off a ref called refs/stash — and that commit is only visible in visigit's verbose mode. This video shows you the hidden object, how stash entries stack up, and what pop, apply, and drop each do to the graph.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The mystery: where does stashed work go? |
| 1:00 | Start in verbose monitor mode: `visigit --mode verbose --monitor` |
| 1:45 | Make uncommitted changes on a dirty working tree |
| 2:30 | `git stash` — watch the refs/stash node appear in the graph |
| 3:30 | The stash commit: it contains both your staged and unstaged changes |
| 4:30 | `git stash list` — stash@{0}, stash@{1}... each is a commit in the graph |
| 5:30 | `git stash` again with different changes — stash@{0} and stash@{1} both visible |
| 6:30 | `git stash pop` — stash ref disappears; changes re-enter the working tree |
| 7:30 | `git stash apply` vs `git stash pop`: apply leaves the stash entry; pop removes it |
| 8:30 | `git stash drop` — entry removed from graph |
| 9:30 | Why stash is a commit: it has a SHA and behaves like any other commit — but it's only protected from garbage collection as long as refs/stash (or its reflog) still points to it, exactly like any other ref |
| 10:30 | Stash is only visible in verbose mode — explain why (include_stash flag) |

#### Key Visual Moments
- Stash refs ONLY appear in verbose mode (the first time students see this distinction)
- refs/stash → stash commit node appearing after `git stash`
- Multiple stash entries stacking up
- stash@{0} node disappearing on `git stash pop`

---

### EP 17 — Intermediate — Cherry-Pick: Copying a Commit (and Why the SHA Changes)

**visigit mode:** normal
**Target length:** 10–12 min
**Commands covered:** git cherry-pick, git cherry-pick --no-commit, git cherry-pick --abort

#### Why This Matters

A commit's SHA is a hash of its content, and its content includes its parent's SHA — so replaying the exact same change onto a different parent necessarily produces a different SHA, even though nothing about the change itself changed. This is the clearest hands-on proof in the whole series that git identity is about content and lineage together, not just content, and it's the same fact that explains why rebase and amend also produce new SHAs.

#### YouTube Title
> git cherry-pick: Watch the Commit SHA Always Change

#### YouTube Description
> cherry-pick lets you take one specific commit from any branch and replay it somewhere else. But the resulting commit always has a different SHA — even though the changes are identical. This video explains why using visigit: the parent commit is different, so the content of the commit object is different, so the SHA is different. You'll see it happen live.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The use case: hotfix on main that also needs to go to a release branch |
| 1:00 | Build the scenario: main and release/1.0 diverged from a common base |
| 2:00 | Make a critical fix commit on main; record its SHA |
| 3:00 | `git checkout release/1.0` |
| 3:30 | `git cherry-pick <sha>` — a NEW commit node appears on release/1.0 |
| 4:30 | New SHA despite same changes: show both nodes in graph; different SHAs, different parents |
| 5:30 | Why the SHA differs: the commit object contains the parent SHA — change the parent, change the SHA |
| 6:30 | `git cherry-pick --no-commit`: changes land in index; you commit manually |
| 7:30 | Multiple cherry-picks: each creates its own new node |
| 8:30 | Cherry-pick a merge commit: `--mainline` flag |
| 9:30 | When to prefer cherry-pick over merge/rebase |
| 10:30 | Downside: diverging histories can accumulate if overused |

#### Key Visual Moments
- Original commit node on main with SHA X
- New commit node on release/1.0 with SHA Y — same label content, different node identity
- Parent edge from Y to the release branch tip (not to X's parent)
- The original commit X still in the graph on main, untouched

---

### EP 18 — Intermediate — You Didn't Lose It: Finding Commits with git reflog

**visigit mode:** normal
**Target length:** 12–14 min
**Commands covered:** git reflog, git reset --hard, git checkout SHA, git branch recover

#### Why This Matters

git almost never deletes a commit the instant it becomes unreachable — it just stops being able to find it through any ref, while the object itself sits untouched in .git/objects for weeks. reflog is the log of everywhere HEAD has pointed, which means "I lost my commits" is almost always actually "I lost the address," and this episode is about how to look the address back up.

#### YouTube Title
> git reflog: Watch "Lost" Commits Reappear

#### YouTube Description
> You ran git reset --hard or git rebase and now your commits are "gone." They're not — git keeps every commit in the object store for at least 30 days. git reflog shows you the history of where HEAD has been, giving you the SHA of every commit you've ever had checked out. This video shows you how to find and recover them using visigit to confirm the work is really still there.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The disaster scenario: commits gone after reset --hard |
| 1:00 | Build a chain: three commits on main |
| 2:00 | `git reset --hard HEAD~2` — main jumps back two commits; the old tip stays visible via ORIG_HEAD, but ORIG_HEAD only remembers ONE prior position |
| 3:00 | The trap: do another operation and ORIG_HEAD is overwritten — now where did the work go? |
| 3:30 | `git reflog` — full history of HEAD positions with SHAs |
| 4:30 | Find the SHA of the "lost" commit in the reflog output |
| 5:30 | `git checkout <lost-sha>` — detach HEAD at the commit; it REAPPEARS in visigit |
| 6:30 | The commit was never deleted — just unreachable from any ref |
| 7:30 | `git branch recover <lost-sha>` — new branch label rescues the work |
| 8:30 | `git checkout -` — return to main; the recover branch is still in the graph |
| 9:30 | Reflog for branch tips: `git reflog show main` |
| 10:30 | When reflog fails: commits older than 30 days get garbage collected |
| 11:30 | `git gc --prune=now` for demo: permanently remove unreachable objects |

#### Key Visual Moments
- The pre-reset tip staying visible via ORIG_HEAD after `reset --hard`; reflog recovering commits from BEFORE that, which ORIG_HEAD no longer remembers
- A "lost" commit reappearing when HEAD is detached at the SHA found in the reflog
- `git branch recover <sha>` making the commits permanently reachable again
- Before/after: the "lost" work visible in the graph once a branch ref points at it

---

### EP 19 — Intermediate — Git's Safety Nets: ORIG_HEAD, FETCH_HEAD, and Friends

**visigit mode:** normal
**Target length:** 10–12 min
**Commands covered:** observing ORIG_HEAD, FETCH_HEAD, MERGE_HEAD, CHERRY_PICK_HEAD, BISECT_HEAD

#### Why This Matters

ORIG_HEAD, MERGE_HEAD, FETCH_HEAD, CHERRY_PICK_HEAD, and BISECT_HEAD are not five unrelated features to memorize — they're the same pattern repeated five times: before doing something to HEAD that might need undoing or referencing later, git writes down where things stood in an ordinary ref file. Recognizing that pattern means the next unfamiliar ALL_CAPS_HEAD you see in git's output won't need a new mental model, just the one you already have.

#### YouTube Title
> ORIG_HEAD, FETCH_HEAD: Watch Git's Hidden Safety Refs

#### YouTube Description
> You've seen them flash by: ORIG_HEAD after a reset, MERGE_HEAD during a conflict, FETCH_HEAD after a fetch. These are git's pointer files — special refs git writes so YOU (and git) can recover and reason about what just happened. Most tools hide them; visigit shows them. This video gathers them in one place so you understand the safety net under every "dangerous" command.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The refs you keep seeing but nobody explains |
| 1:00 | ORIG_HEAD: written by reset, rebase, and merge — the "where I was" pointer |
| 2:30 | Recover from `git reset --hard` using ORIG_HEAD, live |
| 3:30 | MERGE_HEAD: the other side of an in-progress merge (callback to EP06) |
| 4:30 | CHERRY_PICK_HEAD: the commit being applied during a cherry-pick conflict |
| 5:30 | FETCH_HEAD: what `git fetch` just brought down |
| 6:30 | BISECT_HEAD: only written when a bisect session runs with `--no-checkout` — a plain `git bisect start`/`good`/`bad` session detaches HEAD directly at the midpoint instead and never writes this ref (callback to EP26's bonus segment) |
| 7:30 | The one exception: `git commit --amend` writes NO ORIG_HEAD (callback to EP08) |
| 8:30 | Why visigit shows these: they ARE refs — real pointers into the object store |
| 9:30 | The mental model: almost nothing is ever truly lost until git gc |
| 11:00 | Recap: every scary command leaves a breadcrumb — now you can see them |

#### Key Visual Moments
- ORIG_HEAD appearing after reset/rebase/merge, keeping the "old" tip reachable
- MERGE_HEAD / CHERRY_PICK_HEAD appearing only mid-operation, then vanishing on completion
- FETCH_HEAD shown as an ordinary ref node with no edge label; BISECT_HEAD shown the same way, but only during a `--no-checkout` bisect session
- The contrast: amend leaves no safety net, so its old commit really is gone from the graph

---

### EP 20 — Intermediate — Finding the Needle: git blame, log -S, and log --grep

**visigit mode:** normal
**Target length:** 11–13 min
**Commands covered:** git log --grep, git log --author, git log -S, git log -G, git blame, git blame -L, git show

#### Why This Matters

Most of what you do with git day to day isn't changing history, it's asking questions about history that already exists — who wrote this, when did this string first appear, why does this line look the way it does. This episode is a deliberate change of pace from "watch the graph change" to "watch the search narrow," because archaeology skills are just as core to using git well as the mutating commands are.

#### YouTube Title
> git blame, log -S, and log --grep: See Who Changed What

#### YouTube Description
> Not every git episode is about changing the graph — sometimes you just need to search it. This video covers the three tools every developer eventually needs: git log --grep and --author to filter commits by metadata, git log -S (the "pickaxe") to find exactly when a string was added or removed, and git blame to see who last touched every line. We use a buried one-line bug to show all three working together to pin down the exact commit that caused it.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "who wrote this line, and why" — the question every dev asks eventually |
| 1:00 | Note: this episode doesn't change the graph — visigit renders the map once, then we search the terrain |
| 1:30 | Build a history with an intentionally buried change (a bug introduced 8 commits back, one line) |
| 2:30 | `git log --oneline --graph --all` next to the static visigit diagram — same DAG, two views |
| 3:15 | `git log --grep "fix"` — filter commits by message text |
| 4:00 | `git log --author "name"` — filter by author |
| 4:45 | `git log -S "old_value"` — the "pickaxe": find commits that ADDED or REMOVED a literal string |
| 5:45 | `git log -G "regex"` — pickaxe's regex sibling, matches diff lines by pattern |
| 6:45 | Pin down the exact commit that introduced the bug using `-S` |
| 7:30 | `git blame app.py` — every line annotated with the commit and author that last touched it |
| 8:30 | `git blame -L 10,20 app.py` — scope blame to a line range |
| 9:15 | `git show <sha>` — full diff of the commit blame pointed at |
| 10:00 | The trap: blame shows the LAST commit to touch a line, not necessarily the one that introduced the bug — `git blame -w` ignores whitespace, `--ignore-rev` skips a known noisy reformat commit |
| 11:00 | Recap: grep/author search by metadata, pickaxe searches by content, blame searches by line |

#### Key Visual Moments
- The static diagram used as a reference map while terminal output narrows down to a single commit
- `-S` narrowing a full history down to the one commit where a string's occurrence count changed
- `git blame` output lining up with the SHA of a node already visible in the diagram

---

### EP 21 — Intermediate — Partial Commits: What git add -p Actually Stages

**visigit mode:** verbose
**Target length:** 10–12 min
**Commands covered:** git add -p, git add -i, git diff, git restore -p, git commit -p

#### Why This Matters

The index isn't required to match either your last commit or your current working tree exactly — it's a genuinely independent third state that you can shape by hand, one hunk at a time. Seeing the same file exist simultaneously as two different blobs, one staged and one not, is the clearest possible proof that "staging" is a real, separate editing step and not just a formality before commit.

#### YouTube Title
> git add -p: Watch One File Split Into Two Blobs

#### YouTube Description
> git add -p lets you stage half a file's changes and leave the rest for later. Most people run it on faith. This video shows you exactly what it does to the object store: the SAME file appears in visigit's verbose mode in BOTH the Staged box and the Unstaged box at once, each with a DIFFERENT blob SHA. Commit, and only the staged blob becomes part of history — the rest stays right where you left it.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "one file, two unrelated changes — you want to commit only one" |
| 1:00 | Start verbose monitor |
| 1:30 | Edit app.py in two unrelated places (a real fix + an unrelated debug print) |
| 2:15 | `git diff` — both hunks show as one big unstaged change |
| 3:00 | `git add -p app.py` — walk the hunk-by-hunk prompt: y/n/s/e |
| 3:45 | Stage only the real fix hunk (`y`), skip the debug-print hunk (`n`) |
| 4:30 | visigit verbose graph: app.py now appears in BOTH the Staged box AND the Unstaged box, with two DIFFERENT blob SHAs |
| 5:30 | Explain: the staged blob is the index version (fix only); the unstaged blob is the working-tree version (fix + debug print) |
| 6:15 | `git commit -m "fix: real bug"` — only the staged hunk's blob becomes part of the tree; the debug print stays uncommitted |
| 7:15 | `git status` confirms app.py is STILL modified after the commit |
| 7:45 | `git restore -p app.py` — interactively discard (or unstage) the leftover hunk |
| 8:45 | `e` (manual edit) mode: briefly show editing a hunk by hand for a partial line change |
| 9:30 | Recap: `-p` lets the index and the working tree diverge on purpose, one hunk at a time; visigit's Staged/Unstaged boxes make that split visible instead of abstract |

#### Key Visual Moments
- app.py showing up as two separate nodes (Staged and Unstaged) with two different blob SHAs simultaneously
- The commit consuming only the Staged blob; the Unstaged node for app.py surviving the commit untouched
- Before/after: one Unstaged node with a combined diff, split into a Staged node (partial) plus a smaller Unstaged node (remainder)

---

[Curriculum index](README.md) | [<- Beginner](01-beginner.md) | [Advanced ->](03-advanced.md)
