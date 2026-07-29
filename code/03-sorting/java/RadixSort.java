public final class RadixSort {
    // snippet:radix-sort:start
    /** LSD Radix Sort (1.6.2). No formal \Procedure pseudocode exists for
     * this section (prose-only in the lecture); this follows the described
     * ones -> tens -> hundreds passes, each a stable counting sort keyed on
     * one digit ({@code (a[i] / exp) % 10}). */
    static void countingSortByDigit(int[] a, int exp) {
        int n = a.length;
        int[] out = new int[n];
        int[] count = new int[10];
        for (int i = 0; i < n; i++) count[(a[i] / exp) % 10]++;
        for (int d = 1; d < 10; d++) count[d] += count[d - 1];
        for (int i = n - 1; i >= 0; i--) {
            int digit = (a[i] / exp) % 10;
            out[--count[digit]] = a[i];
        }
        System.arraycopy(out, 0, a, 0, n);
    }

    static void radixSort(int[] a) {
        int max = a[0];
        for (int x : a) if (x > max) max = x;
        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortByDigit(a, exp);
        }
    }
    // snippet:radix-sort:end

    public static void main(String[] args) {
        int[] data = {170, 90, 802, 2, 24, 45, 75, 66};
        System.out.println("input: " + toCsv(data));
        radixSort(data);
        System.out.println("radix: " + toCsv(data));
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
