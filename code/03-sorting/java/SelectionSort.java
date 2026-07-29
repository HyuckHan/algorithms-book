public final class SelectionSort {
    // snippet:selection-sort:start
    /** Selection Sort (1.3.1). Lecture pseudocode is 1-based; this array is
     * 0-based, so {@code last} here is one less than the lecture's
     * {@code last}, and the scan for the max runs over indices 1..last
     * inclusive either way. */
    static void selectionSort(int[] a) {
        for (int last = a.length - 1; last > 0; last--) {
            int m = 0;
            for (int i = 1; i <= last; i++) {
                if (a[i] > a[m]) m = i;
            }
            int tmp = a[m];
            a[m] = a[last];
            a[last] = tmp;
        }
    }
    // snippet:selection-sort:end

    public static void main(String[] args) {
        int[] data = {29, 10, 14, 37, 13, 5, 21, 8};
        System.out.println("input: " + toCsv(data));
        selectionSort(data);
        System.out.println("selection: " + toCsv(data));
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
