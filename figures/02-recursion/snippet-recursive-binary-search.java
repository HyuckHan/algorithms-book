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
