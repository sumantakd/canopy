import argparse
from builder import build_tree
from traverse import compute_sizes, bfs_levels
from analysis import top_k_files
from storage import save_snapshot, last_snapshot

def main():
    p = argparse.ArgumentParser(description="Canopy — directory tree analyzer")
    p.add_argument("path")
    p.add_argument("--top", type=int, default=5, help="show top-N largest files")
    p.add_argument("--db", default="canopy.db", help="snapshot database path")
    args = p.parse_args()

    tree = build_tree(args.path)
    compute_sizes(tree)

    print(f"{tree.name}: {tree.size / 1024:.1f} KB")
    print(f"Top {args.top} largest files:")
    for size, name in top_k_files(tree, args.top):
        print(f"  {name}: {size/1024:.1f} KB")

    prev = last_snapshot(args.db, tree.path)
    if prev:
        delta = tree.size - prev[1]
        print(f"Change since last scan: {delta/1024:+.1f} KB")
    save_snapshot(args.db, tree)

if __name__ == "__main__":
    main()