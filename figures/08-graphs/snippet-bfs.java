    public static BFSResult bfs(Graph g, int s) {
        int n = g.vertices(), count = 0;
        int[] color = new int[n], dist = new int[n], parent = new int[n], order = new int[n];
        Arrays.fill(dist, -1); Arrays.fill(parent, -1);
        ArrayDeque<Integer> q = new ArrayDeque<>();
        color[s] = 1; dist[s] = 0; q.add(s); // discovered on enqueue
        while (!q.isEmpty()) {
            int u = q.remove();
            order[count++] = u;
            for (Graph.Edge e : g.edgesFrom(u)) if (color[e.to()] == 0) {
                int v = e.to();
                color[v] = 1; dist[v] = dist[u] + 1; parent[v] = u; q.add(v);
            }
            color[u] = 2;
        }
        return new BFSResult(Arrays.copyOf(order, count), dist, parent);
    }
