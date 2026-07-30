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
