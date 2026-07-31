public final class ArithmeticProgressionDemo {
    public static void main(String[] args) {
        int[] input = {4, 1, 3, 5, 7};
        ArithmeticProgressionSearch.Result result =
            new ArithmeticProgressionSearch().solve(input, true);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < result.sequence.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(result.sequence[i]);
        }
        System.out.println("sequence: " + sb);
        System.out.println("length: " + result.sequence.length);
        System.out.println("valid: " + ArithmeticProgressionSearch.valid(result.sequence));
    }
}
