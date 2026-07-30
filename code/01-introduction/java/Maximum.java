public final class Maximum {
    // snippet:maximum:start
    /** Maximum. Lecture pseudocode is 1-based (v <- A[1], i from 2 to n);
     * this array is 0-based, so v starts at a[0] and i runs 1..n-1.
     * Precondition: n >= 1 (non-empty array). */
    static int maximum(int[] a) {
        int v = a[0];
        for (int i = 1; i < a.length; i++) {
            if (a[i] > v) v = a[i];
        }
        return v;
    }
    // snippet:maximum:end

    public static void main(String[] args) {
        int[] data = {7, 12, 3, 15, 8};
        System.out.println("input: " + toCsv(data));
        System.out.println("maximum: " + maximum(data));
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
