    public static Result maxSubarrayKadane(long[] a) {
        if (a == null || a.length == 0) throw new IllegalArgumentException();
        Result ending = new Result(a[0], 0, 0);
        Result best = ending;
        for (int i = 1; i < a.length; i++) {
            Result extend = new Result(Math.addExact(ending.sum(), a[i]), ending.start(), i);
            Result restart = new Result(a[i], i, i);
            ending = better(restart, extend) ? restart : extend;
            if (better(ending, best)) best = ending;
        }
        return best;
    }
