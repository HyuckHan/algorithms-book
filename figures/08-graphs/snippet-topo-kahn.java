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
