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
