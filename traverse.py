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