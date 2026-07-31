from state_space_search import choose_permutation, choose_combination

if __name__ == "__main__":
    perms = choose_permutation(5, 4)
    combos = choose_combination(5, 4)
    print("P(5,4):", len(perms))
    print("C(5,4):", len(combos))
