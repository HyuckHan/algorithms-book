public final class Maze {
    static final int ROWS = 6;
    static final int COLS = 6;

    /** Same 6x6 maze as this section's trace figure: '#' wall, '.' open,
     * start=(0,0), exit=(ROWS-1,COLS-1). */
    static final char[][] GRID = {
        {'.', '.', '#', '#', '#', '#'},
        {'#', '.', '#', '#', '#', '#'},
        {'.', '.', '.', '.', '#', '#'},
        {'#', '#', '.', '.', '#', '#'},
        {'#', '#', '.', '.', '.', '#'},
        {'#', '#', '#', '#', '.', '.'},
    };

    // snippet:maze:start
    /** Maze path existence via DFS + backtracking. Base case: outside the
     * grid, a wall, or already visited (false, no further call); reaching
     * the exit cell is also a base case (true, no further call). Recursive
     * case: choose the current cell (mark visited, append to the candidate
     * path), explore each unvisited open neighbor; if every neighbor
     * fails, unchoose (pop the candidate path -- this cell is not on any
     * path to the exit). Progress measure: the count of unvisited open
     * cells strictly decreases. `visited` and the candidate path are
     * local arrays created by main() and threaded through by parameter
     * (no static/global mutable state), so this is self-contained.
     * Neighbor order (up, down, left, right) is arbitrary but fixed. */
    static boolean findPath(int r, int c, boolean[][] visited, int[] pathR, int[] pathC, int[] pathLen) {
        if (r < 0 || r >= ROWS || c < 0 || c >= COLS) return false;
        if (GRID[r][c] == '#') return false;
        if (visited[r][c]) return false;

        visited[r][c] = true;                 // choose
        pathR[pathLen[0]] = r;
        pathC[pathLen[0]] = c;
        pathLen[0]++;

        if (r == ROWS - 1 && c == COLS - 1) return true;  // exit reached

        int[] dr = {-1, 1, 0, 0};
        int[] dc = {0, 0, -1, 1};
        for (int d = 0; d < 4; d++) {
            if (findPath(r + dr[d], c + dc[d], visited, pathR, pathC, pathLen)) {
                return true;
            }
        }

        pathLen[0]--;                          // unchoose: dead end
        return false;
    }
    // snippet:maze:end

    public static void main(String[] args) {
        boolean[][] visited = new boolean[ROWS][COLS];
        int[] pathR = new int[ROWS * COLS];
        int[] pathC = new int[ROWS * COLS];
        int[] pathLen = {0};

        System.out.println("input: 6x6 maze, start=(0,0), exit=(5,5)");
        boolean found = findPath(0, 0, visited, pathR, pathC, pathLen);
        System.out.println("path_exists: " + found);
        StringBuilder sb = new StringBuilder("path: ");
        for (int i = 0; i < pathLen[0]; i++) {
            sb.append("(").append(pathR[i]).append(",").append(pathC[i]).append(")");
            if (i + 1 < pathLen[0]) sb.append("->");
        }
        System.out.println(sb);
    }
}
