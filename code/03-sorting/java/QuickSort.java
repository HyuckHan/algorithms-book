public final class QuickSort {
    // snippet:quick-sort:start
    /** Quick Sort with Lomuto partition (1.4.2). low/high are 0-based
     * inclusive bounds; the initial call is quickSort(a, 0, n-1) instead of
     * QuickSort(A,1,n), and every index in partition (pivot=a[high],
     * i=low-1, j from low to high-1) carries over unchanged since it's the
     * same generic-bounds recurrence, just starting from 0 instead of 1. */
    static int partition(int[] a, int low, int high) {
        int pivot = a[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (a[j] <= pivot) {
                i++;
                int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
            }
        }
        int tmp = a[i + 1]; a[i + 1] = a[high]; a[high] = tmp;
        return i + 1;
    }

    static void quickSort(int[] a, int low, int high) {
        if (low < high) {
            int p = partition(a, low, high);
            quickSort(a, low, p - 1);
            quickSort(a, p + 1, high);
        }
    }
    // snippet:quick-sort:end

    public static void main(String[] args) {
        int[] data = {31, 8, 48, 73, 11, 3, 20, 29, 65, 15};
        System.out.println("input: " + toCsv(data));
        quickSort(data, 0, data.length - 1);
        System.out.println("quick: " + toCsv(data));
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
