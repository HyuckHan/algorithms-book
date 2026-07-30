"""SelectBySorting: 정렬 후 rank번째 값을 바로 읽는 baseline(Theta(n log n)).
rank는 0-based(0..n-1), 정렬 장/L03 코드와 같은 색인 관례."""

# snippet:select-by-sorting:start
def select_by_sorting(a, rank):
    return sorted(a)[rank]
# snippet:select-by-sorting:end

if __name__ == "__main__":
    data = [31, 8, 48, 73, 11, 3, 20, 29, 65, 15]
    print("input:", ",".join(str(x) for x in data))
    for rank in (1, 6):
        print("rank:", rank)
        print("result:", select_by_sorting(data, rank))
