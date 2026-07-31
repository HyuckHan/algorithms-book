import java.util.List;
import java.util.stream.Collectors;

public final class NaiveMatchDemo {
    public static void main(String[] args) {
        String text = "acebbceeaabceedb", pattern = "eeaab";
        List<Integer> matches = StringMatchers.naiveAll(text, pattern);
        System.out.println("matches: " + matches.stream().map(String::valueOf).collect(Collectors.joining(",")));
    }
}
