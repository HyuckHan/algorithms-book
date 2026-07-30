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
