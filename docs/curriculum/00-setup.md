[Curriculum index](README.md) | [Beginner ->](01-beginner.md)

---

## Tier 0 — Setup

---

### EP 01 — Setup — See Your Git: Setting Up a Live Repository Visualizer

**visigit mode:** demo of all three
**Target length:** 5–8 min
**Commands covered:** git init, pip install

#### Why This Matters

Most git tutorials describe commands in words; this series shows you the actual data structure git is manipulating underneath every command — a DAG of commit objects plus a handful of pointers. Setting up a live-updating diagram alongside your terminal is the foundation the whole series relies on: once you can see the graph change in real time, every later episode becomes a direct observation instead of an act of faith in what the manual says.

#### YouTube Title
> See Your Git: Live Repository Diagrams That Update as You Type Commands

#### YouTube Description
> Stop guessing what git commands do — watch them happen. This video sets up visigit, a free tool that turns any git repository into a live diagram. Every command you run updates the graph in real time. Install it in under five minutes and you'll never memorize git blindly again.

#### Outline
| Time | Section |
|------|---------|
| 0:00 | Hook: show monitor mode updating live as git commands run |
| 0:45 | What visigit is and why it exists |
| 1:30 | Prerequisites: git (2.28+ required for `git init -b`; record on the latest stable git and state the version on-screen), Python 3.9+, graphviz (`apt install graphviz`) |
| 2:30 | Install visigit (`pip install -e .` or from source) |
| 3:30 | Quick demo: `visigit` on an existing repo — three modes at a glance |
| 4:30 | Set up the two-terminal workflow: visigit in Terminal A, git in Terminal B |
| 5:30 | Teaser of what's coming in the series |

#### Key Visual Moments
- Normal mode: collapse of boring commit chains into summary nodes
- Branch mode: topology graph — branches as nodes, fork points visible
- Verbose mode: trees and blobs appearing under each commit
- New nodes highlighted in gold on every monitor update

---

[Curriculum index](README.md) | [Beginner ->](01-beginner.md)
