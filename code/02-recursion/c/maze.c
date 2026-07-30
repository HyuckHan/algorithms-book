#include <stdio.h>
#include <stdbool.h>
#include <string.h>

#define ROWS 6
#define COLS 6

/* Same 6x6 maze as this section's trace figure: '#' wall, '.' open,
 * start=(0,0), exit=(ROWS-1,COLS-1). */
static const char GRID[ROWS][COLS] = {
    {'.', '.', '#', '#', '#', '#'},
    {'#', '.', '#', '#', '#', '#'},
    {'.', '.', '.', '.', '#', '#'},
    {'#', '#', '.', '.', '#', '#'},
    {'#', '#', '.', '.', '.', '#'},
    {'#', '#', '#', '#', '.', '.'},
};

// snippet:maze:start
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
// snippet:maze:end

int main(void) {
    bool visited[ROWS][COLS];
    memset(visited, 0, sizeof(visited));
    int path_r[ROWS * COLS], path_c[ROWS * COLS];
    int path_len = 0;

    printf("input: 6x6 maze, start=(0,0), exit=(5,5)\n");
    bool found = find_path(0, 0, visited, path_r, path_c, &path_len);
    printf("path_exists: %s\n", found ? "true" : "false");
    printf("path: ");
    for (int i = 0; i < path_len; i++) {
        printf("(%d,%d)%s", path_r[i], path_c[i], i + 1 < path_len ? "->" : "\n");
    }
    return 0;
}
