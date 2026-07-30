public final class PowerSet {
    static final int N = 3;
    static final char[] DATA = {'a', 'b', 'c'};

    static void printSelected(boolean[] include) {
        StringBuilder sb = new StringBuilder("{");
        boolean first = true;
        for (int i = 0; i < N; i++) {
            if (include[i]) {
                if (!first) sb.append(",");
                sb.append(DATA[i]);
                first = false;
            }
        }
        sb.append("}");
        System.out.println(sb);
    }

    // snippet:power-set:start
    /** Power Set. Base case: k == n (all n elements decided; prints the
     * current selection, including the empty set). Recursive case:
     * exclude data[k] first, then include it -- this exclude-before-include
     * order at every level makes the printed order match the state-space
     * tree's left-to-right leaf order exactly (see 13-power-set-tree).
     * Progress measure: k -> k+1. Max call-stack depth is n. `include` is
     * a caller-owned array (no static/global state), threaded through by
     * parameter. */
    static void powerSet(int k, int n, boolean[] include) {
        if (k == n) {
            printSelected(include);
            return;
        }
        include[k] = false;
        powerSet(k + 1, n, include);
        include[k] = true;
        powerSet(k + 1, n, include);
    }
    // snippet:power-set:end

    public static void main(String[] args) {
        boolean[] include = new boolean[N];
        System.out.println("input: {a,b,c}");
        powerSet(0, N, include);
    }
}
