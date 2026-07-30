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
