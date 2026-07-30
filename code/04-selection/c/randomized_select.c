#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// snippet:randomized-select:start
/* lecture-notes/code/lecture04/c/quickselect.c의 quickselect_int를 그대로 옮긴
 * 것이다(RandomizedSelect). 무작위인 것은 내부 pivot 선택뿐이고, 결과는 어떤
 * pivot을 뽑든 항상 정확한 rank번째 값이다. rank는 0-based(0..n-1). */
static void swap_int(int *a, int *b) {
    int t = *a; *a = *b; *b = t;
}

/* [lo, hi)를 < pivot, == pivot, > pivot으로 나눈다. */
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

static bool randomized_select(int *a, size_t n, size_t rank, int *result) {
    if (a == NULL || result == NULL || n == 0 || rank >= n) return false;
    size_t lo = 0, hi = n;
    for (;;) {
        if (hi - lo == 1) { *result = a[lo]; return true; }
        size_t pivot_index = lo + (size_t)rand() % (hi - lo);
        int pivot = a[pivot_index];
        size_t lt, gt;
        partition3(a, lo, hi, pivot, &lt, &gt);
        if (rank < lt) hi = lt;
        else if (rank >= gt) lo = gt;
        else { *result = pivot; return true; }
    }
}
// snippet:randomized-select:end

int main(void) {
    srand(20260729u);
    int data[] = {31, 8, 48, 73, 11, 3, 20, 29, 65, 15};
    int n = sizeof(data) / sizeof(data[0]);
    printf("input: ");
    for (int i = 0; i < n; i++) printf("%d%s", data[i], i + 1 < n ? "," : "\n");
    size_t ranks[] = {1, 6};
    for (int i = 0; i < 2; i++) {
        int copy[10];
        for (int j = 0; j < n; j++) copy[j] = data[j];
        int result;
        randomized_select(copy, (size_t)n, ranks[i], &result);
        printf("rank: %zu\n", ranks[i]);
        printf("result: %d\n", result);
    }
    return 0;
}
