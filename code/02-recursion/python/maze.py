"""Maze path existence via DFS + backtracking."""

ROWS, COLS = 6, 6

# Same 6x6 maze as this section's trace figure: '#' wall, '.' open,
# start=(0,0), exit=(ROWS-1,COLS-1).
GRID = [
    "..####",
    "#.####",
    "....##",
    "##..##",
    "##...#",
    "####..",
]

# snippet:maze:start
def find_path(r, c, visited, path):
    # Base case: outside the grid, a wall, or already visited (False, no
    # further call); reaching the exit cell is also a base case (True, no
    # further call). Recursive case: choose the current cell (mark
    # visited, append to the candidate path), explore each unvisited open
    # neighbor; if every neighbor fails, unchoose (pop the candidate path
    # -- this cell is not on any path to the exit). Progress measure: the
    # count of unvisited open cells strictly decreases. `visited` and
    # `path` are caller-owned (no module-level/global mutable state), so
    # this is self-contained. Neighbor order (up, down, left, right) is
    # arbitrary but fixed.
    if r < 0 or r >= ROWS or c < 0 or c >= COLS:
        return False
    if GRID[r][c] == "#":
        return False
    if visited[r][c]:
        return False

    visited[r][c] = True  # choose
    path.append((r, c))

    if r == ROWS - 1 and c == COLS - 1:
        return True  # exit reached

    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        if find_path(r + dr, c + dc, visited, path):
            return True

    path.pop()  # unchoose: dead end
    return False
# snippet:maze:end

if __name__ == "__main__":
    visited = [[False] * COLS for _ in range(ROWS)]
    path = []
    print("input: 6x6 maze, start=(0,0), exit=(5,5)")
    found = find_path(0, 0, visited, path)
    print("path_exists:", "true" if found else "false")
    print("path:", "->".join("(%d,%d)" % p for p in path))
