def dfs(g):
    n = g.vertices()
    color = [0] * n
    discover = [0] * n
    finish = [0] * n
    parent = [-1] * n
    time = [0]

    def visit(u):
        color[u] = 1
        time[0] += 1
        discover[u] = time[0]
        for v, _ in g.edges_from(u):
            if color[v] == 0:
                parent[v] = u
                visit(v)
        color[u] = 2
        time[0] += 1
        finish[u] = time[0]

    for u in range(n):
        if color[u] == 0:
            visit(u)
    return discover, finish, parent
