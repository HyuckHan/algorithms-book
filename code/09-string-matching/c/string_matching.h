#ifndef LECTURE09_STRING_MATCHING_H
#define LECTURE09_STRING_MATCHING_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef struct {
    size_t *data;
    size_t count;
    size_t capacity;
} SmMatches;

void sm_matches_init(SmMatches *matches);
void sm_matches_destroy(SmMatches *matches);

bool sm_naive_all(const unsigned char *text, size_t n,
                  const unsigned char *pattern, size_t m, SmMatches *out);
bool sm_rabin_karp_all(const unsigned char *text, size_t n,
                       const unsigned char *pattern, size_t m,
                       uint64_t base, uint64_t modulus, SmMatches *out);
bool sm_build_lps(const unsigned char *pattern, size_t m, size_t *lps);
bool sm_kmp_all(const unsigned char *text, size_t n,
                const unsigned char *pattern, size_t m, SmMatches *out);
void sm_build_horspool_shift(const unsigned char *pattern, size_t m,
                             size_t shift[256]);
bool sm_horspool_all(const unsigned char *text, size_t n,
                     const unsigned char *pattern, size_t m, SmMatches *out);

#endif
