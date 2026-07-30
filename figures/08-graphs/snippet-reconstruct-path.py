def reconstruct_path(parent, dist, target):
    if dist[target] == INF:
        return []
    path = []
    seen = set()
    v = target
    while v != -1:
        if v in seen:
            raise ValueError("parent cycle")
        seen.add(v)
        path.append(v)
        v = parent[v]
    path.reverse()
    return path
