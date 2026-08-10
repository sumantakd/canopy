# canopy

A command-line tool that scans a directory, builds a tree representing its
structure, and analyzes it — folder sizes, largest files, and growth over
time between scans.

Built to explore tree traversal (DFS and BFS), and to practice turning a
data-structures concept into something that behaves like real software:
persistence, tests, and a usable interface, not just an algorithm demo.

## Run it

```bash
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt  # if you add one; currently stdlib only
python main.py ~/Downloads --top 10
```

Run pytest to verify correctness:
```bash
pytest -v
```

## What it does

- Recursively scans a folder and builds a tree (`Node`: name, path,
  is_folder, size, children)
- Computes each folder's total size bottom-up (post-order DFS)
- Provides the same size computation as an iterative version using an
  explicit stack, to avoid Python's recursion depth limit on very deep
  trees
- Produces a level-by-level (BFS) view of the tree
- Finds the top-N largest files using a min-heap, without sorting the
  entire file list
- Stores a snapshot of each scan in SQLite, so a second run on the same
  folder reports the size change since last time

## Project structure

```
node.py           Node class — the tree's building block
builder.py        Walks a real folder and builds the Node tree
traverse.py       compute_sizes (recursive DFS), compute_sizes_iterative
                   (stack-based DFS), bfs_levels (queue-based BFS)
analysis.py       top_k_files — heap-based top-N largest files
storage.py        SQLite snapshot save/read, used for size-change tracking
test_traverse.py  pytest tests verifying DFS/BFS correctness on a known tree
main.py           CLI entry point tying everything together
```

## Design decisions

**Why DFS for size computation:** a folder's size can't be known until
every child's size is known, so post-order DFS (children resolved before
the parent) is the natural fit.

**Why an iterative DFS as well as recursive:** recursive DFS relies on
Python's call stack, which has a depth limit — a sufficiently deep folder
tree would crash it. The iterative version uses an explicit stack instead,
so it has no such limit.

**Why BFS for the level view:** BFS naturally produces a shallow-to-deep
ordering, which matches how a user actually wants to browse an unfamiliar,
possibly huge folder tree — top-level structure first, details on demand.

**Why a heap for top-K files:** sorting every file to get the top 5 is
wasteful once a folder has thousands of files. A size-bounded min-heap
finds the top-K in O(n log k) instead of O(n log n).

**Why SQLite for snapshots:** a single scan alone doesn't answer "is this
folder growing?" — that requires state across runs. SQLite needs no server
and ships with Python, which fits a small CLI tool.

## Complexity

- DFS (recursive and iterative): O(n) time, where n is the number of files
  and folders. O(h) additional space for the recursive version's call
  stack, where h is the tree's height.
- BFS: O(n) time, O(w) space, where w is the tree's maximum width (the
  queue can hold at most one full level at a time).
- top_k_files: O(n log k) time using a size-k min-heap, versus O(n log n)
  for a full sort.

## What I'd add next

- A basic web UI on top of the same core logic (the CLI output maps
  directly to what a frontend would render)
- Duplicate file detection via content hashing
- Symlink cycle detection (currently symlinked directories are skipped
  entirely rather than followed, to avoid infinite loops)
