    public static int[] buildLps(String pattern) {
        int m = pattern.length();
        int[] lps = new int[m];
        for (int i = 1, len = 0; i < m;) {
            if (pattern.charAt(i) == pattern.charAt(len)) lps[i++] = ++len;
            else if (len > 0) len = lps[len - 1];
            else lps[i++] = 0;
        }
        return lps;
    }

    public static List<Integer> kmpSearch(String text, String pattern) {
        int n = text.length(), m = pattern.length();
        if (m == 0) return List.of(0);
        int[] lps = buildLps(pattern);
        List<Integer> out = new ArrayList<>();
        for (int i = 0, j = 0; i < n;) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++; j++;
                if (j == m) {
                    out.add(i - m);
                    j = lps[j - 1];
                }
            } else if (j > 0) j = lps[j - 1];
            else i++;
        }
        return out;
    }
