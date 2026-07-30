#include <stdio.h>
#include <string.h>

/* StringHash: Horner's rule 다항식 문자열 해시. hash = hash*B + code(c)를
 * 왼쪽에서 오른쪽으로 누적한다(lecture-notes/lecture07/sections/04_string_hashing.tex). */

// snippet:string-hash:start
static long ascii_sum(const char *s) {
    long sum = 0;
    for (size_t i = 0; s[i] != '\0'; i++) sum += (unsigned char)s[i];
    return sum;
}

static long long string_hash(const char *s, long long base) {
    long long hash = 0;
    for (size_t i = 0; s[i] != '\0'; i++) hash = hash * base + (unsigned char)s[i];
    return hash;
}
// snippet:string-hash:end

int main(void) {
    printf("ascii_sum(abcd): %ld\n", ascii_sum("abcd"));
    printf("ascii_sum(dbac): %ld\n", ascii_sum("dbac"));
    printf("string_hash(abcd): %lld\n", string_hash("abcd", 131));
    printf("string_hash(dbac): %lld\n", string_hash("dbac", 131));
    printf("string_hash(Apple): %lld\n", string_hash("Apple", 131));
    printf("string_hash(Apply): %lld\n", string_hash("Apply", 131));
    return 0;
}
