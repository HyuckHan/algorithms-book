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
