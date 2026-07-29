#include <stdio.h>

// snippet:quick-sort:start
/* Quick Sort with Lomuto partition (1.4.2). low/high are 0-based inclusive
 * bounds; the initial call is quick_sort(a, 0, n-1) instead of
 * QuickSort(A,1,n), and every index in Partition (pivot=A[high], i=low-1,
 * j from low to high-1) carries over unchanged since it's the same
 * generic-bounds recurrence, just starting from 0 instead of 1. */
static int partition(int *a, int low, int high) {
    int pivot = a[high];
    int i = low - 1;
    for (int j = low; j < high; j++) {
        if (a[j] <= pivot) {
            i++;
            int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
        }
    }
    int tmp = a[i + 1]; a[i + 1] = a[high]; a[high] = tmp;
    return i + 1;
}

static void quick_sort(int *a, int low, int high) {
    if (low < high) {
        int p = partition(a, low, high);
        quick_sort(a, low, p - 1);
        quick_sort(a, p + 1, high);
    }
}
// snippet:quick-sort:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {31, 8, 48, 73, 11, 3, 20, 29, 65, 15};
    int n = sizeof(data) / sizeof(data[0]);
    print_array("input", data, n);
    quick_sort(data, 0, n - 1);
    print_array("quick", data, n);
    return 0;
}
