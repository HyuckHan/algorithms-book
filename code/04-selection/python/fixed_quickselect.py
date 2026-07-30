"""FixedQuickselect: 정렬 장(Quick Sort)의 Lomuto partition(pivot=a[high])을
그대로 재사용해 고정 pivot으로 재귀한다. rank는 0-based(0..n-1)."""

# snippet:fixed-quickselect:start
def _lomuto_partition(a, low, high):
    """정렬 장의 quick_sort partition과 동일한 로직(pivot=a[high])."""
    pivot = a[high]
    i = low - 1
    for j in range(low, high):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[high] = a[high], a[i + 1]
    return i + 1


def fixed_quickselect(a, rank):
    a = a[:]
    low, high = 0, len(a) - 1
    while low < high:
        q = _lomuto_partition(a, low, high)
        if rank == q:
            return a[q]
        elif rank < q:
            high = q - 1
        else:
            low = q + 1
    return a[low]
# snippet:fixed-quickselect:end

if __name__ == "__main__":
    data = [31, 8, 48, 73, 11, 3, 20, 29, 65, 15]
    print("input:", ",".join(str(x) for x in data))
    for rank in (1, 6):
        print("rank:", rank)
        print("result:", fixed_quickselect(data, rank))
