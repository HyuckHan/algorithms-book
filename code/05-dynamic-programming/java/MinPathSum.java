public final class MinPathSum {
    public record Result(long sum, int[][] path) {}
    private MinPathSum() {}

    // Top-down with memoization (sentinel `seen[i][j]`), matching the
    // MinPathMemo pseudocode's boundary recurrence exactly. New for this
    // book -- the canonical Java only has the bottom-up loop version.
    // snippet:min-path-memo:start
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
    // snippet:min-path-memo:end

    // Bottom-up, row-major evaluation order. Reused verbatim from
    // lecture-notes/code/lecture05/java/MinPathSum.java (solve), renamed to
    // match this chapter's pseudocode block name. Rectangular matrix,
    // right/down. Theta(rows*cols) time/table space.
    // snippet:matrix-bottom-up:start
    public static Result minPathBottomUp(long[][] a) {
        if (a == null || a.length == 0 || a[0] == null || a[0].length == 0) {
            throw new IllegalArgumentException();
        }
        int rows = a.length, cols = a[0].length;
        for (long[] row : a) {
            if (row == null || row.length != cols) throw new IllegalArgumentException();
        }

        long[][] dp = new long[rows][cols];
        byte[][] parent = new byte[rows][cols]; // 1=up, 2=left
        dp[0][0] = a[0][0];
        for (int j = 1; j < cols; j++) {
            dp[0][j] = Math.addExact(dp[0][j - 1], a[0][j]);
            parent[0][j] = 2;
        }
        for (int i = 1; i < rows; i++) {
            dp[i][0] = Math.addExact(dp[i - 1][0], a[i][0]);
            parent[i][0] = 1;
        }
        for (int i = 1; i < rows; i++) {
            for (int j = 1; j < cols; j++) {
                long up = dp[i - 1][j], left = dp[i][j - 1];
                if (up <= left) {
                    dp[i][j] = Math.addExact(up, a[i][j]);
                    parent[i][j] = 1;
                } else {
                    dp[i][j] = Math.addExact(left, a[i][j]);
                    parent[i][j] = 2;
                }
            }
        }

        int[][] path = new int[rows + cols - 1][2];
        int i = rows - 1, j = cols - 1;
        for (int k = path.length - 1; k >= 0; k--) {
            path[k][0] = i;
            path[k][1] = j;
            if (i == 0 && j == 0) break;
            if (parent[i][j] == 1) i--; else j--;
        }
        return new Result(dp[rows - 1][cols - 1], path);
    }
    // snippet:matrix-bottom-up:end

    public static void main(String[] args) {
        long[][] m = {{6,7,12,5},{5,3,11,18},{7,17,3,3},{8,10,14,9}};
        System.out.println("memo sum: " + minPathMemo(m));
        Result r = minPathBottomUp(m);
        System.out.println("bottom_up sum: " + r.sum());
        StringBuilder sb = new StringBuilder("path:");
        for (int[] cell : r.path()) sb.append(" (").append(cell[0] + 1).append(",").append(cell[1] + 1).append(")");
        System.out.println(sb);
    }
}
