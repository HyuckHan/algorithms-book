bool sm_naive_all(const unsigned char *t, size_t n,
                  const unsigned char *p, size_t m, SmMatches *out) {
    if (!begin_output(out,m)) return false;
    if (m == 0 || m > n) return true;
    for (size_t s = 0; s <= n-m; s++) if (equal_at(t,p,s,m) && !append(out,s)) return false;
    return true;
}
