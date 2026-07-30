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
