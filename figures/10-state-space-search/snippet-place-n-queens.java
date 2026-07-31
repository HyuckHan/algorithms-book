    public Result solve(int n) {
        if (n < 0 || n > 30) throw new IllegalArgumentException();
        Result result = new Result();
        if (n == 0) {
            result.solutions.add(new int[0]);
            return result;
        }
        place(0, n, new int[n], new boolean[n], new boolean[2 * n - 1],
              new boolean[2 * n - 1], result);
        return result;
    }

    private void place(int row, int n, int[] pos, boolean[] col,
                       boolean[] d1, boolean[] d2, Result r) {
        r.expanded++;
        r.maxDepth = Math.max(r.maxDepth, row);
        if (row == n) {
            r.solutions.add(pos.clone());
            return;
        }
        for (int c = 0; c < n; c++) {
            int a = row - c + n - 1;
            int b = row + c;
            if (col[c] || d1[a] || d2[b]) {
                r.pruned++;
                continue;
            }
            col[c] = d1[a] = d2[b] = true;
            pos[row] = c;
            place(row + 1, n, pos, col, d1, d2, r);
            col[c] = d1[a] = d2[b] = false;
        }
    }
