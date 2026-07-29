#include <stdio.h>

// snippet:counting-sort:start
/* Counting Sort (1.6.1). This procedure's pseudocode signature is A[1..n];
 * rather than reinventing 0-based index arithmetic, this keeps the working
 * A/B arrays 1-based internally (index 0 unused) so the prefix-sum C array
 * and the place-then-decrement order match the pseudocode exactly. */
static void counting_sort(const int *a_zero_based, int n, int k, int *b_zero_based) {
    int a[n + 1];
    for (int j = 1; j <= n; j++) a[j] = a_zero_based[j - 1];

    int c[k + 1];
    for (int i = 0; i <= k; i++) c[i] = 0;
    for (int j = 1; j <= n; j++) c[a[j]]++;
    for (int i = 1; i <= k; i++) c[i] += c[i - 1];

    int b[n + 1];
    for (int j = n; j >= 1; j--) {
        b[c[a[j]]] = a[j];
        c[a[j]]--;
    }
    for (int j = 1; j <= n; j++) b_zero_based[j - 1] = b[j];
}
// snippet:counting-sort:end

static void print_array(const char *label, const int *a, int n) {
    printf("%s: ", label);
    for (int i = 0; i < n; i++) printf("%d%s", a[i], i + 1 < n ? "," : "\n");
}

int main(void) {
    int data[] = {4, 1, 3, 4, 3};
    int n = sizeof(data) / sizeof(data[0]);
    int k = 4;
    int out[5];
    print_array("input", data, n);
    counting_sort(data, n, k, out);
    print_array("counting", out, n);
    return 0;
}
