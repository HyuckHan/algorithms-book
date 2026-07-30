public final class LinearSearch {
    // snippet:linear-search:start
    /** Linear Search. Lecture pseudocode is 1-based (i from 1 to n); this
     * array is 0-based, so i runs 0..n-1. NOT_FOUND is represented as -1. */
    static int linearSearch(int[] a, int x) {
        for (int i = 0; i < a.length; i++) {
            if (a[i] == x) return i;
        }
        return -1;
    }
    // snippet:linear-search:end

    public static void main(String[] args) {
        int[] data = {3, 6, 9, 12, 15, 18, 21, 24};
        int x = 12;
        System.out.println("input: " + toCsv(data));
        System.out.println("x: " + x);
        System.out.println("linear: " + linearSearch(data, x));
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
