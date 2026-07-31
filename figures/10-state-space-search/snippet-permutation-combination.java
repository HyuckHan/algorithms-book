    public static List<int[]> generate(int n, int k) {
        if (n < 0 || k < 0 || k > n) throw new IllegalArgumentException();
        List<int[]> out = new ArrayList<>();
        dfs(n, k, 0, new boolean[n], new int[k], out);
        return out;
    }

    private static void dfs(int n, int k, int depth, boolean[] used,
                            int[] choice, List<int[]> out) {
        if (depth == k) {
            out.add(choice.clone());
            return;
        }
        for (int value = 0; value < n; value++) {
            if (!used[value]) {
                used[value] = true;
                choice[depth] = value;
                dfs(n, k, depth + 1, used, choice, out);
                used[value] = false;
            }
        }
    }

    public static List<int[]> combinations(int n, int k) {
        if (n < 0 || k < 0 || k > n) throw new IllegalArgumentException();
        List<int[]> out = new ArrayList<>();
        combine(n, k, 0, 0, new int[k], out);
        return out;
    }

    private static void combine(int n, int k, int start, int depth,
                                int[] choice, List<int[]> out) {
        if (depth == k) {
            out.add(choice.clone());
            return;
        }
        for (int value = start; value <= n - (k - depth); value++) {
            choice[depth] = value;
            combine(n, k, value + 1, depth + 1, choice, out);
        }
    }
