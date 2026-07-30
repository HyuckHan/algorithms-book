#include <stdio.h>

// snippet:maximum:start
/* Maximum. Lecture pseudocode is 1-based (v <- A[1], i from 2 to n); this
 * array is 0-based, so v starts at a[0] and i runs 1..n-1. Precondition:
 * n >= 1 (non-empty array). */
static int maximum(const int *a, int n) {
    int v = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] > v) v = a[i];
    }
    return v;
}
// snippet:maximum:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {7, 12, 3, 15, 8};
    int n = sizeof(data) / sizeof(data[0]);
    print_array("input", data, n);
    printf("maximum: %d\n", maximum(data, n));
    return 0;
}
