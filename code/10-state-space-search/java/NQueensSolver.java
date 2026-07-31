import java.util.ArrayList;
import java.util.List;

/** lecture-notes/code/lecture10/java/NQueensSolver.java와 같은 정책(O(1)
 * promising check via column/diagonal boolean array). */
public final class NQueensSolver {
    public static final class Result {
        public final List<int[]> solutions = new ArrayList<>();
        public long expanded;
        public long pruned;
        public int maxDepth;
    }

    // snippet:place-n-queens:start
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
    // snippet:place-n-queens:end

    public static boolean valid(int[] p) {
        for (int r1 = 0; r1 < p.length; r1++)
            for (int r2 = r1 + 1; r2 < p.length; r2++)
                if (p[r1] == p[r2] || Math.abs(r1 - r2) == Math.abs(p[r1] - p[r2]))
                    return false;
        return true;
    }
}
