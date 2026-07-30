"""Same Dijkstra, Bellman-Ford, and path reconstruction as
ShortestPaths.java/shortest_paths.c -- newly written in Python, no canonical
source exists."""
import heapq

from graph import Graph

INF = float("inf")


# snippet:dijkstra:start
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
# snippet:dijkstra:end


# snippet:bellman-ford:start
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
# snippet:bellman-ford:end


# snippet:reconstruct-path:start
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
# snippet:reconstruct-path:end


if __name__ == "__main__":
    sname = "SABCDE"
    g = Graph(6, True)
    for u, v, w in [(0,1,4),(0,2,2),(2,1,1),(1,3,5),(2,3,8),
                    (2,4,10),(3,4,2),(3,5,6),(4,5,3)]:
        g.add_edge(u, v, w)
    dist, parent = dijkstra(g, 0)
    print("dijkstra dist:", [int(x) for x in dist])
    path = reconstruct_path(parent, dist, 5)
    print("dijkstra path to E:", " -> ".join(sname[v] for v in path))

    bfname = "sabcd"
    bf = Graph(5, True)
    for u, v, w in [(3,4,2),(1,3,-2),(2,3,3),(0,1,4),(0,2,5),(2,4,6)]:
        bf.add_edge(u, v, w)
    bdist, bparent, _ = bellman_ford(bf, 0)
    print("bellman-ford dist:", [int(x) for x in bdist])
    bpath = reconstruct_path(bparent, bdist, 4)
    print("bellman-ford path to d:", " -> ".join(bfname[v] for v in bpath))

    neg = Graph(3, True)
    neg.add_edge(0, 1, 1); neg.add_edge(1, 2, -2); neg.add_edge(2, 1, -2)
    _, _, negative_cycle = bellman_ford(neg, 0)
    print("reachable negative cycle detected:", "true" if negative_cycle else "false")
