#ifndef STATE_SPACE_SEARCH_H
#define STATE_SPACE_SEARCH_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

typedef enum {
    SS_OK = 0,
    SS_INVALID = 1,
    SS_OVERFLOW = 2,
    SS_NO_MEMORY = 3,
    SS_NO_SOLUTION = 4
} ss_status;

typedef struct {
    uint64_t expanded;
    uint64_t pruned;
    size_t max_depth;
    size_t max_frontier;
} ss_metrics;

typedef struct {
    int64_t weight;
    int64_t profit;
} ss_item;

typedef struct {
    int64_t weight;
    int64_t profit;
    uint64_t selected_mask;
    ss_metrics metrics;
} ss_knapsack_result;

ss_status ss_permutation_count(size_t n, size_t k, uint64_t *count,
                               ss_metrics *metrics);
/* New in this book's port (no lecture-notes/code/lecture10/c equivalent --
 * the original C file only ports ChoosePermutation, not ChooseCombination). */
ss_status ss_combination_count(size_t n, size_t k, uint64_t *count,
                               ss_metrics *metrics);
ss_status ss_n_queens_count(size_t n, uint64_t *count, ss_metrics *metrics);
ss_status ss_subset_sum_masks(const int64_t *weights, size_t n, int64_t target,
                              uint64_t *masks, size_t capacity,
                              size_t *solution_count, bool pruning,
                              ss_metrics *metrics);
/* New in this book's port (no lecture-notes/code/lecture10/c equivalent --
 * graph coloring has no C source at all).
 * adjacency is a row-major n*n 0/1 matrix. colors[n] is filled 1..m on
 * success (0-based vertex index -> color). */
ss_status ss_color_graph(const unsigned char *adjacency, size_t n, int m,
                         int *colors);
ss_status ss_knapsack_bnb(const ss_item *items, size_t n, int64_t capacity,
                          ss_knapsack_result *result);
ss_status ss_astar_grid(const unsigned char *blocked, size_t rows, size_t cols,
                        size_t start, size_t goal, bool zero_heuristic,
                        int64_t *cost, ss_metrics *metrics);

#endif
