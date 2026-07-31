public final class KnapsackDemo {
    public static void main(String[] args) {
        KnapsackBranchAndBound.Item[] items = {
            new KnapsackBranchAndBound.Item("A", 2, 40),
            new KnapsackBranchAndBound.Item("B", 5, 30),
            new KnapsackBranchAndBound.Item("C", 10, 50),
            new KnapsackBranchAndBound.Item("D", 5, 10),
        };
        KnapsackBranchAndBound.Result result = new KnapsackBranchAndBound().solve(items, 16);
        System.out.println("profit: " + result.profit);
        System.out.println("weight: " + result.weight);
    }
}
