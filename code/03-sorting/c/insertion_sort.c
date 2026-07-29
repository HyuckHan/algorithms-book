#include <stdio.h>

// snippet:insertion-sort:start
/* Insertion Sort (1.3.3). Lecture pseudocode is 1-based (i from 2 to n,
 * j from i-1 downto 1); this array is 0-based, so i runs 1..n-1 and j
 * runs i-1 downto 0 -- same shape, one less on each index. */
static void insertion_sort(int *a, int n) {
    for (int i = 1; i < n; i++) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            j--;
        }
        a[j + 1] = key;
    }
}
// snippet:insertion-sort:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {29, 10, 14, 37, 13, 5, 21, 8};
    int n = sizeof(data) / sizeof(data[0]);
    print_array("input", data, n);
    insertion_sort(data, n);
    print_array("insertion", data, n);
    return 0;
}
