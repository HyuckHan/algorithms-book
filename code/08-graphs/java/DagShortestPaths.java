import java.util.*;

// New: no canonical source (lecture-notes/code/lecture08/java/ShortestPaths.java
// only has Dijkstra/Bellman-Ford). Reuses TopologicalSort.kahn verbatim and
// adds the Relax loop the DAGShortestPaths pseudocode describes.
public final class DagShortestPaths {
    public record Result(long[] dist, int[] parent) {}
    private DagShortestPaths() {}

    // snippet:dag-shortest-paths:start
    public static Result dagShortestPaths(Graph g, int s) {
        int[] order = TopologicalSort.kahn(g).orElseThrow(() -> new IllegalArgumentException("not a DAG"));
        int n = g.vertices();
        long[] dist = new long[n]; int[] parent = new int[n];
        Arrays.fill(dist, ShortestPaths.INF); Arrays.fill(parent, -1); dist[s] = 0;
        for (int u : order) {
            if (dist[u] == ShortestPaths.INF) continue;
            for (Graph.Edge e : g.edgesFrom(u)) {
                long cand = dist[u] + e.weight();
                if (cand < dist[e.to()]) { dist[e.to()] = cand; parent[e.to()] = u; }
            }
        }
        return new Result(dist, parent);
    }
    // snippet:dag-shortest-paths:end

    public static void main(String[] args) {
        String[] name = {"s", "a", "b", "c"};
        Graph g = new Graph(4, true);
        long[][] e = {{0,1,3},{0,2,2},{1,3,-4},{2,3,1}};
        for (long[] x : e) g.addEdge((int)x[0], (int)x[1], x[2]);
        Result r = dagShortestPaths(g, 0);
        System.out.println("dist: " + Arrays.toString(r.dist()));
        int[] path = ShortestPaths.path(new ShortestPaths.Result(r.dist(), r.parent(), false), 3);
        StringBuilder sb = new StringBuilder();
        for (int v : path) { if (sb.length() > 0) sb.append(" -> "); sb.append(name[v]); }
        System.out.println("path to c: " + sb);
    }
}
