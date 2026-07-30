    public static int[] path(Result r, int target) {
        if (r.dist()[target] == INF || r.negativeCycle()) return new int[0];
        List<Integer> rev = new ArrayList<>();
        boolean[] seen = new boolean[r.parent().length];
        for (int v = target; v >= 0; v = r.parent()[v]) {
            if (seen[v]) throw new IllegalStateException("parent cycle");
            seen[v] = true; rev.add(v);
        }
        Collections.reverse(rev);
        return rev.stream().mapToInt(Integer::intValue).toArray();
    }
