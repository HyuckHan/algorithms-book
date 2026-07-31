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
