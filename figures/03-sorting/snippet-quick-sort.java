    /** Quick Sort with Lomuto partition (1.4.2). low/high are 0-based
     * inclusive bounds; the initial call is quickSort(a, 0, n-1) instead of
     * QuickSort(A,1,n), and every index in partition (pivot=a[high],
     * i=low-1, j from low to high-1) carries over unchanged since it's the
     * same generic-bounds recurrence, just starting from 0 instead of 1. */
    static int partition(int[] a, int low, int high) {
        int pivot = a[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (a[j] <= pivot) {
                i++;
                int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
            }
        }
        int tmp = a[i + 1]; a[i + 1] = a[high]; a[high] = tmp;
        return i + 1;
    }

    static void quickSort(int[] a, int low, int high) {
        if (low < high) {
            int p = partition(a, low, high);
            quickSort(a, low, p - 1);
            quickSort(a, p + 1, high);
        }
    }
