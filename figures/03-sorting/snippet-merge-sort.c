/* Merge Sort (1.4.1). low/high are 0-based inclusive bounds -- the lecture
 * pseudocode's low/high play the same role over 1-based bounds; the
 * initial call here is merge_sort(a, 0, n-1) instead of MergeSort(A,1,n).
 * mid uses the overflow-safe `low + (high-low)/2` form from this section's
 * "흔한 실수" callout, not `(low+high)/2`. */
static void merge(int *a, int low, int mid, int high) {
    int n1 = mid - low + 1;
    int n2 = high - mid;
    int L[n1], R[n2];
    for (int x = 0; x < n1; x++) L[x] = a[low + x];
    for (int x = 0; x < n2; x++) R[x] = a[mid + 1 + x];

    int i = 0, j = 0, k = low;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) a[k++] = L[i++];
        else              a[k++] = R[j++];
    }
    while (i < n1) a[k++] = L[i++];
    while (j < n2) a[k++] = R[j++];
}

static void merge_sort(int *a, int low, int high) {
    if (low >= high) return;
    int mid = low + (high - low) / 2;
    merge_sort(a, low, mid);
    merge_sort(a, mid + 1, high);
    merge(a, low, mid, high);
}
