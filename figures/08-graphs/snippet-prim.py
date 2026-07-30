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
