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
