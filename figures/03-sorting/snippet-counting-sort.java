    /** Counting Sort (1.6.1). This procedure's pseudocode signature is
     * A[1..n]; rather than reinventing 0-based index arithmetic, this keeps
     * the working A/B arrays 1-based internally (index 0 unused) so the
     * prefix-sum C array and the place-then-decrement order match the
     * pseudocode exactly. */
    static int[] countingSort(int[] aZeroBased, int k) {
        int n = aZeroBased.length;
        int[] a = new int[n + 1];
        for (int j = 1; j <= n; j++) a[j] = aZeroBased[j - 1];

        int[] c = new int[k + 1];
        for (int j = 1; j <= n; j++) c[a[j]]++;
        for (int i = 1; i <= k; i++) c[i] += c[i - 1];

        int[] b = new int[n + 1];
        for (int j = n; j >= 1; j--) {
            b[c[a[j]]] = a[j];
            c[a[j]]--;
        }
        int[] bZeroBased = new int[n];
        for (int j = 1; j <= n; j++) bZeroBased[j - 1] = b[j];
        return bZeroBased;
    }
