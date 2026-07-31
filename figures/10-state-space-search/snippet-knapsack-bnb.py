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
