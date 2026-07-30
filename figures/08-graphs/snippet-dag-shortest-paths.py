def dag_shortest_paths(g, s):
    order = kahn(g)
    if order is None:
        raise ValueError("not a DAG")
    n = g.vertices()
    dist = [INF] * n
    parent = [-1] * n
    dist[s] = 0
    for u in order:
        if dist[u] == INF:
            continue
        for v, w in g.edges_from(u):
            cand = dist[u] + w
            if cand < dist[v]:
                dist[v] = cand
                parent[v] = u
    return dist, parent
