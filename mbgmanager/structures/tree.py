class TreeNode:
    def __init__(self, nama):
        self.nama = nama
        self.children = []

    def tambah_child(self, child):
        self.children.append(child)

    def to_lines(self, level=0, lines=None):
        if lines is None:
            lines = []
        lines.append("  " * level + "• " + self.nama)
        for c in self.children:
            c.to_lines(level + 1, lines)
        return lines


def hitung_node_tree(root):
    if root is None:
        return 0
    total = 1
    for c in root.children:
        total += hitung_node_tree(c)
    return total
