class Graph:
    def __init__(self):
        self.adj = {}

    def tambah_node(self, nama):
        if nama not in self.adj:
            self.adj[nama] = []

    def tambah_edge(self, a, b):
        self.tambah_node(a)
        self.tambah_node(b)
        if b not in self.adj[a]:
            self.adj[a].append(b)
        if a not in self.adj[b]:
            self.adj[b].append(a)

    def tampilkan_str(self):
        return "\n".join(
            f"{k} → {', '.join(v)}" for k, v in self.adj.items()
        )

    def bfs_str(self, start):
        if start not in self.adj:
            return "Node awal tidak ada di graph."
        visited = {start}
        queue = [start]
        urutan = []
        while queue:
            cur = queue.pop(0)
            urutan.append(cur)
            for n in self.adj[cur]:
                if n not in visited:
                    visited.add(n)
                    queue.append(n)
        return "Urutan BFS: " + " → ".join(urutan)
