import java.util.*;

// Reused verbatim from lecture-notes/code/lecture08/java/Graph.java. Shared
// by every algorithm demo in this chapter, so it carries no single snippet
// marker of its own -- each algorithm's snippet is the function that uses it.
public final class Graph {
    public record Edge(int to, long weight) {}
    private final List<List<Edge>> adj;
    private final boolean directed;

    public Graph(int vertices, boolean directed) {
        if (vertices < 0) throw new IllegalArgumentException("negative vertex count");
        this.directed = directed;
        adj = new ArrayList<>(vertices);
        for (int i = 0; i < vertices; i++) adj.add(new ArrayList<>());
    }

    public int vertices() { return adj.size(); }
    public boolean directed() { return directed; }
    public List<Edge> edgesFrom(int u) {
        check(u);
        return Collections.unmodifiableList(adj.get(u));
    }

    // Duplicate policy: update the existing directed arc's weight.
    public void addEdge(int u, int v, long weight) {
        check(u); check(v);
        putArc(u, v, weight);
        if (!directed && u != v) putArc(v, u, weight);
    }

    public Long weight(int u, int v) {
        check(u); check(v);
        for (Edge e : adj.get(u)) if (e.to() == v) return e.weight();
        return null;
    }

    public List<long[]> arcs() {
        List<long[]> out = new ArrayList<>();
        for (int u = 0; u < vertices(); u++)
            for (Edge e : adj.get(u)) out.add(new long[]{u, e.to(), e.weight()});
        return out;
    }

    public void validate() {
        for (int u = 0; u < vertices(); u++) {
            Set<Integer> seen = new HashSet<>();
            for (Edge e : adj.get(u)) {
                check(e.to());
                if (!seen.add(e.to())) throw new AssertionError("duplicate arc");
                if (!directed && !Objects.equals(weight(e.to(), u), e.weight()))
                    throw new AssertionError("missing reverse arc");
            }
        }
    }

    private void putArc(int u, int v, long w) {
        List<Edge> list = adj.get(u);
        for (int i = 0; i < list.size(); i++)
            if (list.get(i).to() == v) { list.set(i, new Edge(v, w)); return; }
        list.add(new Edge(v, w));
        list.sort(Comparator.comparingInt(Edge::to));
    }
    private void check(int v) {
        if (v < 0 || v >= vertices()) throw new IndexOutOfBoundsException("vertex " + v);
    }
}
