def bfs(g, s):
    n = g.vertices()
    color = [0] * n
    dist = [-1] * n
    parent = [-1] * n
    order = []
    color[s] = 1
    dist[s] = 0
    q = deque([s])
    while q:
        u = q.popleft()
        order.append(u)
        for v, _ in g.edges_from(u):
            if color[v] == 0:
                color[v] = 1
                dist[v] = dist[u] + 1
                parent[v] = u
                q.append(v)
        color[u] = 2
    return order, dist, parent
