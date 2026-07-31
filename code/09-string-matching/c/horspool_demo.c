#include "string_matching.h"
#include <stdio.h>
#include <string.h>

int main(void) {
    const unsigned char tiger[]="TIGER", rational[]="RATIONAL";
    size_t tiger_shift[256], rational_shift[256];
    sm_build_horspool_shift(tiger,strlen((const char *)tiger),tiger_shift);
    sm_build_horspool_shift(rational,strlen((const char *)rational),rational_shift);
    printf("shift_I: %zu\n", tiger_shift[(unsigned char)'I']);
    printf("shift_A: %zu\n", rational_shift[(unsigned char)'A']);

    const unsigned char text[]="acebbceeaabceedb", pattern[]="eeaab";
    SmMatches out={0};
    if (!sm_horspool_all(text,strlen((const char *)text),
                         pattern,strlen((const char *)pattern),&out)) return 1;
    printf("matches:");
    for (size_t i=0;i<out.count;i++) printf("%s%zu", i?",":" ", out.data[i]);
    putchar('\n');
    sm_matches_destroy(&out);
    return 0;
}
