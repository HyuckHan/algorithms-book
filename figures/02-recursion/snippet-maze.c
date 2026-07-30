/* Maze path existence via DFS + backtracking. Base case: outside the
 * grid, a wall, or already visited (false, no further call); reaching
 * the exit cell is also a base case (true, no further call). Recursive
 * case: choose the current cell (mark visited, append to the candidate
 * path), explore each unvisited open neighbor; if every neighbor fails,
 * unchoose (pop the candidate path -- this cell is not on any path to
 * the exit). Progress measure: the count of unvisited open cells
 * strictly decreases. `visited` and the candidate path are local
 * arrays owned by the caller and threaded through by pointer/parameter
 * (no global state), so this is self-contained. Neighbor order
 * (up, down, left, right) is arbitrary but fixed. */
static bool find_path(int r, int c, bool visited[ROWS][COLS],
                      int path_r[], int path_c[], int *path_len) {
    if (r < 0 || r >= ROWS || c < 0 || c >= COLS) return false;
    if (GRID[r][c] == '#') return false;
    if (visited[r][c]) return false;

    visited[r][c] = true;                    /* choose */
    path_r[*path_len] = r;
    path_c[*path_len] = c;
    (*path_len)++;

    if (r == ROWS - 1 && c == COLS - 1) return true;   /* exit reached */

    static const int DR[4] = {-1, 1, 0, 0};
    static const int DC[4] = {0, 0, -1, 1};
    for (int d = 0; d < 4; d++) {
        if (find_path(r + DR[d], c + DC[d], visited, path_r, path_c, path_len)) {
            return true;
        }
    }

    (*path_len)--;                           /* unchoose: dead end */
    return false;
}
