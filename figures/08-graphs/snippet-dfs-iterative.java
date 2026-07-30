    public static int[] dfsIterative(Graph g, int s) {
        int n = g.vertices();
        boolean[] discovered = new boolean[n];
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(s); discovered[s] = true;
        List<Integer> visitOrder = new ArrayList<>();
        while (!stack.isEmpty()) {
            int u = stack.pop();
            visitOrder.add(u);
            List<Graph.Edge> neighbors = g.edgesFrom(u);
            for (int i = neighbors.size() - 1; i >= 0; i--) {
                int v = neighbors.get(i).to();
                if (!discovered[v]) { discovered[v] = true; stack.push(v); }
            }
        }
        return visitOrder.stream().mapToInt(Integer::intValue).toArray();
    }
