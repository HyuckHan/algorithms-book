#include <stdio.h>

// snippet:bubble-sort:start
/* Bubble Sort (1.3.2). Lecture pseudocode is 1-based; this array is 0-based.
 * 1-based `last` runs n downto 2 with inner `i` 1..last-1 comparing
 * A[i],A[i+1]; here 0-based `last` runs n-1 downto 1 with inner `i`
 * 0..last-1 comparing a[i],a[i+1] -- same shape, one less on each index. */
static void bubble_sort(int *a, int n) {
    for (int last = n - 1; last > 0; last--) {
        int swapped = 0;
        for (int i = 0; i < last; i++) {
            if (a[i] > a[i + 1]) {
                int tmp = a[i];
                a[i] = a[i + 1];
                a[i + 1] = tmp;
                swapped = 1;
            }
        }
        if (!swapped) break;
    }
}
// snippet:bubble-sort:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {29, 10, 14, 37, 13, 5, 21, 8};
    int n = sizeof(data) / sizeof(data[0]);
    print_array("input", data, n);
    bubble_sort(data, n);
    print_array("bubble", data, n);
    return 0;
}
