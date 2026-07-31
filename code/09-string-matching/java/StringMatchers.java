import java.util.*;

/** lecture-notes/code/lecture09/java/StringMatchers.java와 같은 정책(0-based,
 * empty pattern all-match [0], overflow-safe modular Rabin-Karp, standard LPS,
 * Horspool). */
public final class StringMatchers {
    // snippet:naive-match:start
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
    // snippet:naive-match:end

    private static long code(char c) { return (long) c + 1; }

    private static long addMod(long a, long b, long q) {
        a %= q; b %= q;
        return a >= q - b ? a - (q - b) : a + b;
    }
    private static long subMod(long a, long b, long q) {
        a %= q; b %= q;
        return a >= b ? a - b : q - (b - a);
    }
    private static long mulMod(long a, long b, long q) {
        a %= q; b %= q;
        long result = 0;
        while (b > 0) {
            if ((b & 1L) != 0) result = addMod(result, a, q);
            a = addMod(a, a, q);
            b >>>= 1;
        }
        return result;
    }
    private static boolean equalsAt(String text, String pattern, int s) {
        for (int j = 0; j < pattern.length(); j++)
            if (text.charAt(s + j) != pattern.charAt(j)) return false;
        return true;
    }

    // snippet:rabin-karp:start
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
    // snippet:rabin-karp:end

    // snippet:kmp:start
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
    // snippet:kmp:end

    // snippet:horspool:start
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
    // snippet:horspool:end

    private StringMatchers() {}
}
