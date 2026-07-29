    /** Bubble Sort (1.3.2). Lecture pseudocode is 1-based; this array is
     * 0-based. 1-based {@code last} runs n downto 2 with inner {@code i}
     * 1..last-1 comparing A[i],A[i+1]; here 0-based {@code last} runs n-1
     * downto 1 with inner {@code i} 0..last-1 comparing a[i],a[i+1]. */
    static void bubbleSort(int[] a) {
        for (int last = a.length - 1; last > 0; last--) {
            boolean swapped = false;
            for (int i = 0; i < last; i++) {
                if (a[i] > a[i + 1]) {
                    int tmp = a[i];
                    a[i] = a[i + 1];
                    a[i + 1] = tmp;
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }
