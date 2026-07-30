#include <stdio.h>
#include <stdlib.h>

// snippet:select-by-sorting:start
static int compare_int(const void *pa, const void *pb) {
    int a = *(const int *)pa, b = *(const int *)pb;
    return (a > b) - (a < b);
}

static int select_by_sorting(const int *a, int n, int rank) {
    int *copy = malloc((size_t)n * sizeof *copy);
    for (int i = 0; i < n; i++) copy[i] = a[i];
    qsort(copy, (size_t)n, sizeof *copy, compare_int);
    int result = copy[rank];
    free(copy);
    return result;
}
// snippet:select-by-sorting:end

int main(void) {
    int data[] = {31, 8, 48, 73, 11, 3, 20, 29, 65, 15};
    int n = sizeof(data) / sizeof(data[0]);
    printf("input: ");
    for (int i = 0; i < n; i++) printf("%d%s", data[i], i + 1 < n ? "," : "\n");
    int ranks[] = {1, 6};
    for (int i = 0; i < 2; i++) {
        printf("rank: %d\n", ranks[i]);
        printf("result: %d\n", select_by_sorting(data, n, ranks[i]));
    }
    return 0;
}
