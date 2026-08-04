    /** 강의노트 원본의 select를 그대로
     * 옮긴 것이다. 무작위인 것은 내부 pivot 선택뿐이고, 결과는 어떤 pivot을
     * 뽑든 항상 정확한 rank번째 값이다. rank는 0-based(0..n-1). */
    static int randomizedSelect(int[] a, int rank, Random random) {
        int lo = 0, hi = a.length;
        while (true) {
            if (hi - lo == 1) return a[lo];
            int pivot = a[lo + random.nextInt(hi - lo)];
            int[] equal = partition3(a, lo, hi, pivot);
            if (rank < equal[0]) hi = equal[0];
            else if (rank >= equal[1]) lo = equal[1];
            else return pivot;
        }
    }

    /** [lt, gt) 구간이 pivot과 같다. */
    private static int[] partition3(int[] a, int lo, int hi, int pivot) {
        int lt = lo, scan = lo, gt = hi;
        while (scan < gt) {
            if (a[scan] < pivot) swap(a, lt++, scan++);
            else if (a[scan] > pivot) swap(a, scan, --gt);
            else scan++;
        }
        return new int[] {lt, gt};
    }

    private static void swap(int[] a, int i, int j) {
        int t = a[i]; a[i] = a[j]; a[j] = t;
    }
