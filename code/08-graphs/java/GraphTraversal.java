import java.util.*;

public final class GraphTraversal {
    public record BFSResult(int[] order, int[] dist, int[] parent) {}
    public record DFSResult(int[] discoveryOrder, int[] discover, int[] finish,
                            int[] parent) {}

    // Reused verbatim from lecture-notes/code/lecture08/java/GraphTraversal.java.
    // snippet:bfs:start
    public static BFSResult bfs(Graph g, int s) {
        int n = g.vertices(), count = 0;
        int[] color = new int[n], dist = new int[n], parent = new int[n], order = new int[n];
        Arrays.fill(dist, -1); Arrays.fill(parent, -1);
        ArrayDeque<Integer> q = new ArrayDeque<>();
        color[s] = 1; dist[s] = 0; q.add(s); // discovered on enqueue
        while (!q.isEmpty()) {
            int u = q.remove();
            order[count++] = u;
            for (Graph.Edge e : g.edgesFrom(u)) if (color[e.to()] == 0) {
                int v = e.to();
                color[v] = 1; dist[v] = dist[u] + 1; parent[v] = u; q.add(v);
            }
            color[u] = 2;
        }
        return new BFSResult(Arrays.copyOf(order, count), dist, parent);
    }
    // snippet:bfs:end

    // snippet:dfs:start
    public static DFSResult dfs(Graph g) {
        int n = g.vertices();
        int[] color = new int[n], d = new int[n], f = new int[n], p = new int[n];
        Arrays.fill(p, -1);
        List<Integer> order = new ArrayList<>();
        int[] time = {0};
        for (int u = 0; u < n; u++) if (color[u] == 0) visit(g, u, color, d, f, p, time, order);
        return new DFSResult(order.stream().mapToInt(Integer::intValue).toArray(), d, f, p);
    }

    private static void visit(Graph g, int u, int[] color, int[] d, int[] f,
                              int[] p, int[] time, List<Integer> order) {
        color[u] = 1; d[u] = ++time[0]; order.add(u);
        for (Graph.Edge e : g.edgesFrom(u)) if (color[e.to()] == 0) {
            p[e.to()] = u; visit(g, e.to(), color, d, f, p, time, order);
        }
        color[u] = 2; f[u] = ++time[0];
    }
    // snippet:dfs:end

    private GraphTraversal() {}

    public static void main(String[] args) {
        Graph g = new Graph(8, false);
        int[][] edges = {{0,1},{0,2},{0,3},{1,4},{2,4},{2,5},{3,6},{4,7},{6,7}};
        for (int[] e : edges) g.addEdge(e[0], e[1], 1);

        BFSResult b = bfs(g, 0);
        System.out.println("bfs order: " + Arrays.toString(b.order()));
        System.out.println("bfs dist: " + Arrays.toString(b.dist()));
        System.out.println("bfs parent: " + Arrays.toString(b.parent()));

        DFSResult d = dfs(g);
        System.out.println("dfs discover: " + Arrays.toString(d.discover()));
        System.out.println("dfs finish: " + Arrays.toString(d.finish()));
        System.out.println("dfs parent: " + Arrays.toString(d.parent()));
    }
}
