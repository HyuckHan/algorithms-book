import java.util.ArrayList;
import java.util.List;

/** lecture-notes/code/lecture10/java/SubsetSumSolver.java와 같은 정책(양의
 * weight 전제 아래 두 sound pruning: sum>target, sum+remaining<target). */
public final class SubsetSumSolver {
    public static final class Result {
        public final List<int[]> indexSolutions = new ArrayList<>();
        public long expanded;
        public long pruned;
    }

    // snippet:subset-sum:start
    public Result solve(int[] weights, long target, boolean usePruning) {
        if (weights == null || target < 0) throw new IllegalArgumentException();
        long remaining = 0;
        for (int w : weights) {
            if (w <= 0) throw new IllegalArgumentException("positive weights required");
            remaining = Math.addExact(remaining, w);
        }
        Result r = new Result();
        dfs(weights, target, 0, 0, remaining, new int[weights.length], 0,
            usePruning, r);
        return r;
    }

    private void dfs(int[] w, long target, int i, long sum, long remaining,
                     int[] chosen, int size, boolean prune, Result r) {
        r.expanded++;
        if (sum == target) {
            int[] answer = new int[size];
            System.arraycopy(chosen, 0, answer, 0, size);
            r.indexSolutions.add(answer);
            return;
        }
        if (i == w.length) return;
        if (prune && (sum > target || sum + remaining < target)) {
            r.pruned++;
            return;
        }
        chosen[size] = i;
        dfs(w, target, i + 1, Math.addExact(sum, w[i]), remaining - w[i],
            chosen, size + 1, prune, r);
        dfs(w, target, i + 1, sum, remaining - w[i], chosen, size, prune, r);
    }
    // snippet:subset-sum:end

    public static long sum(int[] weights, int[] indices) {
        long s = 0;
        for (int i : indices) s = Math.addExact(s, weights[i]);
        return s;
    }
}
