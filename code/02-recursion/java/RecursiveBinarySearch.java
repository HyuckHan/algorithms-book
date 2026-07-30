public final class RecursiveBinarySearch {
    // snippet:recursive-binary-search:start
    /** Recursive Binary Search. Base case: begin > end (empty interval, -1,
     * no further call). Recursive case: narrow to one inclusive half
     * [begin,mid-1] or [mid+1,end], progress measure end-begin strictly
     * decreasing. Max call-stack depth is Theta(log n). mid uses the
     * overflow-safe `begin + (end-begin)/2` form. */
    static int bsearch(int[] a, int x, int begin, int end) {
        if (begin > end) return -1;
        int mid = begin + (end - begin) / 2;
        if (a[mid] == x) return mid;
        if (x < a[mid]) return bsearch(a, x, begin, mid - 1);
        return bsearch(a, x, mid + 1, end);
    }
    // snippet:recursive-binary-search:end

    public static void main(String[] args) {
        int[] data = {2, 5, 8, 12, 16, 23, 38};
        int x = 16;
        System.out.println("input: " + toCsv(data));
        System.out.println("x: " + x);
        System.out.println("bsearch: " + bsearch(data, x, 0, data.length - 1));
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
