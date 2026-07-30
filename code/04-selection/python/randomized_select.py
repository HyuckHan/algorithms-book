"""RandomizedSelect: lecture-notes/code/lecture04/{java,c}의 Quickselect와 같은
반복적 3-way partition(Dutch-flag lt/scan/gt) 구조를 옮긴 것이다. 무작위인 것은
내부 pivot 선택뿐이고, 결과는 어떤 pivot을 뽑든 항상 정확한 rank번째 값이다.
rank는 0-based(0..n-1)."""
import random

# snippet:randomized-select:start
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
# snippet:randomized-select:end

if __name__ == "__main__":
    data = [31, 8, 48, 73, 11, 3, 20, 29, 65, 15]
    print("input:", ",".join(str(x) for x in data))
    for rank in (1, 6):
        print("rank:", rank)
        print("result:", randomized_select(data, rank))
