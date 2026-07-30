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
