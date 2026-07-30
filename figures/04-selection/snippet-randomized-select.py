def _partition3(a, lo, hi, pivot):
    """[lt, gt) 구간이 pivot과 같다: a[lo:lt] < pivot, a[lt:gt] == pivot, a[gt:hi] > pivot."""
    lt, scan, gt = lo, lo, hi
    while scan < gt:
        if a[scan] < pivot:
            a[lt], a[scan] = a[scan], a[lt]
            lt += 1
            scan += 1
        elif a[scan] > pivot:
            gt -= 1
            a[scan], a[gt] = a[gt], a[scan]
        else:
            scan += 1
    return lt, gt


def randomized_select(a, rank):
    a = a[:]
    lo, hi = 0, len(a)
    while True:
        if hi - lo == 1:
            return a[lo]
        pivot = a[random.randrange(lo, hi)]
        lt, gt = _partition3(a, lo, hi, pivot)
        if rank < lt:
            hi = lt
        elif rank >= gt:
            lo = gt
        else:
            return pivot
