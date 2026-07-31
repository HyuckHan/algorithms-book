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
