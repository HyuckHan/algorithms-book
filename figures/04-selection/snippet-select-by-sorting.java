    static int selectBySorting(int[] a, int rank) {
        int[] copy = a.clone();
        Arrays.sort(copy);
        return copy[rank];
    }
