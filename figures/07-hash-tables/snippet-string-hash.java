    public static int asciiSum(String s) {
        int sum = 0;
        for (int i = 0; i < s.length(); i++) sum += s.charAt(i);
        return sum;
    }

    public static long stringHash(String s, int base) {
        long hash = 0;
        for (int i = 0; i < s.length(); i++) hash = hash * base + s.charAt(i);
        return hash;
    }
