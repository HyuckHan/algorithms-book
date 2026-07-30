"""Same BFS/DFS as GraphTraversal.java/bfs_dfs.c -- newly written in Python,
no canonical source exists."""
from collections import deque

from graph import Graph


# snippet:bfs:start
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
# snippet:bfs:end


# snippet:dfs:start
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
# snippet:dfs:end


if __name__ == "__main__":
    g = Graph(8, False)
    for u, v in [(0,1),(0,2),(0,3),(1,4),(2,4),(2,5),(3,6),(4,7),(6,7)]:
        g.add_edge(u, v, 1)

    order, dist, parent = bfs(g, 0)
    print("bfs order:", order)
    print("bfs dist:", dist)
    print("bfs parent:", parent)

    discover, finish, dfs_parent = dfs(g)
    print("dfs discover:", discover)
    print("dfs finish:", finish)
    print("dfs parent:", dfs_parent)
