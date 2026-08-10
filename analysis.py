import heapq

def top_k_files(root, k=5):
    heap = []  # min-heap of (size, path)
    def walk(node):
        if node.is_folder:
            for c in node.children:
                walk(c)
        else:
            if len(heap) < k:
                heapq.heappush(heap, (node.size, node.name))
            elif node.size > heap[0][0]:
                heapq.heapreplace(heap, (node.size, node.name))
    walk(root)
    return sorted(heap, reverse=True)