public final class PermutationDemo {
    public static void main(String[] args) {
        int perms = PermutationGenerator.generate(5, 4).size();
        int combos = PermutationGenerator.combinations(5, 4).size();
        System.out.println("P(5,4): " + perms);
        System.out.println("C(5,4): " + combos);
    }
}
