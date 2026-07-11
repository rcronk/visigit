[Curriculum index](README.md) | [<- Internals](04-internals.md)

---

## Tier 5 — Reference: Configuration & Housekeeping

These five episodes round out "everything you'd want to know about git." They're lighter on
diagram-watching than the rest of the series — some (config, rerere) barely touch the object
graph at all — so they're framed as compact reference episodes rather than full diagram
walkthroughs.

---

### EP 35 — Reference — Making Git Yours: git config, Aliases, and .gitconfig

**visigit mode:** terminal only — no diagram, config doesn't touch the object store or refs
**Target length:** 8–10 min
**Commands covered:** git config --global user.name/user.email, git config --list --show-origin, git config --global alias.X, git config --global core.editor, git config --global init.defaultBranch

#### Why This Matters

None of the shortcuts and identity settings in this episode touch the object graph at all — config lives entirely outside the DAG, in plain text files that just happen to control who git says you are and what your commands expand to. Understanding the three-scope precedence (system, global, local) is what stops "why does this repo use a different email" from being a mystery.

#### YouTube Title
> git config --global Explained: Identity, Aliases, and the Three Config Files That Run Everything

#### YouTube Description
> Every commit's author field, every default editor, every shortcut you type — it all comes from git config. This episode has no diagram, because config doesn't touch refs or objects; it's pure setup. We cover the three config scopes and their precedence, building real aliases (including a shell-out alias), and where every setting physically lives on disk.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: three levels of config that silently decide who you are in every commit |
| 1:00 | `git config --global user.name` / `user.email` — what actually goes into every commit's author field |
| 2:00 | `git config --list --show-origin` — see exactly which file each setting came from |
| 3:00 | The three scopes: --system, --global, --local, and precedence (local wins) |
| 4:00 | Per-repo override: `git config user.email work@company.com` inside one repo only |
| 5:00 | Aliases: `git config --global alias.st status`, `alias.lg "log --graph --oneline --all"` |
| 6:30 | A shell-out alias: `alias.undo "!git reset --soft HEAD~1"` — the `!` prefix runs a real shell command |
| 7:30 | `git config --global core.editor "code --wait"` — set your commit-message editor |
| 8:15 | `git config --global init.defaultBranch main` — why new repos say "main" (or don't) |
| 9:00 | Where it all lives: `~/.gitconfig` and `.git/config`, opened side by side in a text editor |
| 9:45 | Recap: config makes every other episode's commands shorter and safer |

#### Key Visual Moments
- No diagram this episode — call that out explicitly on screen
- `--show-origin` output pinpointing which config file wins for a given setting
- A raw `.gitconfig` file on screen, mapped line-by-line to the `git config` commands that wrote it
- The custom `git lg` alias reproducing the same `--graph` output used throughout the whole series, this time as a one-word command

---

### EP 36 — Reference — Line Endings and .gitattributes: Taming Cross-Platform Diffs

**visigit mode:** verbose
**Target length:** 8–10 min
**Commands covered:** .gitattributes, git config core.autocrlf, git add --renormalize, git diff --stat

#### Why This Matters

A line-ending mismatch produces a diff that touches every line of a file with a change that isn't really there, and core.autocrlf only patches over the symptom on your machine — .gitattributes is the fix that travels with the repository itself, because it's a committed file, not a personal setting. This episode exists because line-ending "diff bombs" are one of the most common sources of team friction, and the fix is almost always simpler than the confusion it causes.

#### YouTube Title
> "Every File Changed" But You Didn't Touch Anything: Line Endings, autocrlf, and .gitattributes

#### YouTube Description
> Windows uses CRLF, Unix uses LF, and a repo with mixed line endings produces diffs that touch every line of every file for no reason. This episode covers core.autocrlf (a personal, local setting) and the better fix — a committed .gitattributes file that makes line-ending rules part of the repo itself — plus the one command that cleanly renormalizes an already-mixed repo.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "it says every file changed, but I didn't touch anything" — the classic line-ending diff bomb |
| 1:00 | The cause: Windows CRLF vs Unix LF, and a repo with mixed line endings |
| 2:00 | `git config core.autocrlf true/input/false` — what each setting does on checkout/commit |
| 3:00 | The better fix: `.gitattributes` — `* text=auto`, `*.sh text eol=lf`, `*.png binary` |
| 4:30 | Create a `.gitattributes`, then `git add --renormalize .` — rewrites tracked files' line endings to match the new rules in a single, clean commit |
| 5:30 | Verbose graph: a new blob SHA for every renormalized file, but `git diff --stat` shows the change is explicitly whitespace/line-ending only, not silent |
| 6:30 | `.gitattributes` for binary files: marking `*.png binary` stops git from ever trying to diff or merge them as text |
| 7:15 | Custom diff drivers for binary formats (brief mention) |
| 8:00 | Recap: autocrlf is a personal/local setting; .gitattributes is a committed, repo-wide contract — prefer the latter for teams |

#### Key Visual Moments
- Every tracked text file getting a new blob SHA in one commit after `--renormalize`, visibly distinct in cause from EP31's "real content change" blob updates
- `.gitattributes` itself rendered as an ordinary tracked blob — it's just a file, with no special node type

---

### EP 37 — Reference — Never Resolve the Same Conflict Twice: git rerere

**visigit mode:** normal (the graph is a constant backdrop across both rebases — the point is that it doesn't change, only your manual effort does)
**Target length:** 8–9 min
**Commands covered:** git config --global rerere.enabled true, git rerere diff, git rerere status, git rerere forget

#### Why This Matters

rerere is built on a simple observation: a conflict is defined by its content, not by when it happens, so if you've resolved this exact conflict before, git can just remember and reapply your resolution. This matters most for exactly the situation that makes rebase conflicts painful (EP12) — a long-lived branch rebased repeatedly against a moving main — where rerere turns "resolve this again" into "already handled."

#### YouTube Title
> git rerere: Stop Resolving the Same Rebase Conflict Every Single Time

#### YouTube Description
> Rebasing a long-lived branch against a moving main means resolving the SAME conflict over and over. git rerere ("reuse recorded resolution") remembers how you resolved a conflict and auto-applies that resolution the next time it sees the identical conflict. This episode runs the same rebase twice — once manually, once with rerere doing the work — on an identical resulting graph, to make clear that rerere changes your effort, not your history.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: rebasing the same long-lived branch against main, over and over, resolving the SAME conflict every single time |
| 1:00 | `git config --global rerere.enabled true` — "reuse recorded resolution" |
| 2:00 | First rebase: hit a conflict, resolve it manually, `git add`, `git rebase --continue` — rerere silently records the resolution |
| 3:00 | `.git/rr-cache/` — where recorded resolutions live, keyed by a hash of the conflict content |
| 3:45 | Second rebase (same branch, main has moved again): the SAME conflict appears |
| 4:30 | `git rerere diff` — shows the recorded resolution about to be auto-applied |
| 5:00 | git auto-applies it and stages the file — no manual edit needed this time, just `git rebase --continue` |
| 6:00 | `git rerere status` — see which paths have recorded resolutions in play |
| 6:45 | When it breaks: if the conflicting hunk's surrounding context changes, rerere won't match and you resolve manually again (and it re-records) |
| 7:30 | `git rerere forget <path>` to discard a bad recorded resolution |
| 8:00 | Recap: rerere doesn't change the graph, it changes how much manual work future conflicts cost |

#### Key Visual Moments
- Two rebases producing an IDENTICAL resulting graph shape, but the second one requiring zero manual conflict edits
- `.git/rr-cache/` contents shown side-by-side with the conflict markers they resolved

---

### EP 38 — Reference — Proving It Was You: Signing Commits and Tags

**visigit mode:** verbose (for the cat-file callback)
**Target length:** 10–11 min
**Commands covered:** git config --global commit.gpgsign true, git config --global gpg.format ssh, git commit -S, git tag -s, git verify-commit, git verify-tag, git log --show-signature

#### Why This Matters

A commit's author field is plain text that anyone with write access can set to anything — signing is the mechanism that actually binds a commit's exact content to a cryptographic identity, checkable by anyone, forever. This episode matters more every year as supply-chain attacks target exactly this gap: an unsigned commit's authorship is a claim, a signed one's is a proof.

#### YouTube Title
> Anyone Can Put Your Name on a Commit — Signing Proves It Was Actually You

#### YouTube Description
> A commit's author field is just a text string; anyone can type your name and email into it. Signing binds a real cryptographic identity to a commit's exact content, permanently. This episode covers both the GPG path and the newer, simpler SSH-key signing path, opens a signed commit with git cat-file to show exactly where the signature lives inside the object, and covers signed tags too.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: any commit's author field is just a text string — anyone can claim to be you |
| 1:00 | Recap: EP25 (tags) mentioned signed tags briefly; this episode does the whole thing, GPG and SSH signing |
| 2:00 | GPG path: `git config --global user.signingkey <keyid>`, `git config --global commit.gpgsign true` |
| 3:00 | SSH path (modern, simpler): `git config --global gpg.format ssh`, `git config --global user.signingkey ~/.ssh/id_ed25519.pub` |
| 4:00 | `git commit -S -m "signed commit"` — commit as usual, GPG/SSH prompts for a signature |
| 5:00 | `git log --show-signature` — "Good signature from..." verification inline with the log |
| 5:45 | The signature lives INSIDE the commit object itself — `git cat-file -p <sha>` shows a `gpgsig` header block (callback to EP33) |
| 6:45 | `git verify-commit <sha>` — standalone verification |
| 7:15 | Signed tags: `git tag -s v1.0 -m "Release 1.0"` and `git verify-tag v1.0` |
| 8:00 | What signing does NOT protect: it proves who committed, not that the code is bug-free or that the diff itself passed review |
| 8:45 | GitHub's "Verified" badge is exactly this check, run server-side |
| 9:15 | Recap: signing binds a cryptographic identity to a commit object's exact content, permanently |

#### Key Visual Moments
- `git cat-file -p` output growing a new `gpgsig` block on a signed commit vs. an unsigned sibling commit, both otherwise identical
- `--show-signature` output lining up against the same commit node already on screen in the diagram

---

### EP 39 — Reference — Big Repos, Small Checkouts: Sparse Checkout and Partial Clone

**visigit mode:** verbose
**Target length:** 10–12 min
**Commands covered:** git clone --filter=blob:none, git sparse-checkout init --cone, git sparse-checkout set, git sparse-checkout list, git sparse-checkout add, git sparse-checkout disable

#### Why This Matters

Shallow clones (EP34) trim how much history you download; sparse checkout and partial clone trim something else entirely — which files exist on disk and which blobs ever get fetched — and the two axes are independent and combinable. This episode exists because as repos grow into monorepo territory, "clone everything" stops being a viable default, and understanding which knob controls which resource is what makes working in a huge repo feel normal instead of painful.

#### YouTube Title
> Sparse Checkout and Partial Clone: Work in a 50-Project Monorepo Without Downloading All 50

#### YouTube Description
> Shallow clones (EP34) trim history depth. Sparse checkout and partial clone trim a completely different axis: which files exist on disk and which blobs ever get downloaded. This episode clones with --filter=blob:none so file contents fetch lazily, then narrows the working tree to one directory with sparse-checkout — while the full commit graph, for every project in the monorepo, stays completely intact and visible.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: a monorepo with 50 top-level projects — you only work in one of them |
| 1:00 | Recap EP34 (shallow clones): that trims HISTORY depth; this episode trims the WORKING TREE and object DOWNLOADS instead — a different axis entirely |
| 2:00 | `git clone --filter=blob:none <repo>` — full commit history downloads, but file CONTENTS (blobs) download lazily on demand |
| 3:00 | `git sparse-checkout init --cone` — switch to cone-mode sparse checkout |
| 3:45 | `git sparse-checkout set services/api` — working tree collapses to just that directory |
| 4:30 | `ls` — the other 49 project directories are simply gone from disk, though every commit that ever touched them is still in the object DAG |
| 5:15 | Checking out a commit that touches an out-of-cone file: git fetches that one blob on demand (watch a quick fetch happen) |
| 6:15 | `git sparse-checkout list` — see the current cone |
| 6:45 | Widen it: `git sparse-checkout add services/billing` |
| 7:15 | `git sparse-checkout disable` — back to a full working tree (blobs still fetched lazily under `--filter`) |
| 8:00 | visigit note: the commit graph itself (refs, commits, trees) looks completely normal in verbose mode — sparse checkout and partial clone only affect which BLOBS exist locally and which files are materialized on disk, not the DAG shape |
| 8:45 | Recap: shallow = less history (EP34), partial clone = fewer blobs, sparse checkout = smaller working tree — three independent knobs, often combined for huge repos |

#### Key Visual Moments
- The graph itself (commits/trees) rendering fully normal and complete in verbose mode, even though most blobs haven't been downloaded yet — makes visible that "the DAG" and "the file contents" are separate concerns
- The working tree on disk shrinking to one directory while `git log --all` still shows full project history
- A one-off blob fetch happening live the moment a sparse boundary is crossed

---

[Curriculum index](README.md) | [<- Internals](04-internals.md)
