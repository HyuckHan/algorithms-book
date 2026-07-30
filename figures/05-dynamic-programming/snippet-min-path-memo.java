    private static long minPathMemoRec(long[][] a, int i, int j, long[][] memo, boolean[][] seen) {
        if (seen[i][j]) return memo[i][j];
        long result;
        if (i == 0 && j == 0) {
            result = a[0][0];
        } else if (i == 0) {
            result = minPathMemoRec(a, i, j - 1, memo, seen) + a[i][j];
        } else if (j == 0) {
            result = minPathMemoRec(a, i - 1, j, memo, seen) + a[i][j];
        } else {
            long up = minPathMemoRec(a, i - 1, j, memo, seen);
            long left = minPathMemoRec(a, i, j - 1, memo, seen);
            result = (up <= left ? up : left) + a[i][j];
        }
        seen[i][j] = true;
        memo[i][j] = result;
        return result;
    }

    public static long minPathMemo(long[][] a) {
        int r = a.length, c = a[0].length;
        long[][] memo = new long[r][c];
        boolean[][] seen = new boolean[r][c];
        return minPathMemoRec(a, r - 1, c - 1, memo, seen);
    }
