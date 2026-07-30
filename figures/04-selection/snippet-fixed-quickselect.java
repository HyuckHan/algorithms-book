    /** 정렬 장의 QuickSort.java partition과 동일한 Lomuto partition(pivot=a[high]). */
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

    static int fixedQuickselect(int[] a, int rank) {
        int low = 0, high = a.length - 1;
        while (low < high) {
            int q = partition(a, low, high);
            if (rank == q) return a[q];
            if (rank < q) high = q - 1;
            else low = q + 1;
        }
        return a[low];
    }
