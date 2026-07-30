"""Same recurrence as the "Brute Force" pseudocode and the bestEndingAt/
bestOverall DP template (Kadane), and the C/Java demos in this chapter --
newly written in Python, no canonical source exists."""


# snippet:max-subarray-brute-force:start
def max_subarray_brute_force(a):
    best_sum, best_start, best_end = a[0], 0, 0
    for i in range(len(a)):
        running = 0
        for j in range(i, len(a)):
            running += a[j]
            if running > best_sum:
                best_sum, best_start, best_end = running, i, j
    return best_sum, best_start, best_end
# snippet:max-subarray-brute-force:end


def _length(start, end):
    return end - start + 1


def _better(a, b):
    a_sum, a_start, a_end = a
    b_sum, b_start, b_end = b
    if a_sum != b_sum:
        return a_sum > b_sum
    a_len, b_len = _length(a_start, a_end), _length(b_start, b_end)
    if a_len != b_len:
        return a_len < b_len
    return a_start < b_start


# snippet:max-subarray-kadane:start
def max_subarray_kadane(a):
    ending = (a[0], 0, 0)
    best = ending
    for i in range(1, len(a)):
        extend = (ending[0] + a[i], ending[1], i)
        restart = (a[i], i, i)
        ending = restart if _better(restart, extend) else extend
        if _better(ending, best):
            best = ending
    return best
# snippet:max-subarray-kadane:end


if __name__ == "__main__":
    a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    bf_sum, bf_start, bf_end = max_subarray_brute_force(a)
    kd_sum, kd_start, kd_end = max_subarray_kadane(a)
    print("brute_force sum:", bf_sum, "start:", bf_start, "end:", bf_end)
    print("kadane sum:", kd_sum, "start:", kd_start, "end:", kd_end)
