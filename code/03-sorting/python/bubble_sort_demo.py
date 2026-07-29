"""Runs Bubble Sort alone on the 1.3.2 example input, matching the isolated
C (bubble_sort.c) and Java (BubbleSort.java) demos in this section. The
algorithm itself lives in sorting.py (reused, not duplicated)."""
from sorting import bubble_sort

if __name__ == "__main__":
    data = [29, 10, 14, 37, 13, 5, 21, 8]
    print("input:", ",".join(str(x) for x in data))
    sorted_data, _ = bubble_sort(data)
    print("bubble:", ",".join(str(x) for x in sorted_data))
