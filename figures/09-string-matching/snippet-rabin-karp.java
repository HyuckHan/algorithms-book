    public static List<Integer> rabinKarp(String text, String pattern, long base, long modulus) {
        int n = text.length(), m = pattern.length();
        if (m == 0) return List.of(0);
        if (m > n) return List.of();
        long h = 1, pHash = 0, tHash = 0;
        for (int j = 1; j < m; j++) h = mulMod(h, base, modulus);
        for (int j = 0; j < m; j++) {
            pHash = addMod(mulMod(pHash, base, modulus), code(pattern.charAt(j)), modulus);
            tHash = addMod(mulMod(tHash, base, modulus), code(text.charAt(j)), modulus);
        }
        List<Integer> out = new ArrayList<>();
        for (int s = 0; s + m <= n; s++) {
            if (pHash == tHash && equalsAt(text, pattern, s)) out.add(s);
            if (s + m < n) {
                long leading = mulMod(code(text.charAt(s)), h, modulus);
                long remainder = subMod(tHash, leading, modulus);
                tHash = addMod(mulMod(base, remainder, modulus), code(text.charAt(s + m)), modulus);
            }
        }
        return out;
    }
