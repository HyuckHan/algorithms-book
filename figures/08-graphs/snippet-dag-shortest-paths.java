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
