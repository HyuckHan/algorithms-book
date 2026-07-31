"""State-space tree search: permutation/combination generation, N-Queens,
Subset Sum, Graph Coloring (all backtracking), 0/1 Knapsack (branch-and-bound),
A* grid search. Policy matches lecture-notes/code/lecture10's Java/C: 0-based
indexing, sound feasibility/objective pruning, deterministic tie-breaking."""


# snippet:permutation-combination:start
def choose_permutation(n, k):
    result = []
    used = [False] * n
    choice = [0] * k

    def recurse(depth):
        if depth == k:
            result.append(tuple(choice))
            return
        for value in range(n):
            if not used[value]:
                used[value] = True
                choice[depth] = value
                recurse(depth + 1)
                used[value] = False

    recurse(0)
    return result


def choose_combination(n, k):
    result = []
    choice = [0] * k

    def recurse(start, depth):
        if depth == k:
            result.append(tuple(choice))
            return
        for value in range(start, n - (k - depth) + 1):
            choice[depth] = value
            recurse(value + 1, depth + 1)

    recurse(0, 0)
    return result
# snippet:permutation-combination:end


# snippet:place-n-queens:start
def solve_n_queens(n):
    solutions = []
    position = [0] * n
    used_col = [False] * n
    diag1 = [False] * (2 * n - 1) if n > 0 else []
    diag2 = [False] * (2 * n - 1) if n > 0 else []

    def place(row):
        if row == n:
            solutions.append(tuple(position))
            return
        for col in range(n):
            a = row - col + n - 1
            b = row + col
            if used_col[col] or diag1[a] or diag2[b]:
                continue
            used_col[col] = diag1[a] = diag2[b] = True
            position[row] = col
            place(row + 1)
            used_col[col] = diag1[a] = diag2[b] = False

    if n == 0:
        return [()]
    place(0)
    return solutions
# snippet:place-n-queens:end


# snippet:subset-sum:start
def subset_sum(weights, target):
    n = len(weights)
    remaining_total = sum(weights)
    result = []

    def recurse(i, current_sum, remaining, selected):
        if current_sum == target:
            result.append(tuple(selected))
            return
        if i == n or current_sum > target or current_sum + remaining < target:
            return
        selected.append(i)
        recurse(i + 1, current_sum + weights[i], remaining - weights[i], selected)
        selected.pop()
        recurse(i + 1, current_sum, remaining - weights[i], selected)

    recurse(0, 0, remaining_total, [])
    return result
# snippet:subset-sum:end


# snippet:color-graph-coloring:start
def color_graph(adjacency, m):
    n = len(adjacency)
    color = [0] * n

    def safe(v, c):
        return all(not (adjacency[v][u] and color[u] == c) for u in range(v))

    def recurse(v):
        if v == n:
            return True
        for c in range(1, m + 1):
            if safe(v, c):
                color[v] = c
                if recurse(v + 1):
                    return True
                color[v] = 0
        return False

    return list(color) if recurse(0) else None
# snippet:color-graph-coloring:end


# snippet:knapsack-bnb:start
def knapsack_bnb(items, capacity):
    """items: list of (weight, profit). Returns (best_profit, best_weight)."""
    order = sorted(range(len(items)), key=lambda i: -(items[i][1] / items[i][0]))
    sorted_items = [items[i] for i in order]
    n = len(sorted_items)

    def bound(level, weight, profit):
        if weight > capacity:
            return -1.0
        value = float(profit)
        remaining = capacity - weight
        for i in range(level, n):
            w, p = sorted_items[i]
            if remaining <= 0:
                break
            if w <= remaining:
                remaining -= w
                value += p
            else:
                value += p * remaining / w
                remaining = 0
        return value

    import heapq
    best_profit, best_weight = 0, 0
    counter = 0
    root_bound = bound(0, 0, 0)
    heap = [(-root_bound, counter, 0, 0, 0)]
    while heap:
        neg_bound, _, level, weight, profit = heapq.heappop(heap)
        node_bound = -neg_bound
        if node_bound <= best_profit:
            continue
        if level == n:
            continue
        w, p = sorted_items[level]
        if weight + w <= capacity:
            take_weight, take_profit = weight + w, profit + p
            if take_profit > best_profit:
                best_profit, best_weight = take_profit, take_weight
            take_bound = bound(level + 1, take_weight, take_profit)
            if take_bound > best_profit:
                counter += 1
                heapq.heappush(heap, (-take_bound, counter, level + 1, take_weight, take_profit))
        skip_bound = bound(level + 1, weight, profit)
        if skip_bound > best_profit:
            counter += 1
            heapq.heappush(heap, (-skip_bound, counter, level + 1, weight, profit))
    return best_profit, best_weight
# snippet:knapsack-bnb:end


# snippet:a-star:start
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
# snippet:a-star:end
