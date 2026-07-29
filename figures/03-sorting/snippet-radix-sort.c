/* LSD Radix Sort (1.6.2). No formal \Procedure pseudocode exists for this
 * section (prose-only in the lecture); this follows the described
 * ones -> tens -> hundreds passes, each a stable counting sort keyed on
 * one digit (`(a[i] / exp) % 10`). */
static void counting_sort_by_digit(int *a, int n, int exp) {
    int out[n];
    int count[10] = {0};
    for (int i = 0; i < n; i++) count[(a[i] / exp) % 10]++;
    for (int d = 1; d < 10; d++) count[d] += count[d - 1];
    for (int i = n - 1; i >= 0; i--) {
        int digit = (a[i] / exp) % 10;
        out[--count[digit]] = a[i];
    }
    for (int i = 0; i < n; i++) a[i] = out[i];
}

static void radix_sort(int *a, int n) {
    int max = a[0];
    for (int i = 1; i < n; i++) if (a[i] > max) max = a[i];
    for (int exp = 1; max / exp > 0; exp *= 10) {
        counting_sort_by_digit(a, n, exp);
    }
}
