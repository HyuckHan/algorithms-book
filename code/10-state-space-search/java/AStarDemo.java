public final class AStarDemo {
    public static void main(String[] args) {
        // 5x7 grid, obstacles, S at (0,0), G at (4,6) -- the lecture's own example.
        boolean[][] blocked = new boolean[5][7];
        int[][] obstacles = {{0,3},{1,3},{2,1},{2,2},{2,3},{3,5}};
        for (int[] o : obstacles) blocked[o[0]][o[1]] = true;
        AStarGrid solver = new AStarGrid();
        AStarGrid.Result result = solver.search(blocked, 0, 0, 4, 6, false);
        System.out.println("cost: " + result.cost);
        AStarGrid.Result dijkstra = solver.search(blocked, 0, 0, 4, 6, true);
        System.out.println("dijkstra_cost: " + dijkstra.cost);
    }
}
