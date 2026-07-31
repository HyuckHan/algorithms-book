public final class GraphColoringDemo {
    public static void main(String[] args) {
        // A-B-C-D-A cycle plus A-C diagonal, matching the lecture's own example.
        int[][] adjacency = {
            {0, 1, 1, 1},
            {1, 0, 1, 0},
            {1, 1, 0, 1},
            {1, 0, 1, 0},
        };
        GraphColoringSolver solver = new GraphColoringSolver();
        int[] colors = solver.color(adjacency, 3);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < colors.length; i++) { if (i > 0) sb.append(','); sb.append(colors[i]); }
        System.out.println("colors: " + sb);
    }
}
