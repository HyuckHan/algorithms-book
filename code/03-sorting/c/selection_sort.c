#include <stdio.h>

// snippet:selection-sort:start
/* Selection Sort (1.3.1). Lecture pseudocode is 1-based; this array is
 * 0-based, so `last` here is one less than the lecture's `last`, and the
 * scan for the max runs over indices 1..last inclusive either way. */
static void selection_sort(int *a, int n) {
    for (int last = n - 1; last > 0; last--) {
        int m = 0;
        for (int i = 1; i <= last; i++) {
            if (a[i] > a[m]) m = i;
        }
        int tmp = a[m];
        a[m] = a[last];
        a[last] = tmp;
    }
}
// snippet:selection-sort:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {29, 10, 14, 37, 13, 5, 21, 8};
    int n = sizeof(data) / sizeof(data[0]);
    print_array("input", data, n);
    selection_sort(data, n);
    print_array("selection", data, n);
    return 0;
}
