from state_space_search import knapsack_bnb

if __name__ == "__main__":
    # A, B, C, D with (weight, profit); W=16 -- the lecture's own running example.
    items = [(2, 40), (5, 30), (10, 50), (5, 10)]
    profit, weight = knapsack_bnb(items, 16)
    print("profit:", profit)
    print("weight:", weight)
