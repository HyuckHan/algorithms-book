def kahn(g):
    n = g.vertices()
    indegree = [0] * n
    for _, v, _ in g.arcs():
        indegree[v] += 1
    zero = [v for v in range(n) if indegree[v] == 0]
    heapq.heapify(zero)
    order = []
    while zero:
        u = heapq.heappop(zero)
        order.append(u)
        for v, _ in g.edges_from(u):
            indegree[v] -= 1
            if indegree[v] == 0:
                heapq.heappush(zero, v)
    return order if len(order) == n else None
