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
