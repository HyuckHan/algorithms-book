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
