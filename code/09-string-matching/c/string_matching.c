/* lecture-notes/code/lecture09/c/string_matching.c와 같은 정책(0-based, empty
 * pattern all-match [0], overflow-safe modular Rabin-Karp, standard LPS,
 * Horspool). */
#include "string_matching.h"
#include <stdlib.h>

void sm_matches_init(SmMatches *m) { if (m) *m = (SmMatches){0}; }
void sm_matches_destroy(SmMatches *m) {
    if (!m) return;
    free(m->data);
    *m = (SmMatches){0};
}

static bool append(SmMatches *out, size_t value) {
    if (out->count == out->capacity) {
        size_t next = out->capacity ? out->capacity * 2 : 8;
        if (next < out->capacity || next > SIZE_MAX / sizeof(*out->data)) return false;
        size_t *tmp = realloc(out->data, next * sizeof(*tmp));
        if (!tmp) return false;
        out->data = tmp; out->capacity = next;
    }
    out->data[out->count++] = value;
    return true;
}
static bool equal_at(const unsigned char *t, const unsigned char *p,
                     size_t s, size_t m) {
    for (size_t j = 0; j < m; j++) if (t[s+j] != p[j]) return false;
    return true;
}
static bool begin_output(SmMatches *out, size_t m) {
    out->count = 0;
    return m != 0 || append(out, 0); /* documented empty-pattern all-match policy */
}

// snippet:naive-match:start
bool sm_naive_all(const unsigned char *t, size_t n,
                  const unsigned char *p, size_t m, SmMatches *out) {
    if (!begin_output(out,m)) return false;
    if (m == 0 || m > n) return true;
    for (size_t s = 0; s <= n-m; s++) if (equal_at(t,p,s,m) && !append(out,s)) return false;
    return true;
}
// snippet:naive-match:end

static uint64_t add_mod(uint64_t a, uint64_t b, uint64_t q) {
    a %= q; b %= q;
    return a >= q-b ? a-(q-b) : a+b;
}
static uint64_t sub_mod(uint64_t a, uint64_t b, uint64_t q) {
    a %= q; b %= q;
    return a >= b ? a-b : q-(b-a);
}
static uint64_t mul_mod(uint64_t a, uint64_t b, uint64_t q) {
    uint64_t result = 0;
    a %= q; b %= q;
    while (b) {
        if (b & UINT64_C(1)) result = add_mod(result,a,q);
        a = add_mod(a,a,q);
        b >>= 1;
    }
    return result;
}

// snippet:rabin-karp:start
bool sm_rabin_karp_all(const unsigned char *t, size_t n,
                       const unsigned char *p, size_t m,
                       uint64_t base, uint64_t q, SmMatches *out) {
    if (!begin_output(out,m)) return false;
    if (m == 0 || m > n) return true;
    uint64_t h=1, ph=0, th=0;
    for (size_t j=1;j<m;j++) h=mul_mod(h,base,q);
    for (size_t j=0;j<m;j++) {
        ph=add_mod(mul_mod(ph,base,q),(uint64_t)p[j]+1,q);
        th=add_mod(mul_mod(th,base,q),(uint64_t)t[j]+1,q);
    }
    for (size_t s=0;s<=n-m;s++) {
        if (ph==th && equal_at(t,p,s,m) && !append(out,s)) return false;
        if (s<n-m) {
            uint64_t lead=mul_mod((uint64_t)t[s]+1,h,q);
            th=add_mod(mul_mod(base,sub_mod(th,lead,q),q),(uint64_t)t[s+m]+1,q);
        }
    }
    return true;
}
// snippet:rabin-karp:end

// snippet:kmp:start
bool sm_build_lps(const unsigned char *p, size_t m, size_t *lps) {
    if (m == 0) return true;
    lps[0]=0;
    for (size_t i=1,len=0;i<m;) {
        if (p[i]==p[len]) lps[i++]=++len;
        else if (len) len=lps[len-1];
        else lps[i++]=0;
    }
    return true;
}

bool sm_kmp_all(const unsigned char *t, size_t n,
                const unsigned char *p, size_t m, SmMatches *out) {
    if (!begin_output(out,m)) return false;
    if (m == 0 || m > n) return true;
    size_t *lps=malloc(m*sizeof(*lps));
    if (!lps || !sm_build_lps(p,m,lps)) { free(lps); return false; }
    size_t i=0,j=0;
    while (i<n) {
        if (t[i]==p[j]) {
            i++;j++;
            if (j==m) {
                if (!append(out,i-m)) { free(lps); return false; }
                j=lps[j-1];
            }
        } else if (j) j=lps[j-1];
        else i++;
    }
    free(lps); return true;
}
// snippet:kmp:end

// snippet:horspool:start
void sm_build_horspool_shift(const unsigned char *p, size_t m, size_t shift[256]) {
    size_t fallback=m ? m : 1;
    for (size_t c=0;c<256;c++) shift[c]=fallback;
    for (size_t j=0;j+1<m;j++) shift[p[j]]=m-1-j;
}

bool sm_horspool_all(const unsigned char *t, size_t n,
                     const unsigned char *p, size_t m, SmMatches *out) {
    if (!begin_output(out,m)) return false;
    if (m == 0 || m > n) return true;
    size_t shift[256]; sm_build_horspool_shift(p,m,shift);
    for (size_t s=0;s<=n-m;) {
        size_t j=m;
        while (j && p[j-1]==t[s+j-1]) j--;
        if (j==0 && !append(out,s)) return false;
        size_t step=shift[t[s+m-1]];
        if (step==0 || step>SIZE_MAX-s) break;
        s+=step;
    }
    return true;
}
// snippet:horspool:end
