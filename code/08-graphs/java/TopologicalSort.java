import java.util.*;

public final class TopologicalSort {
    // Reused verbatim from lecture-notes/code/lecture08/java/TopologicalSort.java.
    // Min-heap Kahn: O(V + E + V log V) = O(E + V log V).
    // Replacing the heap with a queue or stack gives Theta(V + E).
    // snippet:topo-kahn:start
    public static Optional<int[]> kahn(Graph g) {
        int n = g.vertices(), used = 0;
        int[] indegree = new int[n], out = new int[n];
        for (long[] e : g.arcs()) indegree[(int)e[1]]++;
        PriorityQueue<Integer> zero = new PriorityQueue<>();
        for (int v = 0; v < n; v++) if (indegree[v] == 0) zero.add(v);
        while (!zero.isEmpty()) {
            int u = zero.remove(); out[used++] = u;
            for (Graph.Edge e : g.edgesFrom(u)) if (--indegree[e.to()] == 0) zero.add(e.to());
        }
        return used == n ? Optional.of(out) : Optional.empty();
    }
    // snippet:topo-kahn:end

    // snippet:topo-dfs:start
    public static Optional<int[]> dfs(Graph g) {
        int[] color = new int[g.vertices()];
        List<Integer> finish = new ArrayList<>();
        for (int u = 0; u < g.vertices(); u++)
            if (color[u] == 0 && !visit(g, u, color, finish)) return Optional.empty();
        Collections.reverse(finish);
        return Optional.of(finish.stream().mapToInt(Integer::intValue).toArray());
    }

    private static boolean visit(Graph g, int u, int[] color, List<Integer> finish) {
        color[u] = 1;
        for (Graph.Edge e : g.edgesFrom(u)) {
            int v = e.to();
            if (color[v] == 1 || color[v] == 0 && !visit(g, v, color, finish)) return false;
        }
        color[u] = 2; finish.add(u); return true;
    }
    // snippet:topo-dfs:end

    public static void validate(Graph g, int[] order) {
        if (order.length != g.vertices()) throw new AssertionError("partial order");
        int[] pos = new int[order.length];
        for (int i = 0; i < order.length; i++) pos[order[i]] = i;
        for (long[] e : g.arcs()) if (pos[(int)e[0]] >= pos[(int)e[1]])
            throw new AssertionError("invalid topological order");
    }
    private TopologicalSort() {}

    public static void main(String[] args) {
        Graph dag = new Graph(6, true);
        int[][] e = {{0,1},{0,3},{1,2},{1,4},{2,5},{3,5},{4,5}};
        for (int[] x : e) dag.addEdge(x[0], x[1], 1);

        int[] k = kahn(dag).orElseThrow();
        validate(dag, k);
        System.out.println("kahn order: " + Arrays.toString(k));

        int[] d = dfs(dag).orElseThrow();
        validate(dag, d);
        System.out.println("dfs-topo order: " + Arrays.toString(d));

        Graph cycle = new Graph(3, true);
        cycle.addEdge(0,1,1); cycle.addEdge(1,2,1); cycle.addEdge(2,0,1);
        System.out.println("cycle graph kahn detects cycle: " + kahn(cycle).isEmpty());
        System.out.println("cycle graph dfs-topo detects cycle: " + dfs(cycle).isEmpty());
    }
}
