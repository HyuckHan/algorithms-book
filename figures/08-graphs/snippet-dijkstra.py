def dijkstra(g, s):
    for _, _, w in g.arcs():
        if w < 0:
            raise ValueError("negative edge")
    n = g.vertices()
    dist = [INF] * n
    parent = [-1] * n
    finalized = [False] * n
    dist[s] = 0
    pq = [(0, s)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u] or finalized[u]:
            continue
        finalized[u] = True
        for v, w in g.edges_from(u):
            if finalized[v]:
                continue
            cand = dist[u] + w
            if cand < dist[v]:
                dist[v] = cand
                parent[v] = u
                heapq.heappush(pq, (cand, v))
    return dist, parent
