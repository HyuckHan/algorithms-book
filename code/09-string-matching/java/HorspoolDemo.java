import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public final class HorspoolDemo {
    public static void main(String[] args) {
        int[] fallback = new int[1];
        Map<Character,Integer> tigerShift = StringMatchers.buildHorspoolShift("TIGER", fallback);
        Map<Character,Integer> rationalShift = StringMatchers.buildHorspoolShift("RATIONAL", fallback);
        System.out.println("shift_I: " + tigerShift.get('I'));
        System.out.println("shift_A: " + rationalShift.get('A'));
        String text = "acebbceeaabceedb", pattern = "eeaab";
        List<Integer> matches = StringMatchers.horspoolSearch(text, pattern);
        System.out.println("matches: " + matches.stream().map(String::valueOf).collect(Collectors.joining(",")));
    }
}
