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
