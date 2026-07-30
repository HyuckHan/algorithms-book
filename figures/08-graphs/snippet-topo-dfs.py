def topo_dfs(g):
    n = g.vertices()
    color = [0] * n
    finish = []

    def visit(u):
        color[u] = 1
        for v, _ in g.edges_from(u):
            if color[v] == 1:
                return False
            if color[v] == 0 and not visit(v):
                return False
        color[u] = 2
        finish.append(u)
        return True

    for u in range(n):
        if color[u] == 0 and not visit(u):
            return None
    finish.reverse()
    return finish
