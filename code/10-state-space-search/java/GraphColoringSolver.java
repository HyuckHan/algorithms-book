/** lecture-notes/code/lecture10/java/GraphColoringSolver.java와 같은 정책
 * (vertex 순서대로 color 1..m 시도, 이전 colored neighbor와만 비교). */
public final class GraphColoringSolver {
    // snippet:color-graph-coloring:start
    public int[] color(int[][] graph, int colorCount) {
        if (graph == null || colorCount < 0) throw new IllegalArgumentException();
        int n = graph.length;
        for (int[] row : graph) if (row == null || row.length != n) throw new IllegalArgumentException();
        int[] colors = new int[n];
        return dfs(graph, colorCount, 0, colors) ? colors : null;
    }

    private boolean dfs(int[][] g, int m, int v, int[] c) {
        if (v == g.length) return true;
        for (int color = 1; color <= m; color++) {
            if (safe(g, v, color, c)) {
                c[v] = color;
                if (dfs(g, m, v + 1, c)) return true;
                c[v] = 0;
            }
        }
        return false;
    }

    private boolean safe(int[][] g, int v, int color, int[] c) {
        for (int u = 0; u < v; u++) if (g[v][u] != 0 && c[u] == color) return false;
        return true;
    }
    // snippet:color-graph-coloring:end

    public static boolean valid(int[][] g, int[] c) {
        if (c == null || c.length != g.length) return false;
        for (int v = 0; v < g.length; v++)
            for (int u = v + 1; u < g.length; u++)
                if (g[v][u] != 0 && c[v] == c[u]) return false;
        return true;
    }
}
