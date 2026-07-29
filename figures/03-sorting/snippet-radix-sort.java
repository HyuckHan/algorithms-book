    /** LSD Radix Sort (1.6.2). No formal \Procedure pseudocode exists for
     * this section (prose-only in the lecture); this follows the described
     * ones -> tens -> hundreds passes, each a stable counting sort keyed on
     * one digit ({@code (a[i] / exp) % 10}). */
    static void countingSortByDigit(int[] a, int exp) {
        int n = a.length;
        int[] out = new int[n];
        int[] count = new int[10];
        for (int i = 0; i < n; i++) count[(a[i] / exp) % 10]++;
        for (int d = 1; d < 10; d++) count[d] += count[d - 1];
        for (int i = n - 1; i >= 0; i--) {
            int digit = (a[i] / exp) % 10;
            out[--count[digit]] = a[i];
        }
        System.arraycopy(out, 0, a, 0, n);
    }

    static void radixSort(int[] a) {
        int max = a[0];
        for (int x : a) if (x > max) max = x;
        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortByDigit(a, exp);
        }
    }
