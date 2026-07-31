    public static Map<Character,Integer> buildHorspoolShift(String pattern, int[] fallbackOut) {
        int m = pattern.length();
        fallbackOut[0] = Math.max(1, m);
        Map<Character,Integer> shift = new HashMap<>();
        for (int j = 0; j < m - 1; j++) shift.put(pattern.charAt(j), m - 1 - j);
        return shift;
    }

    public static List<Integer> horspoolSearch(String text, String pattern) {
        int n = text.length(), m = pattern.length();
        if (m == 0) return List.of(0);
        if (m > n) return List.of();
        int[] fallback = new int[1];
        Map<Character,Integer> shift = buildHorspoolShift(pattern, fallback);
        List<Integer> out = new ArrayList<>();
        for (int s = 0; s + m <= n;) {
            int j = m - 1;
            while (j >= 0 && pattern.charAt(j) == text.charAt(s + j)) j--;
            if (j < 0) out.add(s);
            s += shift.getOrDefault(text.charAt(s + m - 1), fallback[0]);
        }
        return out;
    }
