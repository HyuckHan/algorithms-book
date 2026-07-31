from state_space_search import color_graph

if __name__ == "__main__":
    # A-B-C-D-A cycle plus A-C diagonal, matching the lecture's own example.
    adjacency = [
        [0, 1, 1, 1],  # A: B, C, D
        [1, 0, 1, 0],  # B: A, C
        [1, 1, 0, 1],  # C: A, B, D
        [1, 0, 1, 0],  # D: A, C
    ]
    colors = color_graph(adjacency, 3)
    print("colors:", ",".join(str(c) for c in colors))
