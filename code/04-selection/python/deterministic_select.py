"""DeterministicSelect: lecture-notes/code/lecture04/c/deterministic_select.c와
같은 in-place group-of-5 압축(median of medians)을 옮긴 것이다. 최악의 경우에도
Theta(n)을 보장한다. rank는 0-based(0..n-1)."""

# snippet:deterministic-select:start
def _insertion_sort(a, lo, hi):
    for i in range(lo + 1, hi):
        key = a[i]
        j = i
        while j > lo and a[j - 1] > key:
            a[j] = a[j - 1]
            j -= 1
        a[j] = key


def _partition3(a, lo, hi, pivot):
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


def _select_range(a, lo, hi, target):
    while True:
        n = hi - lo
        if n <= 5:
            _insertion_sort(a, lo, hi)
            return a[target]
        groups = 0
        start = lo
        while start < hi:
            end = min(start + 5, hi)
            _insertion_sort(a, start, end)
            median = start + (end - start - 1) // 2  # lower median
            a[lo + groups], a[median] = a[median], a[lo + groups]
            groups += 1
            start += 5
        # 그룹 median들의 median(1-based ceil(groups/2)번째, 0-based로는 (groups-1)//2)
        pivot = _select_range(a, lo, lo + groups, lo + (groups - 1) // 2)
        lt, gt = _partition3(a, lo, hi, pivot)
        if target < lt:
            hi = lt
        elif target >= gt:
            lo = gt
        else:
            return pivot


def deterministic_select(a, rank):
    a = a[:]
    return _select_range(a, 0, len(a), rank)
# snippet:deterministic-select:end

if __name__ == "__main__":
    data = [22, 4, 17, 9, 31, 12, 28, 6, 19, 2, 25, 1, 14, 30, 8,
            16, 27, 5, 23, 10, 20, 3, 29, 7, 24]
    print("input:", ",".join(str(x) for x in data))
    rank = 6
    print("rank:", rank)
    print("result:", deterministic_select(data, rank))
