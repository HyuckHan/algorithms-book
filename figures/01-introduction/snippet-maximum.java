    /** Maximum. Lecture pseudocode is 1-based (v <- A[1], i from 2 to n);
     * this array is 0-based, so v starts at a[0] and i runs 1..n-1.
     * Precondition: n >= 1 (non-empty array). */
    static int maximum(int[] a) {
        int v = a[0];
        for (int i = 1; i < a.length; i++) {
            if (a[i] > v) v = a[i];
        }
        return v;
    }
