import java.util.*;

public final class ShortestPaths {
    public static final long INF = Long.MAX_VALUE / 4;
    public record Result(long[] dist, int[] parent, boolean negativeCycle) {}

    // Reused verbatim from lecture-notes/code/lecture08/java/ShortestPaths.java.
    // snippet:dijkstra:start
    public static Result dijkstra(Graph g, int s) {
        for (long[] e : g.arcs()) if (e[2] < 0) throw new IllegalArgumentException("negative edge");
        int n = g.vertices(); long[] d = new long[n]; int[] p = new int[n];
        boolean[] finalized = new boolean[n];
        Arrays.fill(d, INF); Arrays.fill(p, -1); d[s] = 0;
        PriorityQueue<long[]> q = new PriorityQueue<>(
            Comparator.<long[]>comparingLong(x -> x[0]).thenComparingLong(x -> x[1]));
        q.add(new long[]{0, s});
        while (!q.isEmpty()) {
            long[] x = q.remove(); int u = (int)x[1];
            if (x[0] != d[u]) continue;
            if (finalized[u]) continue;
            finalized[u] = true;
            for (Graph.Edge e : g.edgesFrom(u)) {
                if (finalized[e.to()]) continue;
                long cand = safeAdd(d[u], e.weight());
                if (cand < d[e.to()]) {
                    d[e.to()] = cand; p[e.to()] = u; q.add(new long[]{cand, e.to()});
                }
            }
        }
        return new Result(d, p, false);
    }
    // snippet:dijkstra:end

    // snippet:bellman-ford:start
    public static Result bellmanFord(Graph g, int s) {
        int n = g.vertices(); long[] d = new long[n]; int[] p = new int[n];
        Arrays.fill(d, INF); Arrays.fill(p, -1); d[s] = 0;
        List<long[]> arcs = g.arcs();
        for (int i = 1; i < n; i++) {
            boolean changed = false;
            for (long[] e : arcs) if (d[(int)e[0]] != INF) {
                long cand = safeAdd(d[(int)e[0]], e[2]);
                if (cand < d[(int)e[1]]) {
                    d[(int)e[1]] = cand; p[(int)e[1]] = (int)e[0]; changed = true;
                }
            }
            if (!changed) break;
        }
        for (long[] e : arcs) if (d[(int)e[0]] != INF &&
                safeAdd(d[(int)e[0]], e[2]) < d[(int)e[1]])
            return new Result(d, p, true);
        return new Result(d, p, false);
    }
    // snippet:bellman-ford:end

    // snippet:reconstruct-path:start
    public static int[] path(Result r, int target) {
        if (r.dist()[target] == INF || r.negativeCycle()) return new int[0];
        List<Integer> rev = new ArrayList<>();
        boolean[] seen = new boolean[r.parent().length];
        for (int v = target; v >= 0; v = r.parent()[v]) {
            if (seen[v]) throw new IllegalStateException("parent cycle");
            seen[v] = true; rev.add(v);
        }
        Collections.reverse(rev);
        return rev.stream().mapToInt(Integer::intValue).toArray();
    }
    // snippet:reconstruct-path:end

    public static void validate(Graph g, int s, Result r) {
        if (!r.negativeCycle() && r.dist()[s] != 0) throw new AssertionError();
        if (!r.negativeCycle()) for (long[] e : g.arcs())
            if (r.dist()[(int)e[0]] != INF &&
                r.dist()[(int)e[1]] > safeAdd(r.dist()[(int)e[0]], e[2]))
                throw new AssertionError("triangle inequality");
    }

    private static long safeAdd(long a, long b) {
        if (a == INF) return INF;
        if (b > 0 && a > INF - b || b < 0 && a < -INF - b)
            throw new ArithmeticException("distance overflow");
        return a + b;
    }
    private ShortestPaths() {}

    public static void main(String[] args) {
        String[] name = {"S", "A", "B", "C", "D", "E"};
        Graph g = new Graph(6, true);
        long[][] e = {{0,1,4},{0,2,2},{2,1,1},{1,3,5},{2,3,8},
            {2,4,10},{3,4,2},{3,5,6},{4,5,3}};
        for (long[] x : e) g.addEdge((int)x[0], (int)x[1], x[2]);
        Result d = dijkstra(g, 0);
        validate(g, 0, d);
        System.out.println("dijkstra dist: " + Arrays.toString(d.dist()));
        StringBuilder sb = new StringBuilder();
        for (int v : path(d, 5)) { if (sb.length() > 0) sb.append(" -> "); sb.append(name[v]); }
        System.out.println("dijkstra path to E: " + sb);

        String[] bfName = {"s", "a", "b", "c", "d"};
        Graph bf = new Graph(5, true);
        long[][] be = {{3,4,2},{1,3,-2},{2,3,3},{0,1,4},{0,2,5},{2,4,6}};
        for (long[] x : be) bf.addEdge((int)x[0], (int)x[1], x[2]);
        Result br = bellmanFord(bf, 0);
        System.out.println("bellman-ford dist: " + Arrays.toString(br.dist()));
        StringBuilder sb2 = new StringBuilder();
        for (int v : path(br, 4)) { if (sb2.length() > 0) sb2.append(" -> "); sb2.append(bfName[v]); }
        System.out.println("bellman-ford path to d: " + sb2);

        Graph neg = new Graph(3, true);
        neg.addEdge(0,1,1); neg.addEdge(1,2,-2); neg.addEdge(2,1,-2);
        System.out.println("reachable negative cycle detected: " + bellmanFord(neg, 0).negativeCycle());
    }
}
