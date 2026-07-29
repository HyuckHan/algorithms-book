"""Runs Selection Sort alone on the 1.3.1 example input, matching the
isolated C (selection_sort.c) and Java (SelectionSort.java) demos in this
section (see scripts/run_examples.py). The algorithm itself lives in
sorting.py (reused, not duplicated) since it's already the from-scratch
Python reference (ADR-004)."""
from sorting import selection_sort

if __name__ == "__main__":
    data = [29, 10, 14, 37, 13, 5, 21, 8]
    print("input:", ",".join(str(x) for x in data))
    sorted_data, _ = selection_sort(data)
    print("selection:", ",".join(str(x) for x in sorted_data))
