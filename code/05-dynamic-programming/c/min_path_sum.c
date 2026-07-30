#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct { long long sum; size_t *rows, *cols, length; } PathResult;

/* Top-down with memoization (sentinel `seen[i][j]`), matching the
 * MinPathMemo pseudocode's boundary recurrence exactly: base cell (0,0),
 * first row/column accumulate, interior cell is M[i][j]+min(up,left). New
 * for this book -- the naive/memoized recursive forms don't exist in the
 * canonical lecture-notes C, only the bottom-up loop version does. */

// snippet:min-path-memo:start
static long long min_path_memo_rec(const long long *a, size_t cols, int i, int j, long long *memo, bool *seen) {
    size_t k = (size_t)i * cols + (size_t)j;
    if (seen[k]) return memo[k];
    long long result;
    if (i == 0 && j == 0) {
        result = a[k];
    } else if (i == 0) {
        result = min_path_memo_rec(a, cols, i, j - 1, memo, seen) + a[k];
    } else if (j == 0) {
        result = min_path_memo_rec(a, cols, i - 1, j, memo, seen) + a[k];
    } else {
        long long up = min_path_memo_rec(a, cols, i - 1, j, memo, seen);
        long long left = min_path_memo_rec(a, cols, i, j - 1, memo, seen);
        result = (up <= left ? up : left) + a[k];
    }
    seen[k] = true;
    memo[k] = result;
    return result;
}

static bool min_path_memo(const long long *a, size_t rows, size_t cols, long long *out) {
    if (!a || !out || rows == 0 || cols == 0) return false;
    size_t n = rows * cols;
    long long *memo = malloc(n * sizeof(*memo));
    bool *seen = calloc(n, sizeof(*seen));
    if (!memo || !seen) { free(memo); free(seen); return false; }
    *out = min_path_memo_rec(a, cols, (int)rows - 1, (int)cols - 1, memo, seen);
    free(memo); free(seen);
    return true;
}
// snippet:min-path-memo:end

/* Bottom-up, row-major evaluation order (Bottom-Up Evaluation Order
 * pseudocode). Reused verbatim from lecture-notes/code/lecture05/c/min_path_sum.c
 * (min_path), renamed to match this chapter's pseudocode block name. */

// snippet:matrix-bottom-up:start
static bool min_path_bottom_up(const long long *a, size_t rows, size_t cols, PathResult *out) {
    if (!a || !out || rows == 0 || cols == 0) return false;
    size_t n = rows * cols;
    long long *dp = malloc(n * sizeof(*dp));
    unsigned char *parent = calloc(n, 1); /* 1=up, 2=left */
    if (!dp || !parent) { free(dp); free(parent); return false; }
    dp[0] = a[0];
    for (size_t j=1;j<cols;++j){dp[j]=dp[j-1]+a[j];parent[j]=2;}
    for (size_t i=1;i<rows;++i){dp[i*cols]=dp[(i-1)*cols]+a[i*cols];parent[i*cols]=1;}
    for (size_t i=1;i<rows;++i) for(size_t j=1;j<cols;++j){
        size_t k=i*cols+j; long long up=dp[k-cols], left=dp[k-1];
        if (up <= left) { dp[k]=up+a[k]; parent[k]=1; } /* tie: up */
        else { dp[k]=left+a[k]; parent[k]=2; }
    }
    size_t len=rows+cols-1;
    out->rows=malloc(len*sizeof(*out->rows)); out->cols=malloc(len*sizeof(*out->cols));
    if(!out->rows||!out->cols){free(out->rows);free(out->cols);free(dp);free(parent);return false;}
    size_t i=rows-1,j=cols-1,pos=len;
    while(pos){--pos;out->rows[pos]=i;out->cols[pos]=j;if(i==0&&j==0)break;if(parent[i*cols+j]==1)--i;else --j;}
    out->sum=dp[n-1];out->length=len;free(dp);free(parent);return true;
}
// snippet:matrix-bottom-up:end

static void release(PathResult *r) { free(r->rows); free(r->cols); }

int main(void) {
    const long long m[] = {6,7,12,5, 5,3,11,18, 7,17,3,3, 8,10,14,9};
    long long memo_sum = -1;
    min_path_memo(m, 4, 4, &memo_sum);
    printf("memo sum: %lld\n", memo_sum);

    PathResult r = {0};
    min_path_bottom_up(m, 4, 4, &r);
    printf("bottom_up sum: %lld\n", r.sum);
    printf("path:");
    for (size_t k = 0; k < r.length; ++k) printf(" (%zu,%zu)", r.rows[k] + 1, r.cols[k] + 1);
    printf("\n");
    release(&r);
    return 0;
}
