def max_subarray_brute_force(a):
    best_sum, best_start, best_end = a[0], 0, 0
    for i in range(len(a)):
        running = 0
        for j in range(i, len(a)):
            running += a[j]
            if running > best_sum:
                best_sum, best_start, best_end = running, i, j
    return best_sum, best_start, best_end
