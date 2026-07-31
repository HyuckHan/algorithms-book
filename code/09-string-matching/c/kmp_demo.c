#include "string_matching.h"
#include <stdio.h>
#include <string.h>

int main(void) {
    const unsigned char lps_pattern[]="BAABABAA";
    size_t m0 = strlen((const char *)lps_pattern);
    size_t lps[32];
    if (!sm_build_lps(lps_pattern,m0,lps)) return 1;
    printf("lps:");
    for (size_t i=0;i<m0;i++) printf("%s%zu", i?",":" ", lps[i]);
    putchar('\n');

    const unsigned char text[]="acebbceeaabceedb", pattern[]="eeaab";
    SmMatches out={0};
    if (!sm_kmp_all(text,strlen((const char *)text),
                    pattern,strlen((const char *)pattern),&out)) return 1;
    printf("matches:");
    for (size_t i=0;i<out.count;i++) printf("%s%zu", i?",":" ", out.data[i]);
    putchar('\n');
    sm_matches_destroy(&out);
    return 0;
}
