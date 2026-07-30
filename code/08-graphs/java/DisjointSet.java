// Reused verbatim from lecture-notes/code/lecture08/java/DisjointSet.java.
// snippet:disjoint-set:start
public final class DisjointSet {
    private final int[] parent, rank;
    public DisjointSet(int n) {
        if (n < 0) throw new IllegalArgumentException();
        parent = new int[n]; rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    public int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }
    public boolean union(int a, int b) {
        int x = find(a), y = find(b);
        if (x == y) return false;
        if (rank[x] < rank[y]) { int t = x; x = y; y = t; }
        parent[y] = x;
        if (rank[x] == rank[y]) rank[x]++;
        return true;
    }
}
// snippet:disjoint-set:end
