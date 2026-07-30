/** StringHash: Horner's rule 다항식 문자열 해시. hash = hash*B + code(c)를
 * 왼쪽에서 오른쪽으로 누적한다(lecture-notes/lecture07/sections/04_string_hashing.tex). */
public final class StringHash {
    // snippet:string-hash:start
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
    // snippet:string-hash:end

    public static void main(String[] args) {
        System.out.println("ascii_sum(abcd): " + asciiSum("abcd"));
        System.out.println("ascii_sum(dbac): " + asciiSum("dbac"));
        System.out.println("string_hash(abcd): " + stringHash("abcd", 131));
        System.out.println("string_hash(dbac): " + stringHash("dbac", 131));
        System.out.println("string_hash(Apple): " + stringHash("Apple", 131));
        System.out.println("string_hash(Apply): " + stringHash("Apply", 131));
    }
}
