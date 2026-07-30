def dfs_iterative(g, s):
    discovered = [False] * g.vertices()
    stack = [s]
    discovered[s] = True
    visit_order = []
    while stack:
        u = stack.pop()
        visit_order.append(u)
        for v, _ in reversed(g.edges_from(u)):
            if not discovered[v]:
                discovered[v] = True
                stack.append(v)
    return visit_order
