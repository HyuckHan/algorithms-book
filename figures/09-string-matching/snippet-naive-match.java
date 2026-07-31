    public static List<Integer> naiveAll(String text, String pattern) {
        int n = text.length(), m = pattern.length();
        if (m == 0) return List.of(0);
        List<Integer> out = new ArrayList<>();
        for (int s = 0; s + m <= n; s++) {
            int j = 0;
            while (j < m && text.charAt(s + j) == pattern.charAt(j)) j++;
            if (j == m) out.add(s);
        }
        return out;
    }
