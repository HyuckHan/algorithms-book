#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>

// snippet:deterministic-select:start
/* lecture-notes/code/lecture04/c/deterministic_select.c의
 * deterministic_select_int를 그대로 옮긴 것이다(Median of Medians, group of 5).
 * 최악의 경우에도 Theta(n)을 보장한다. rank는 0-based(0..n-1). */
static void swap_int(int *a, int *b) { int t = *a; *a = *b; *b = t; }

static void insertion_sort(int *a, size_t lo, size_t hi) {
    for (size_t i = lo + 1; i < hi; ++i) {
        int key = a[i]; size_t j = i;
        while (j > lo && a[j - 1] > key) { a[j] = a[j - 1]; --j; }
        a[j] = key;
    }
}

static void partition3(int *a, size_t lo, size_t hi, int pivot,
                       size_t *lt_out, size_t *gt_out) {
    size_t lt = lo, scan = lo, gt = hi;
    while (scan < gt) {
        if (a[scan] < pivot) swap_int(&a[lt++], &a[scan++]);
        else if (a[scan] > pivot) swap_int(&a[scan], &a[--gt]);
        else ++scan;
    }
    *lt_out = lt; *gt_out = gt;
}

static int select_range(int *a, size_t lo, size_t hi, size_t target) {
    for (;;) {
        size_t n = hi - lo;
        if (n <= 5) { insertion_sort(a, lo, hi); return a[target]; }
        size_t groups = 0;
        for (size_t start = lo; start < hi; start += 5) {
            size_t end = start + 5 < hi ? start + 5 : hi;
            insertion_sort(a, start, end);
            size_t median = start + (end - start - 1) / 2; /* lower median */
            swap_int(&a[lo + groups], &a[median]);
            ++groups;
        }
        /* 그룹 median들의 median: 1-based ceil(groups/2)번째. */
        int pivot = select_range(a, lo, lo + groups,
                                 lo + (groups - 1) / 2);
        size_t lt, gt;
        partition3(a, lo, hi, pivot, &lt, &gt);
        if (target < lt) hi = lt;
        else if (target >= gt) lo = gt;
        else return pivot;
    }
}

static bool deterministic_select(int *a, size_t n, size_t rank, int *result) {
    if (a == NULL || result == NULL || n == 0 || rank >= n) return false;
    *result = select_range(a, 0, n, rank);
    return true;
}
// snippet:deterministic-select:end

int main(void) {
    int data[] = {22, 4, 17, 9, 31, 12, 28, 6, 19, 2, 25, 1, 14, 30, 8,
                  16, 27, 5, 23, 10, 20, 3, 29, 7, 24};
    int n = sizeof(data) / sizeof(data[0]);
    printf("input: ");
    for (int i = 0; i < n; i++) printf("%d%s", data[i], i + 1 < n ? "," : "\n");
    size_t rank = 6;
    int result;
    deterministic_select(data, (size_t)n, rank, &result);
    printf("rank: %zu\n", rank);
    printf("result: %d\n", result);
    return 0;
}
