// Driver for the "DSU Animation" toy example (A=0, B=1, C=2, D=3): matches
// the trace's exact edge order and accept/reject decisions.
public final class DisjointSetDemo {
    public static void main(String[] args) {
        DisjointSet d = new DisjointSet(4);
        String[] name = {"A", "B", "C", "D"};
        int[][] edges = {{0,1},{2,3},{1,2},{0,3}};
        for (int[] e : edges) {
            boolean accepted = d.union(e[0], e[1]);
            System.out.println(name[e[0]] + name[e[1]] + ": " + (accepted ? "accept" : "reject"));
        }
        StringBuilder components = new StringBuilder();
        for (int root = 0; root < 4; root++) {
            boolean any = false;
            for (int v = 0; v < 4; v++) if (d.find(v) == root) {
                if (!any) { components.append("{"); any = true; } else components.append(",");
                components.append(name[v]);
            }
            if (any) components.append("}");
        }
        System.out.println("components: " + components);
    }
}
