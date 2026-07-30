#include <stdio.h>

// snippet:linear-search:start
/* Linear Search. Lecture pseudocode is 1-based (i from 1 to n); this array
 * is 0-based, so i runs 0..n-1. NOT_FOUND is represented as -1. */
static int linear_search(const int *a, int n, int x) {
    for (int i = 0; i < n; i++) {
        if (a[i] == x) return i;
    }
    return -1;
}
// snippet:linear-search:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {3, 6, 9, 12, 15, 18, 21, 24};
    int n = sizeof(data) / sizeof(data[0]);
    int x = 12;
    print_array("input", data, n);
    printf("x: %d\n", x);
    printf("linear: %d\n", linear_search(data, n, x));
    return 0;
}
