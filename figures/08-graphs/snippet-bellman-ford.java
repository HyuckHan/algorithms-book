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
