public final class BinarySearch {
    // snippet:binary-search:start
    /** Binary Search. Lecture pseudocode is 1-based (low=1, high=n); this
     * array is 0-based, so low starts at 0 and high starts at n-1. mid =
     * low + (high-low)/2 matches the pseudocode exactly (already
     * overflow-safe). NOT_FOUND is represented as -1. */
    static int binarySearch(int[] a, int x) {
        int low = 0, high = a.length - 1;
        while (low <= high) {
            int mid = low + (high - low) / 2;
            if (a[mid] == x) return mid;
            else if (a[mid] < x) low = mid + 1;
            else high = mid - 1;
        }
        return -1;
    }
    // snippet:binary-search:end

    public static void main(String[] args) {
        int[] data = {3, 6, 9, 12, 15, 18, 21, 24};
        int x = 18;
        System.out.println("input: " + toCsv(data));
        System.out.println("x: " + x);
        System.out.println("binary: " + binarySearch(data, x));
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
