import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;

/** lecture-notes/code/lecture10/java/KnapsackBranchAndBound.java와 같은 정책
 * (profit/weight ratio 내림차순 정렬, fractional-relaxation upper bound,
 * best-first max-heap by bound). */
public final class KnapsackBranchAndBound {
    public static final class Item {
        public final String name;
        public final long weight;
        public final long profit;
        public Item(String name, long weight, long profit) {
            if (name == null || weight <= 0 || profit < 0) throw new IllegalArgumentException();
            this.name = name; this.weight = weight; this.profit = profit;
        }
    }
    public static final class Result {
        public long profit;
        public long weight;
        public List<String> selected = new ArrayList<>();
        public long expanded;
        public long pruned;
        public int maxFrontier;
    }
    private static final class Node {
        int level;
        long weight, profit;
        double bound;
        boolean[] selected;
    }

    // snippet:knapsack-bnb:start
    public Result solve(Item[] input, long capacity) {
        if (input == null || capacity < 0) throw new IllegalArgumentException();
        Item[] items = input.clone();
        Arrays.sort(items, (a, b) -> {
            int c = Long.compare(Math.multiplyExact(b.profit, a.weight),
                                 Math.multiplyExact(a.profit, b.weight));
            return c != 0 ? c : a.name.compareTo(b.name);
        });
        PriorityQueue<Node> pq = new PriorityQueue<>(Comparator.comparingDouble((Node n) -> n.bound).reversed());
        Node root = new Node();
        root.selected = new boolean[items.length];
        root.bound = bound(items, capacity, root.level, 0, 0);
        pq.add(root);
        Result result = new Result();
        while (!pq.isEmpty()) {
            result.maxFrontier = Math.max(result.maxFrontier, pq.size());
            Node node = pq.remove();
            if (node.bound <= result.profit) { result.pruned++; continue; }
            result.expanded++;
            if (node.level == items.length) continue;
            int i = node.level;
            if (node.weight <= capacity - items[i].weight) {
                Node take = child(node, true);
                take.weight = Math.addExact(node.weight, items[i].weight);
                take.profit = Math.addExact(node.profit, items[i].profit);
                if (take.profit > result.profit) save(result, take, items);
                take.bound = bound(items, capacity, take.level, take.weight, take.profit);
                if (take.bound > result.profit) pq.add(take); else result.pruned++;
            }
            Node skip = child(node, false);
            skip.bound = bound(items, capacity, skip.level, skip.weight, skip.profit);
            if (skip.bound > result.profit) pq.add(skip); else result.pruned++;
        }
        return result;
    }

    private static Node child(Node p, boolean take) {
        Node c = new Node();
        c.level = p.level + 1; c.weight = p.weight; c.profit = p.profit;
        c.selected = p.selected.clone(); c.selected[p.level] = take;
        return c;
    }

    public static double bound(Item[] items, long capacity, int level, long weight, long profit) {
        if (weight > capacity) return Double.NEGATIVE_INFINITY;
        double value = profit;
        long remaining = capacity - weight;
        for (int i = level; i < items.length && remaining > 0; i++) {
            if (items[i].weight <= remaining) {
                remaining -= items[i].weight;
                value += items[i].profit;
            } else {
                value += (double) items[i].profit * remaining / items[i].weight;
                break;
            }
        }
        return value;
    }
    // snippet:knapsack-bnb:end

    private static void save(Result r, Node n, Item[] items) {
        r.profit = n.profit; r.weight = n.weight; r.selected = new ArrayList<>();
        for (int i = 0; i < items.length; i++) if (n.selected[i]) r.selected.add(items[i].name);
    }
}
