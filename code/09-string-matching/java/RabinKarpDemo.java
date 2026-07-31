import java.util.List;
import java.util.stream.Collectors;

public final class RabinKarpDemo {
    public static void main(String[] args) {
        String text = "acebbceeaabceedb", pattern = "eeaab";
        List<Integer> matches = StringMatchers.rabinKarp(text, pattern, 5, 113);
        System.out.println("matches: " + matches.stream().map(String::valueOf).collect(Collectors.joining(",")));
    }
}
