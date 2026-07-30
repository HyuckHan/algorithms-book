#include <stdio.h>

// snippet:hanoi:start
/* Hanoi. Base case: n == 0 (no disks, 0 moves, no further call). Recursive
 * case: move n-1 disks out of the way (from->via), move disk n
 * (from->to), then move those n-1 disks onto it (via->to) -- matching
 * T(n) = 2*T(n-1) + 1, T(0) = 0. Max call-stack depth is n (one frame per
 * disk count from n down to 1). Returns the total move count so the
 * caller can check it against 2^n - 1. */
static int hanoi(int n, char from, char to, char via) {
    if (n == 0) return 0;
    int moves = hanoi(n - 1, from, via, to);
    printf("move disk %d: %c -> %c\n", n, from, to);
    moves++;
    moves += hanoi(n - 1, via, to, from);
    return moves;
}
// snippet:hanoi:end

int main(void) {
    int n = 3;
    printf("input: n=%d\n", n);
    int total = hanoi(n, 'L', 'R', 'M');
    printf("hanoi: %d\n", total);
    return 0;
}
