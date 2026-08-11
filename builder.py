import os
from node import Node


def build_tree(path):
    name = os.path.basename(path) or path
    node = Node(name, path, is_folder=True)
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    node.children.append(build_tree(entry.path))
                else:
                    try:
                        size = entry.stat().st_size
                    except OSError:
                        size = 0
                    node.children.append(Node(entry.name, entry.path, False, size))
    except PermissionError:
        pass  # skip folders you can't read; don't crash
    return node


def count_nodes(node):
    if not node.is_folder:
        return 1
    return 1 + sum(count_nodes(c) for c in node.children)
