import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public final class KmpDemo {
    public static void main(String[] args) {
        int[] lps = StringMatchers.buildLps("BAABABAA");
        System.out.println("lps: " + Arrays.stream(lps).mapToObj(String::valueOf).collect(Collectors.joining(",")));
        String text = "acebbceeaabceedb", pattern = "eeaab";
        List<Integer> matches = StringMatchers.kmpSearch(text, pattern);
        System.out.println("matches: " + matches.stream().map(String::valueOf).collect(Collectors.joining(",")));
    }
}
