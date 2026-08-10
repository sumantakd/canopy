from node import Node
from traverse import compute_sizes, compute_sizes_iterative, bfs_levels

def make_test_tree():
    root = Node("root", "/root", True)
    a = Node("a.txt", "/root/a.txt", False, size=10)
    sub = Node("sub", "/root/sub", True)
    b = Node("b.txt", "/root/sub/b.txt", False, size=20)
    sub.children = [b]
    root.children = [a, sub]
    return root

def test_recursive_size():
    t = make_test_tree()
    assert compute_sizes(t) == 30

def test_iterative_matches_recursive():
    t1, t2 = make_test_tree(), make_test_tree()
    assert compute_sizes(t1) == compute_sizes_iterative(t2)

def test_bfs_level_order():
    t = make_test_tree()
    levels = bfs_levels(t)
    assert [n.name for n in levels[0]] == ["root"]
    assert set(n.name for n in levels[1]) == {"a.txt", "sub"}