"""Runs Quick Sort alone on the 1.4.2 example input (matching this section's
Lomuto-partition trace figure, where the first partition call resolves
pivot=15 to its final index), mirroring the isolated C (quick_sort.c) and
Java (QuickSort.java) demos. The algorithm itself lives in sorting.py
(reused, not duplicated)."""
from sorting import quick_sort

if __name__ == "__main__":
    data = [31, 8, 48, 73, 11, 3, 20, 29, 65, 15]
    print("input:", ",".join(str(x) for x in data))
    sorted_data = quick_sort(data)
    print("quick:", ",".join(str(x) for x in sorted_data))
