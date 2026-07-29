import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

final class Fruit implements Comparable<Fruit> {
    final String name;
    final int quantity;

    Fruit(String name, int quantity) {
        this.name = name;
        this.quantity = quantity;
    }

    @Override
    public int compareTo(Fruit other) {
        return name.compareTo(other.name);
    }

    @Override
    public String toString() {
        return name + ":" + quantity;
    }
}

public class FruitSorting {
    static final Comparator<Fruit> BY_QUANTITY =
        Comparator.comparingInt((Fruit f) -> f.quantity);

    static final Comparator<Fruit> BY_QUANTITY_THEN_NAME =
        Comparator.comparingInt((Fruit f) -> f.quantity)
                  .thenComparing(f -> f.name);

    private static void require(boolean condition, String message) {
        if (!condition) throw new AssertionError(message);
    }

    public static void main(String[] args) {
        int[] extremes = {Integer.MAX_VALUE, 0, Integer.MIN_VALUE, 0};
        Arrays.sort(extremes);
        require(Arrays.equals(extremes,
            new int[] {Integer.MIN_VALUE, 0, 0, Integer.MAX_VALUE}),
            "primitive ascending order");

        Integer[] descending = {Integer.MIN_VALUE, 7, Integer.MAX_VALUE};
        Arrays.sort(descending, Comparator.reverseOrder());
        require(Arrays.equals(descending,
            new Integer[] {Integer.MAX_VALUE, 7, Integer.MIN_VALUE}),
            "descending order");

        Fruit[] fruits = {
            new Fruit("Pineapple", 70), new Fruit("Apple", 100),
            new Fruit("Orange", 80), new Fruit("Banana", 90),
            new Fruit("Apricot", 90), new Fruit("Apple", 100)
        };
        Arrays.sort(fruits, BY_QUANTITY_THEN_NAME);
        require(List.of(fruits).toString().equals(
            "[Pineapple:70, Orange:80, Apricot:90, Banana:90, Apple:100, Apple:100]"),
            "quantity/name multi-key order with duplicates");

        System.out.println("FruitSorting tests passed");
    }
}
