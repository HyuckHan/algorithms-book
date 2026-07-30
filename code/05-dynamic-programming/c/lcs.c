#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Bottom-up, tie-up backtracking. Reused verbatim from
 * lecture-notes/code/lecture05/c/lcs.c (lcs), renamed to match this
 * chapter's pseudocode block name ("LCS Bottom-Up"). Theta(m*n) time/table
 * space. Caller frees *out. */

// snippet:lcs-bottom-up:start
static bool lcs_bottom_up(const char *x, const char *y, char **out) {
    if (!x || !y || !out) return false;
    size_t m=strlen(x),n=strlen(y),w=n+1;
    size_t *dp=calloc((m+1)*w,sizeof(*dp)); if(!dp)return false;
    for(size_t i=1;i<=m;++i)for(size_t j=1;j<=n;++j)
        dp[i*w+j]=(x[i-1]==y[j-1])?dp[(i-1)*w+j-1]+1:
            (dp[(i-1)*w+j]>=dp[i*w+j-1]?dp[(i-1)*w+j]:dp[i*w+j-1]);
    size_t len=dp[m*w+n];char *s=malloc(len+1);if(!s){free(dp);return false;}s[len]='\0';
    size_t i=m,j=n,k=len;
    while(i&&j){if(x[i-1]==y[j-1]){s[--k]=x[i-1];--i;--j;}
        else if(dp[(i-1)*w+j]>=dp[i*w+j-1])--i;else --j;}
    free(dp);*out=s;return true;
}
// snippet:lcs-bottom-up:end

int main(void) {
    const char *x = "ABCBDAB", *y = "BDCABA";
    char *s = NULL;
    lcs_bottom_up(x, y, &s);
    printf("X: %s\n", x);
    printf("Y: %s\n", y);
    printf("lcs: %s\n", s);
    printf("length: %zu\n", strlen(s));
    free(s);
    return 0;
}
