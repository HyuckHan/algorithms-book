public final class MergeSort {
    // snippet:merge-sort:start
    /** Merge Sort (1.4.1). low/high are 0-based inclusive bounds -- the
     * lecture pseudocode's low/high play the same role over 1-based bounds;
     * the initial call here is mergeSort(a, 0, n-1) instead of
     * MergeSort(A,1,n). mid uses the overflow-safe {@code low + (high-low)/2}
     * form from this section's "흔한 실수" callout, not (low+high)/2. */
    static void merge(int[] a, int low, int mid, int high) {
        int n1 = mid - low + 1;
        int n2 = high - mid;
        int[] L = new int[n1];
        int[] R = new int[n2];
        System.arraycopy(a, low, L, 0, n1);
        System.arraycopy(a, mid + 1, R, 0, n2);

        int i = 0, j = 0, k = low;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j]) a[k++] = L[i++];
            else              a[k++] = R[j++];
        }
        while (i < n1) a[k++] = L[i++];
        while (j < n2) a[k++] = R[j++];
    }

    static void mergeSort(int[] a, int low, int high) {
        if (low >= high) return;
        int mid = low + (high - low) / 2;
        mergeSort(a, low, mid);
        mergeSort(a, mid + 1, high);
        merge(a, low, mid, high);
    }
    // snippet:merge-sort:end

    public static void main(String[] args) {
        int[] data = {29, 10, 14, 37, 13, 5, 21, 8};
        System.out.println("input: " + toCsv(data));
        mergeSort(data, 0, data.length - 1);
        System.out.println("merge: " + toCsv(data));
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
