"""Same adjacency-list design as Graph.java/graph.c (sorted-by-destination
adjacency for deterministic traversal order, duplicate edges update weight)
-- newly written in Python, no canonical source exists."""


class Graph:
    def __init__(self, vertices, directed):
        self.directed = directed
        self.adj = [[] for _ in range(vertices)]

    def vertices(self):
        return len(self.adj)

    def edges_from(self, u):
        return self.adj[u]

    def add_edge(self, u, v, weight):
        self._put_arc(u, v, weight)
        if not self.directed and u != v:
            self._put_arc(v, u, weight)

    def weight(self, u, v):
        for to, w in self.adj[u]:
            if to == v:
                return w
        return None

    def arcs(self):
        return [(u, to, w) for u in range(self.vertices()) for to, w in self.adj[u]]

    def _put_arc(self, u, v, w):
        row = self.adj[u]
        for i, (to, _) in enumerate(row):
            if to == v:
                row[i] = (v, w)
                return
        row.append((v, w))
        row.sort(key=lambda e: e[0])
