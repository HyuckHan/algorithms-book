    public static Result maxSubarrayBruteForce(long[] a) {
        if (a == null || a.length == 0) throw new IllegalArgumentException();
        Result best = new Result(a[0], 0, 0);
        for (int i = 0; i < a.length; i++) {
            long sum = 0;
            for (int j = i; j < a.length; j++) {
                sum = Math.addExact(sum, a[j]);
                if (sum > best.sum()) best = new Result(sum, i, j);
            }
        }
        return best;
    }
