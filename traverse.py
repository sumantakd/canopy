from collections import deque

def bfs_levels(root):
    """Returns a list of levels, each a list of Nodes at that depth."""
    levels = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node)
            if node.is_folder:
                queue.extend(node.children)
        levels.append(level)
    return levels


def compute_sizes(node):
    """Post-order DFS: children resolved before the parent. (Phase 3 — recursive)"""
    if not node.is_folder:
        return node.size
    total = 0
    for child in node.children:
        total += compute_sizes(child)
    node.size = total
    return total


def compute_sizes_iterative(root):
    """Iterative post-order DFS using an explicit stack. (Phase 4 — no recursion limit)"""
    stack = [(root, False)]
    while stack:
        node, processed = stack.pop()
        if node.is_folder and not processed:
            stack.append((node, True))
            for child in node.children:
                stack.append((child, False))
        elif node.is_folder:
            node.size = sum(c.size for c in node.children)
    return root.size