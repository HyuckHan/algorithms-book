import java.util.Arrays;

public final class SelectBySorting {
    // snippet:select-by-sorting:start
    static int selectBySorting(int[] a, int rank) {
        int[] copy = a.clone();
        Arrays.sort(copy);
        return copy[rank];
    }
    // snippet:select-by-sorting:end

    public static void main(String[] args) {
        int[] data = {31, 8, 48, 73, 11, 3, 20, 29, 65, 15};
        System.out.println("input: " + toCsv(data));
        for (int rank : new int[] {1, 6}) {
            System.out.println("rank: " + rank);
            System.out.println("result: " + selectBySorting(data, rank));
        }
    }

    private static String toCsv(int[] a) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(',');
            sb.append(a[i]);
        }
        return sb.toString();
    }
}
