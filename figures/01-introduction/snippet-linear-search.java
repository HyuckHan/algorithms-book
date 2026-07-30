    /** Linear Search. Lecture pseudocode is 1-based (i from 1 to n); this
     * array is 0-based, so i runs 0..n-1. NOT_FOUND is represented as -1. */
    static int linearSearch(int[] a, int x) {
        for (int i = 0; i < a.length; i++) {
            if (a[i] == x) return i;
        }
        return -1;
    }
