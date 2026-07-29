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
