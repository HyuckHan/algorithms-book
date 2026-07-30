def bellman_ford(g, s):
    n = g.vertices()
    dist = [INF] * n
    parent = [-1] * n
    dist[s] = 0
    arcs = g.arcs()
    for _ in range(1, n):
        changed = False
        for u, v, w in arcs:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                changed = True
        if not changed:
            break
    negative_cycle = any(
        dist[u] != INF and dist[u] + w < dist[v] for u, v, w in arcs
    )
    return dist, parent, negative_cycle
