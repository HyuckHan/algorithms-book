def color_graph(adjacency, m):
    n = len(adjacency)
    color = [0] * n

    def safe(v, c):
        return all(not (adjacency[v][u] and color[u] == c) for u in range(v))

    def recurse(v):
        if v == n:
            return True
        for c in range(1, m + 1):
            if safe(v, c):
                color[v] = c
                if recurse(v + 1):
                    return True
                color[v] = 0
        return False

    return list(color) if recurse(0) else None
