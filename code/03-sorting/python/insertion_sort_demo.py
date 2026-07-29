"""Runs Insertion Sort alone on the 1.3.3 example input, matching the
isolated C (insertion_sort.c) and Java (InsertionSort.java) demos in this
section. The algorithm itself lives in sorting.py (reused, not duplicated)."""
from sorting import insertion_sort

if __name__ == "__main__":
    data = [29, 10, 14, 37, 13, 5, 21, 8]
    print("input:", ",".join(str(x) for x in data))
    sorted_data, _ = insertion_sort(data)
    print("insertion:", ",".join(str(x) for x in sorted_data))
