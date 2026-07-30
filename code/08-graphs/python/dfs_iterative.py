"""Same "reverse-push" iterative DFS as DfsIterative.java/dfs_iterative.c --
newly written in Python, no canonical source exists."""
from graph import Graph


# snippet:dfs-iterative:start
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
# snippet:dfs-iterative:end


if __name__ == "__main__":
    g = Graph(8, False)
    for u, v in [(0,1),(0,2),(0,3),(1,4),(2,4),(2,5),(3,6),(4,7),(6,7)]:
        g.add_edge(u, v, 1)
    print("iterative dfs visit order:", dfs_iterative(g, 0))
