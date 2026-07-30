#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>

typedef struct { long long sum; size_t start, end; } MaxSubarrayResult;

/* All Theta(n^2) intervals, matching the "Brute Force" pseudocode exactly
 * (every (i,j) pair, running sum). New for this book -- the canonical file
 * only has the linear-time Kadane form. */

// snippet:max-subarray-brute-force:start
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
// snippet:max-subarray-brute-force:end

static size_t length(MaxSubarrayResult r){return r.end-r.start+1;}
static bool better(MaxSubarrayResult a, MaxSubarrayResult b){
    return a.sum>b.sum||(a.sum==b.sum&&(length(a)<length(b)||(length(a)==length(b)&&a.start<b.start)));
}

/* bestEndingAt[i]/bestOverall (Kadane), matching the DP-template state split.
 * Reused verbatim from lecture-notes/code/lecture05/c/max_subarray.c
 * (max_subarray), renamed to match this chapter's section heading. Nonempty,
 * 0-based inclusive interval. Theta(n) time, Theta(1) space. */

// snippet:max-subarray-kadane:start
static bool max_subarray_kadane(const long long *a,size_t n,MaxSubarrayResult *out){
    if(!a||!out||n==0)return false;
    MaxSubarrayResult ending={a[0],0,0},best=ending;
    for(size_t i=1;i<n;++i){
        MaxSubarrayResult extend={ending.sum+a[i],ending.start,i},restart={a[i],i,i};
        ending=better(restart,extend)?restart:extend;if(better(ending,best))best=ending;
    }*out=best;return true;
}
// snippet:max-subarray-kadane:end

int main(void) {
    const long long a[] = {-2,1,-3,4,-1,2,1,-5,4};
    size_t n = 9;
    MaxSubarrayResult r1, r2;
    max_subarray_brute_force(a, n, &r1);
    max_subarray_kadane(a, n, &r2);
    printf("brute_force sum: %lld start: %zu end: %zu\n", r1.sum, r1.start, r1.end);
    printf("kadane sum: %lld start: %zu end: %zu\n", r2.sum, r2.start, r2.end);
    return 0;
}
