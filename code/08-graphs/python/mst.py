"""Same Prim and Kruskal as MinimumSpanningTree.java/mst.c -- newly written
in Python, no canonical source exists."""
import heapq

from disjoint_set import DisjointSet
from graph import Graph


# snippet:prim:start
def prim(g, root):
    n = g.vertices()
    key = [float("inf")] * n
    parent = [-1] * n
    in_tree = [False] * n
    key[root] = 0
    pq = [(0, root)]
    edges = []
    total = 0
    while pq:
        k, u = heapq.heappop(pq)
        if in_tree[u] or k != key[u]:
            continue
        in_tree[u] = True
        if parent[u] >= 0:
            edges.append((parent[u], u, key[u]))
            total += key[u]
        for v, w in g.edges_from(u):
            if not in_tree[v] and (w < key[v] or (w == key[v] and u < parent[v])):
                key[v] = w
                parent[v] = u
                heapq.heappush(pq, (key[v], v))
    return edges, total
# snippet:prim:end


# snippet:kruskal:start
def kruskal(g):
    edges = sorted(
        ((u, v, w) for u in range(g.vertices()) for v, w in g.edges_from(u) if u < v),
        key=lambda e: (e[2], e[0], e[1]),
    )
    dsu = DisjointSet(g.vertices())
    selected = []
    total = 0
    for u, v, w in edges:
        if dsu.union(u, v):
            selected.append((u, v, w))
            total += w
            if len(selected) == g.vertices() - 1:
                break
    return selected, total
# snippet:kruskal:end


if __name__ == "__main__":
    g = Graph(7, False)
    for u, v, w in [(0,1,8),(0,2,9),(0,3,11),(1,4,10),(2,3,13),
                    (2,4,5),(2,5,12),(3,5,8),(3,6,8),(5,6,7)]:
        g.add_edge(u, v, w)

    name = "ABCDEFG"

    def render(edges):
        return " ".join(f"{name[u]}{name[v]}{w}" for u, v, w in edges)

    prim_edges, prim_weight = prim(g, 0)
    print("prim edges:", render(prim_edges))
    print("prim weight:", prim_weight)

    kruskal_edges, kruskal_weight = kruskal(g)
    print("kruskal edges:", render(kruskal_edges))
    print("kruskal weight:", kruskal_weight)
