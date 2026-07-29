public final class CountingSort {
    // snippet:counting-sort:start
    /** Counting Sort (1.6.1). This procedure's pseudocode signature is
     * A[1..n]; rather than reinventing 0-based index arithmetic, this keeps
     * the working A/B arrays 1-based internally (index 0 unused) so the
     * prefix-sum C array and the place-then-decrement order match the
     * pseudocode exactly. */
    static int[] countingSort(int[] aZeroBased, int k) {
        int n = aZeroBased.length;
        int[] a = new int[n + 1];
        for (int j = 1; j <= n; j++) a[j] = aZeroBased[j - 1];

        int[] c = new int[k + 1];
        for (int j = 1; j <= n; j++) c[a[j]]++;
        for (int i = 1; i <= k; i++) c[i] += c[i - 1];

        int[] b = new int[n + 1];
        for (int j = n; j >= 1; j--) {
            b[c[a[j]]] = a[j];
            c[a[j]]--;
        }
        int[] bZeroBased = new int[n];
        for (int j = 1; j <= n; j++) bZeroBased[j - 1] = b[j];
        return bZeroBased;
    }
    // snippet:counting-sort:end

    public static void main(String[] args) {
        int[] data = {4, 1, 3, 4, 3};
        int k = 4;
        System.out.println("input: " + toCsv(data));
        int[] out = countingSort(data, k);
        System.out.println("counting: " + toCsv(out));
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
