"""Same DAGShortestPaths as DagShortestPaths.java/dag_shortest_paths.c --
newly written in Python, no canonical source exists."""
from graph import Graph
from shortest_paths import INF, reconstruct_path
from topological_sort import kahn


# snippet:dag-shortest-paths:start
def dag_shortest_paths(g, s):
    order = kahn(g)
    if order is None:
        raise ValueError("not a DAG")
    n = g.vertices()
    dist = [INF] * n
    parent = [-1] * n
    dist[s] = 0
    for u in order:
        if dist[u] == INF:
            continue
        for v, w in g.edges_from(u):
            cand = dist[u] + w
            if cand < dist[v]:
                dist[v] = cand
                parent[v] = u
    return dist, parent
# snippet:dag-shortest-paths:end


if __name__ == "__main__":
    name = "sabc"
    g = Graph(4, True)
    for u, v, w in [(0,1,3),(0,2,2),(1,3,-4),(2,3,1)]:
        g.add_edge(u, v, w)
    dist, parent = dag_shortest_paths(g, 0)
    print("dist:", [int(x) for x in dist])
    path = reconstruct_path(parent, dist, 3)
    print("path to c:", " -> ".join(name[v] for v in path))
