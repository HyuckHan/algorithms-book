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
