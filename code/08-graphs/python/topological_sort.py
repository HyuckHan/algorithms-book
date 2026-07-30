"""Same Kahn and DFS topological sort as TopologicalSort.java/
topological_sort.c -- newly written in Python, no canonical source exists."""
import heapq

from graph import Graph


# snippet:topo-kahn:start
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
# snippet:topo-kahn:end


# snippet:topo-dfs:start
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
# snippet:topo-dfs:end


if __name__ == "__main__":
    dag = Graph(6, True)
    for u, v in [(0,1),(0,3),(1,2),(1,4),(2,5),(3,5),(4,5)]:
        dag.add_edge(u, v, 1)
    print("kahn order:", kahn(dag))
    print("dfs-topo order:", topo_dfs(dag))

    cycle = Graph(3, True)
    cycle.add_edge(0, 1, 1); cycle.add_edge(1, 2, 1); cycle.add_edge(2, 0, 1)
    print("cycle graph kahn detects cycle:", "true" if kahn(cycle) is None else "false")
    print("cycle graph dfs-topo detects cycle:", "true" if topo_dfs(cycle) is None else "false")
