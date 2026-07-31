#include "string_matching.h"
#include <stdio.h>
#include <string.h>

int main(void) {
    const unsigned char text[]="acebbceeaabceedb", pattern[]="eeaab";
    SmMatches out={0};
    if (!sm_rabin_karp_all(text,strlen((const char *)text),
                           pattern,strlen((const char *)pattern),5,113,&out)) return 1;
    printf("matches:");
    for (size_t i=0;i<out.count;i++) printf("%s%zu", i?",":" ", out.data[i]);
    putchar('\n');
    sm_matches_destroy(&out);
    return 0;
}
