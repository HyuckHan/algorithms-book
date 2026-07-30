import java.util.*;

public final class MinimumSpanningTree {
    public record MstEdge(int u, int v, long weight) {}
    public record Result(List<MstEdge> edges, long weight, boolean connected) {}

    // Reused verbatim from lecture-notes/code/lecture08/java/MinimumSpanningTree.java.
    // snippet:prim:start
    public static Result prim(Graph g, int root) {
        requireUndirected(g);
        int n = g.vertices();
        long[] key = new long[n]; int[] parent = new int[n]; boolean[] in = new boolean[n];
        Arrays.fill(key, Long.MAX_VALUE); Arrays.fill(parent, -1); key[root] = 0;
        PriorityQueue<long[]> pq = new PriorityQueue<>(
            Comparator.<long[]>comparingLong(x -> x[0]).thenComparingLong(x -> x[1]));
        pq.add(new long[]{0, root});
        List<MstEdge> out = new ArrayList<>(); long total = 0;
        while (!pq.isEmpty()) {
            long[] item = pq.remove(); int u = (int)item[1];
            if (in[u] || item[0] != key[u]) continue;
            in[u] = true;
            if (parent[u] >= 0) { out.add(new MstEdge(parent[u], u, key[u])); total += key[u]; }
            for (Graph.Edge e : g.edgesFrom(u)) if (!in[e.to()] &&
                    (e.weight() < key[e.to()] ||
                     e.weight() == key[e.to()] && u < parent[e.to()])) {
                key[e.to()] = e.weight(); parent[e.to()] = u;
                pq.add(new long[]{key[e.to()], e.to()});
            }
        }
        return new Result(List.copyOf(out), total, out.size() == Math.max(0, n - 1));
    }
    // snippet:prim:end

    // snippet:kruskal:start
    public static Result kruskal(Graph g) {
        requireUndirected(g);
        List<MstEdge> edges = new ArrayList<>();
        for (int u = 0; u < g.vertices(); u++)
            for (Graph.Edge e : g.edgesFrom(u)) if (u < e.to())
                edges.add(new MstEdge(u, e.to(), e.weight()));
        edges.sort(Comparator.comparingLong(MstEdge::weight)
            .thenComparingInt(MstEdge::u).thenComparingInt(MstEdge::v));
        DisjointSet dsu = new DisjointSet(g.vertices());
        List<MstEdge> out = new ArrayList<>(); long total = 0;
        for (MstEdge e : edges) if (dsu.union(e.u(), e.v())) {
            out.add(e); total += e.weight();
            if (out.size() == g.vertices() - 1) break;
        }
        return new Result(List.copyOf(out), total, out.size() == Math.max(0, g.vertices() - 1));
    }
    // snippet:kruskal:end

    public static void validate(Graph g, Result r) {
        DisjointSet d = new DisjointSet(g.vertices()); long sum = 0;
        for (MstEdge e : r.edges()) {
            if (!Objects.equals(g.weight(e.u(), e.v()), e.weight()) || !d.union(e.u(), e.v()))
                throw new AssertionError("invalid MST edge");
            sum += e.weight();
        }
        if (sum != r.weight() || r.connected() && r.edges().size() != g.vertices() - 1)
            throw new AssertionError("MST invariant");
    }
    private static void requireUndirected(Graph g) {
        if (g.directed()) throw new IllegalArgumentException("MST needs undirected graph");
    }
    private MinimumSpanningTree() {}

    private static final String[] NAME = {"A", "B", "C", "D", "E", "F", "G"};

    private static String edgesToString(List<MstEdge> edges) {
        StringBuilder sb = new StringBuilder();
        for (MstEdge e : edges) {
            if (sb.length() > 0) sb.append(" ");
            sb.append(NAME[e.u()]).append(NAME[e.v()]).append(e.weight());
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        Graph g = new Graph(7, false);
        long[][] e = {{0,1,8},{0,2,9},{0,3,11},{1,4,10},{2,3,13},
            {2,4,5},{2,5,12},{3,5,8},{3,6,8},{5,6,7}};
        for (long[] x : e) g.addEdge((int)x[0], (int)x[1], x[2]);

        Result p = prim(g, 0);
        validate(g, p);
        System.out.println("prim edges: " + edgesToString(p.edges()));
        System.out.println("prim weight: " + p.weight());

        Result k = kruskal(g);
        validate(g, k);
        System.out.println("kruskal edges: " + edgesToString(k.edges()));
        System.out.println("kruskal weight: " + k.weight());
    }
}
