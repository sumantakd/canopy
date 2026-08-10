class Node:
    def __init__(self, name, path, is_folder, size=0):
        self.name = name
        self.path = path
        self.is_folder = is_folder
        self.size = size          # bytes; filled in later for folders
        self.children = []        # list[Node], empty for files

    def __repr__(self):
        kind = "DIR" if self.is_folder else "FILE"
        return f"<{kind} {self.name} ({self.size}B)>"