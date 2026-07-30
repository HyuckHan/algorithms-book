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
