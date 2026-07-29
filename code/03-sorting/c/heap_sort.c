#include <stdio.h>

// snippet:heap-sort:start
/* MAX-HEAPIFY / BUILD-MAX-HEAP / Heapsort (1.5.3). This section's heap
 * array is explicitly 1-based (parent(i)=i/2, left(i)=2i, right(i)=2i+1,
 * per the Index convention callout), so instead of re-deriving 0-based
 * formulas, index 0 of the underlying array is left unused and heap data
 * occupies indices 1..n -- matching the pseudocode's index arithmetic
 * exactly rather than translating it. */
static void swap_at(int *a, int i, int j) {
    int tmp = a[i]; a[i] = a[j]; a[j] = tmp;
}

static void max_heapify(int *a, int i, int heap_size) {
    int l = 2 * i, r = 2 * i + 1, largest = i;
    if (l <= heap_size && a[l] > a[largest]) largest = l;
    if (r <= heap_size && a[r] > a[largest]) largest = r;
    if (largest != i) {
        swap_at(a, i, largest);
        max_heapify(a, largest, heap_size);
    }
}

static void build_max_heap(int *a, int n) {
    for (int i = n / 2; i >= 1; i--) {
        max_heapify(a, i, n);
    }
}

static void heap_sort(int *a, int n) {
    build_max_heap(a, n);
    for (int last = n; last >= 2; last--) {
        swap_at(a, 1, last);
        max_heapify(a, 1, last - 1);
    }
}
// snippet:heap-sort:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 1; i <= n; i++) printf("%d%s", a[i], i < n ? "," : "\n");
}

int main(void) {
    int n = 10;
    int data[11] = {0, 16, 14, 10, 8, 7, 9, 3, 2, 4, 1}; /* index 0 unused */
    print_array("input", data, n);
    heap_sort(data, n);
    print_array("heapsort", data, n);
    return 0;
}
