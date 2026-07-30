/* Linear Search. Lecture pseudocode is 1-based (i from 1 to n); this array
 * is 0-based, so i runs 0..n-1. NOT_FOUND is represented as -1. */
static int linear_search(const int *a, int n, int x) {
    for (int i = 0; i < n; i++) {
        if (a[i] == x) return i;
    }
    return -1;
}
