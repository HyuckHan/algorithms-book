def a_star_grid(blocked, rows, cols, start, goal, zero_heuristic=False):
    """blocked: set of (r,c) blocked cells. start/goal: (r,c) tuples."""
    import heapq

    def h(cell):
        if zero_heuristic:
            return 0
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    g = {start: 0}
    closed = set()
    counter = 0
    open_heap = [(h(start), 0, counter, start)]
    while open_heap:
        f, entry_g, _, u = heapq.heappop(open_heap)
        if entry_g != g.get(u):
            continue
        if u in closed:
            continue
        closed.add(u)
        if u == goal:
            return entry_g
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            v = (u[0] + dr, u[1] + dc)
            if not (0 <= v[0] < rows and 0 <= v[1] < cols):
                continue
            if v in blocked or v in closed:
                continue
            tentative = g[u] + 1
            if tentative < g.get(v, float("inf")):
                g[v] = tentative
                counter += 1
                heapq.heappush(open_heap, (tentative + h(v), tentative, counter, v))
    return None
