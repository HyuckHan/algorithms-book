import java.util.*;

// New: the pseudocode's simple "reverse-push" iterative variant (not the
// exact-simulation form only described in prose). No canonical source --
// this deliberately does NOT try to reproduce the exact recursive DFS
// discovery/finish order (see content: "일반 graph에서 visited-on-push 방식은
// exact recursive DFS tree와 finish behavior를 보장하지 않는다").
public final class DfsIterative {
    private DfsIterative() {}

    // snippet:dfs-iterative:start
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
    // snippet:dfs-iterative:end

    public static void main(String[] args) {
        Graph g = new Graph(8, false);
        int[][] edges = {{0,1},{0,2},{0,3},{1,4},{2,4},{2,5},{3,6},{4,7},{6,7}};
        for (int[] e : edges) g.addEdge(e[0], e[1], 1);
        System.out.println("iterative dfs visit order: " + Arrays.toString(dfsIterative(g, 0)));
    }
}
