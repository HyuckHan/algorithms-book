#include "string_matching.h"
#include <stdio.h>
#include <string.h>

int main(void) {
    const unsigned char text[]="acebbceeaabceedb", pattern[]="eeaab";
    SmMatches out={0};
    if (!sm_naive_all(text,strlen((const char *)text),
                       pattern,strlen((const char *)pattern),&out)) return 1;
    printf("matches:");
    for (size_t i=0;i<out.count;i++) printf("%s%zu", i?",":" ", out.data[i]);
    putchar('\n');
    sm_matches_destroy(&out);
    return 0;
}
