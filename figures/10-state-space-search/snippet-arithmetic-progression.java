    public Result solve(int[] input, boolean useBound) {
        if (input == null) throw new IllegalArgumentException();
        int[] a = input.clone();
        Arrays.sort(a);
        Result r = new Result();
        dfs(a, 0, new int[a.length], 0, 0L, false, useBound, r);
        return r;
    }

    private void dfs(int[] a, int i, int[] chosen, int size, long diff,
                     boolean hasDiff, boolean useBound, Result r) {
        r.expanded++;
        if (useBound && size + (a.length - i) <= r.sequence.length) {
            r.pruned++;
            return;
        }
        if (i == a.length) {
            if (size > r.sequence.length) r.sequence = Arrays.copyOf(chosen, size);
            return;
        }
        boolean canTake = size < 2 || (long) a[i] - chosen[size - 1] == diff;
        if (canTake) {
            chosen[size] = a[i];
            long nextDiff = size == 1 ? (long) a[i] - chosen[0] : diff;
            dfs(a, i + 1, chosen, size + 1, nextDiff, size >= 1, useBound, r);
        } else {
            r.pruned++;
        }
        dfs(a, i + 1, chosen, size, diff, hasDiff, useBound, r);
    }
