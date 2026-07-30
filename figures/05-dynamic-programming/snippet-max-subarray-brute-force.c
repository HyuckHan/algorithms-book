static bool max_subarray_brute_force(const long long *a, size_t n, MaxSubarrayResult *out) {
    if (!a || !out || n == 0) return false;
    MaxSubarrayResult best = {a[0], 0, 0};
    for (size_t i = 0; i < n; ++i) {
        long long sum = 0;
        for (size_t j = i; j < n; ++j) {
            sum += a[j];
            if (sum > best.sum) { best.sum = sum; best.start = i; best.end = j; }
        }
    }
    *out = best;
    return true;
}
