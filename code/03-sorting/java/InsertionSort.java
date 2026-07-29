public final class InsertionSort {
    // snippet:insertion-sort:start
    /** Insertion Sort (1.3.3). Lecture pseudocode is 1-based (i from 2 to n,
     * j from i-1 downto 1); this array is 0-based, so i runs 1..n-1 and j
     * runs i-1 downto 0. */
    static void insertionSort(int[] a) {
        for (int i = 1; i < a.length; i++) {
            int key = a[i];
            int j = i - 1;
            while (j >= 0 && a[j] > key) {
                a[j + 1] = a[j];
                j--;
            }
            a[j + 1] = key;
        }
    }
    // snippet:insertion-sort:end

    public static void main(String[] args) {
        int[] data = {29, 10, 14, 37, 13, 5, 21, 8};
        System.out.println("input: " + toCsv(data));
        insertionSort(data);
        System.out.println("insertion: " + toCsv(data));
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
