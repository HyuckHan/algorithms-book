public final class SubsetSumDemo {
    public static void main(String[] args) {
        SubsetSumSolver solver = new SubsetSumSolver();
        int[] weights = {3, 4, 5, 6};
        SubsetSumSolver.Result result = solver.solve(weights, 9, true);
        System.out.println("solutions: " + result.indexSolutions.size());
    }
}
