public final class NQueensDemo {
    public static void main(String[] args) {
        NQueensSolver solver = new NQueensSolver();
        System.out.println("N(4): " + solver.solve(4).solutions.size());
        System.out.println("N(8): " + solver.solve(8).solutions.size());
    }
}
