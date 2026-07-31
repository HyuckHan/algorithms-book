from state_space_search import a_star_grid

if __name__ == "__main__":
    # 5x7 grid, obstacles, S at (0,0), G at (4,6) -- the lecture's own example.
    rows, cols = 5, 7
    blocked = {(0, 3), (1, 3), (2, 1), (2, 2), (2, 3), (3, 5)}
    start, goal = (0, 0), (4, 6)
    cost = a_star_grid(blocked, rows, cols, start, goal, zero_heuristic=False)
    print("cost:", cost)
    dijkstra_cost = a_star_grid(blocked, rows, cols, start, goal, zero_heuristic=True)
    print("dijkstra_cost:", dijkstra_cost)
