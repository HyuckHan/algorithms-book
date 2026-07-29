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
