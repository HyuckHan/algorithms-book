#include <stdio.h>

// snippet:binary-search:start
/* Binary Search. Lecture pseudocode is 1-based (low=1, high=n); this array
 * is 0-based, so low starts at 0 and high starts at n-1. mid = low +
 * (high-low)/2 matches the pseudocode exactly (already overflow-safe).
 * NOT_FOUND is represented as -1. */
static int binary_search(const int *a, int n, int x) {
    int low = 0, high = n - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (a[mid] == x) return mid;
        else if (a[mid] < x) low = mid + 1;
        else high = mid - 1;
    }
    return -1;
}
// snippet:binary-search:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {3, 6, 9, 12, 15, 18, 21, 24};
    int n = sizeof(data) / sizeof(data[0]);
    int x = 18;
    print_array("input", data, n);
    printf("x: %d\n", x);
    printf("binary: %d\n", binary_search(data, n, x));
    return 0;
}
