[Curriculum index](README.md) | [<- Advanced](03-advanced.md) | [Reference ->](05-reference.md)

---

## Tier 4 — Internals: Inside Git

---

### EP 29 — Internals — Inside a Commit: blob, tree, commit — Git's Four Object Types

**visigit mode:** verbose
**Target length:** 13–15 min
**Commands covered:** git commit (step-by-step observation)

#### Why This Matters

Every git command you've run in this series has ultimately been manipulating exactly four object types — blob, tree, commit, tag — hashed and stored by content. This episode is the one where the abstraction finally opens up: "commit" stops being a verb you perform and becomes a noun you can point at, with a SHA, a tree, and a parent, exactly like every other object in the store.

#### YouTube Title
> Watch Inside a git commit: blob, tree, and commit

#### YouTube Description
> Every git commit creates three types of objects: blobs (file contents), trees (directory listings), and a commit object (metadata + pointer to root tree). This video uses visigit's verbose mode to show you all three appearing in the graph the moment you run git commit — and explains the fourth object type (annotated tags) while it's fresh. By the end you'll understand exactly what git is storing on disk.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The premise: git is a content-addressable object store with a DAG on top |
| 1:00 | The four object types: blob, tree, commit, tag — brief overview |
| 2:00 | Start verbose monitor: `visigit --mode verbose --monitor` |
| 3:00 | `echo "hello" > hello.txt && git add hello.txt` — Staged Changes box appears |
| 4:00 | The blob object: file content hashed with SHA-1 (now SHA-256 capable) |
| 5:00 | `git commit -m "initial"` — three new nodes appear: commit → tree → blob |
| 6:30 | Walk through each node: what does each one store? |
| 7:30 | Add a second file: `src/core.py` in a subdirectory |
| 8:30 | Commit — root tree gets a child tree node for `src/`; child tree points to `core.py` blob |
| 9:30 | Each directory level is its own tree object with its own SHA |
| 10:30 | Commit object: parent SHA + tree SHA + author + committer + message |
| 12:00 | How this design enables fast branching: branches are just pointers to commit objects |
| 13:30 | Recap diagram: the full object graph for a two-file, two-directory, two-commit repo |

#### Key Visual Moments
- Staged Changes box appearing immediately on `git add`
- All three object types appearing simultaneously on `git commit`
- Child tree node for subdirectory below root tree
- Edge labels: "tree" from commit → root tree; filename labels from tree → blob

---

### EP 30 — Internals — Submodules vs Subtrees: Pointer or Merged Files?

**visigit mode:** verbose
**Target length:** 12–14 min
**Commands covered:** git submodule add, git subtree add

#### Why This Matters

Including one repository inside another sounds like one problem, but git offers two genuinely different solutions to it: a submodule stores a pointer (a gitlink) to another repo's commit, while a subtree merges that repo's actual files into yours as ordinary blobs. They look similar from the command line and are almost opposite at the object level, which is exactly why picking between them by habit instead of understanding causes so much team friction.

#### YouTube Title
> git Submodule vs Subtree: See Pointer vs Merged Files

#### YouTube Description
> Two ways to include one repo inside another, and they couldn't be more different under the hood. A submodule stores a gitlink — a pointer to a specific commit in another repo — which visigit shows as a distinct node. A subtree merges the other repo's files directly into your tree as ordinary blobs, with its history as a second parent. This video opens both in verbose mode so you can see exactly what git stores in each case.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Same goal, opposite mechanics |
| 1:00 | `git submodule add ../lib lib` — what actually lands in your tree? |
| 2:00 | Verbose graph: a gitlink node (mode 160000) pointing at the submodule's commit |
| 3:00 | The .gitmodules file is a real blob; the submodule itself is just a pointer |
| 4:00 | Key point: your repo does NOT contain the submodule's files — only its SHA |
| 5:30 | Reset and try the other way: `git subtree add --prefix=vendor/lib ../lib main` |
| 6:30 | Verbose graph: the library's files appear as NORMAL blobs under vendor/lib |
| 7:30 | The subtree add is a MERGE commit — the library's history is a second parent |
| 8:30 | Content-addressable bonus: the imported tree is deduplicated in the graph |
| 9:30 | Trade-offs: submodule (light pointer, needs `submodule update`) vs subtree (self-contained) |
| 11:00 | Why visigit renders a gitlink distinctly but a subtree as plain objects |
| 13:00 | Recap: submodule = a SHA pointer node; subtree = the actual files + a merge |

#### Key Visual Moments
- Submodule: a distinct `gitlink` node pointing at another repo's commit, beside the .gitmodules blob
- Subtree: the imported files as ordinary blobs/trees under the prefix directory
- The subtree-add merge commit with two parents (your history + the imported history)
- Tree deduplication: the imported subtree sharing a tree node with the vendored copy

---

### EP 31 — Internals — Same File, Same SHA: How Git Never Stores the Same Content Twice

**visigit mode:** verbose
**Target length:** 11–13 min
**Commands covered:** git add, git commit (observing SHA reuse across commits)

#### Why This Matters

Content-addressable storage means identical content always hashes to the identical object, no matter how many commits or files reference it — git isn't storing a thousand copies of your README, it's storing one blob with a thousand pointers to it. This is the single idea that makes git's storage efficient at any scale, and it's also why a rename with no content change is nearly free.

#### YouTube Title
> Same File, Same SHA: Watch Git Avoid Storing Duplicates

#### YouTube Description
> Every git object is identified by the SHA of its content. This means if you commit a file and don't change it, the next commit reuses exactly the same blob object — the same node in the graph. This video makes content-addressable storage visible by showing two commits in verbose mode sharing a blob node, and then showing what happens when you do change the file.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The claim: git doesn't copy files when you commit — it deduplicates |
| 1:00 | Create a repo with README.md and app.py; commit both |
| 2:00 | Verbose graph: commit 1 → tree → two blobs |
| 3:00 | Modify only app.py; `git commit -m "update app"` |
| 4:00 | Verbose graph: commit 2 → NEW tree → NEW blob for app.py + SAME blob for README.md |
| 5:30 | The README.md node: same SHA, same node, shared between both commits |
| 6:30 | Why: the blob SHA is a hash of the file content; same content = same hash |
| 7:30 | Consequence: renaming a file without changing its content reuses the same blob |
| 8:30 | Consequence: a file that appears in 1000 commits unchanged is stored exactly once |
| 9:30 | Trees are also deduplicated: if a subtree's contents don't change, its SHA doesn't change |
| 10:30 | When does duplication happen? Different content always = different SHA |
| 11:30 | Packfiles: git eventually delta-compresses similar blobs for network efficiency |

#### Key Visual Moments
- Two different commit nodes sharing the same README.md blob node (one blob, two inbound edges)
- New blob appearing for app.py with a different SHA after modification
- Tree node reuse: unchanged subtrees share the same tree SHA across commits

---

### EP 32 — Internals — The Staging Area Exposed: What git add Actually Does to the Object Store

**visigit mode:** verbose
**Target length:** 12–14 min
**Commands covered:** git add, git restore --staged, git rm --cached, git diff --staged

#### Why This Matters

"git add stages the file" undersells what actually happens: git computes a hash of your content and writes a real blob object to .git/objects immediately, before you've committed anything. The staging area isn't a to-do list of filenames, it's a list of blob SHAs — and once you've watched that blob appear in the object store the instant you run add, the difference between the working tree, the index, and HEAD stops being three abstract states and becomes three concrete sets of pointers you can inspect.

#### YouTube Title
> Watch git add Create a Blob Object Before You Commit

#### YouTube Description
> Most tutorials say "git add stages the file." What it actually does is compute the SHA of your file's content, write a blob object to .git/objects, and record the SHA in the index. The blob exists even before you commit. visigit's verbose mode makes this visible: the staged file appears in the graph with its blob SHA the moment you run git add — no commit required.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | The index (staging area) is not just a list of files — it's a list of blob SHAs |
| 1:00 | Start fresh repo in verbose monitor mode |
| 2:00 | Create README.md; DO NOT run git add yet — Untracked box shows it |
| 3:00 | `git add README.md` — Staged Changes box appears with file name + blob SHA |
| 4:00 | The blob is already in `.git/objects` — the commit hasn't happened yet |
| 5:00 | `git commit` — Staged Changes disappears; commit + tree + blob chain appears |
| 6:00 | Edit README.md without staging: Unstaged Changes box appears with new SHA |
| 7:00 | Two SHAs visible: committed blob (in tree) vs working-tree blob (in Unstaged) |
| 8:00 | `git add README.md` again — Unstaged clears; Staged Changes shows new SHA |
| 9:00 | `git restore --staged README.md` — remove from staging, blob still in object store |
| 10:00 | `git rm --cached README.md` — remove from index but keep in working tree |
| 11:00 | `git diff --staged`: compares index blob SHAs to HEAD tree blob SHAs |
| 12:30 | Recap: add = write blob + update index; commit = write tree + write commit object |

#### Key Visual Moments
- Untracked box: file name only, no SHA (file not yet an object)
- Staged Changes box: file name + blob SHA (the blob object exists)
- Unstaged Changes box: modified tracked file with new SHA vs committed SHA
- All three boxes potentially visible simultaneously for different files

---

### EP 33 — Internals — All the Way Down: git cat-file, .git/objects, and Pack Files

**visigit mode:** verbose + terminal (git cat-file)
**Target length:** 14–16 min
**Commands covered:** git cat-file -p/-t/-s, git hash-object, ls .git/objects/, git gc, git verify-pack

#### Why This Matters

Every diagram this series has drawn is a picture of real files sitting in .git/objects, and this episode is where you stop trusting the picture and go read the bytes yourself. cat-file, hash-object, and a raw ls of the object directory are the ground truth that everything else in the series has been representing — seeing the same SHA in the terminal and in the diagram is the moment the abstraction fully collapses into "it's just files on disk."

#### YouTube Title
> git cat-file: See What's Actually Inside .git/objects

#### YouTube Description
> You've seen the object graph in visigit. Now let's open the objects themselves. git cat-file -p <sha> prints the raw content of any git object. In this video we crack open blobs, trees, and commits in the terminal alongside the verbose diagram — showing you exactly what bytes are stored on disk and how git's SHA hash is computed. We also explain how pack files compress thousands of loose objects into an efficient bundle.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Recap: we know the object types; now let's read the actual bytes |
| 1:00 | Build a two-commit repo; start verbose monitor alongside a terminal |
| 2:00 | `ls .git/objects/` — two-character prefix directories |
| 2:30 | A blob: `git cat-file -t <blob-sha>` (type) and `git cat-file -p <blob-sha>` (content) |
| 3:30 | Content is exactly the file content; SHA is SHA1("blob " + length + "\0" + content) |
| 4:30 | A tree: `git cat-file -p <tree-sha>` — mode + type + sha + filename per entry |
| 5:30 | Cross-reference with visigit verbose graph: tree entries match graph edges |
| 6:30 | A commit: `git cat-file -p <commit-sha>` — tree, parent, author, committer, message |
| 7:30 | `git hash-object --stdin`: compute SHA for any content |
| 8:30 | Verify: `echo "hello" | git hash-object --stdin` == blob SHA from earlier commit |
| 9:30 | `git gc` — loose objects become a pack file: `.git/objects/pack/*.pack` |
| 10:30 | `git verify-pack -v *.pack` — see every object in the pack with type and size |
| 11:30 | Delta compression: how pack files store object diffs instead of full content |
| 13:00 | The full picture: git is just a key-value store + a DAG + some ref pointers |
| 14:30 | What's next in this series: shallow-clone boundary commits (EP34) and partial/sparse clones (EP39) both build directly on the object model you just saw |

#### Key Visual Moments
- Verbose graph SHA labels matching the SHAs shown in `git cat-file` terminal output
- The identical blob SHA appearing in both the graph node and `ls .git/objects/` output
- Pack file creation: loose object files disappear from `.git/objects/`; pack file appears

---

### EP 34 — Internals — Thin Slices: Shallow Clones and Grafted History

**visigit mode:** normal
**Target length:** 10–12 min
**Commands covered:** git clone --depth N, git log, cat .git/shallow, git fetch --unshallow

#### Why This Matters

A shallow clone's oldest commit renders with no parent, exactly like a true repository root or an orphan branch — but it's neither; it's an honest gap where parent objects were deliberately never downloaded. Recognizing that "parentless in the graph" doesn't always mean "root of history" is what keeps a shallow clone from looking like data corruption, and understanding the boundary mechanism is what makes fetch --unshallow's "graph grows backward" moment make sense instead of feeling like magic.

#### YouTube Title
> git clone --depth 1: Watch a Shallow Clone Fake History

#### YouTube Description
> git clone --depth 1 downloads a huge repo almost instantly by simply not fetching most of its history. But the oldest commit you DO have still needs to render as a valid DAG node — so git fakes it as parentless, even though it isn't really the repo's root. This video shows that fake boundary commit live in visigit, opens the raw .git/shallow file that makes it possible, and watches the graph grow backward the instant you run git fetch --unshallow.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: "clone a huge repo and get its history WITHOUT downloading years of commits" |
| 1:00 | `git clone --depth 1 <path>` — the clone finishes almost instantly regardless of repo size |
| 1:45 | `git log` in the shallow clone — history just... stops after 1 commit |
| 2:30 | Open it in visigit: the oldest visible commit renders normally, but it has NO parent edge, even though the original repo had a long history before it |
| 3:30 | That's the boundary commit: git records it in `.git/shallow` and treats it as parentless locally; the parent SHAs genuinely aren't in `.git/objects` |
| 4:15 | The tool has to cope with this gracefully: a commit whose recorded parent SHA can't be resolved locally is truncated at that boundary instead of erroring |
| 5:00 | `cat .git/shallow` — the raw file listing boundary commit SHAs |
| 5:45 | Try `git log --all` on other branches — same truncation everywhere |
| 6:30 | `git fetch --unshallow` — full history streams in |
| 7:15 | visigit re-rendered: the old parent edge appears retroactively; the graph "grows backward" past the old boundary |
| 8:00 | `git clone --depth 5` variant — boundary sits 5 commits back instead of 1 |
| 8:45 | Why this matters: CI checkouts, huge monorepos, and `--filter=blob:none` partial clones (full treatment in EP39) all rely on similar truncation tricks |
| 9:30 | Recap: shallow history isn't a lie about the commits you have, it's an honest gap where parent objects were never downloaded |

#### Key Visual Moments
- The oldest commit in a shallow clone rendering with zero parent edges, identical in shape to a true first commit or an orphan-branch commit (EP10) despite NOT actually being the repo's root
- The graph visibly "growing backward" the instant `git fetch --unshallow` completes, with a new parent edge attaching to a commit that already existed on screen
- `.git/shallow`'s boundary SHA matching exactly the parentless node in the diagram

---

[Curriculum index](README.md) | [<- Advanced](03-advanced.md) | [Reference ->](05-reference.md)
