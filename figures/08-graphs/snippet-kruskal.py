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
