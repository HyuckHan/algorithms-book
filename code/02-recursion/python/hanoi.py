"""Hanoi."""

# snippet:hanoi:start
def hanoi(n, frm, to, via):
    # Base case: n == 0 (no disks, 0 moves, no further call). Recursive
    # case: move n-1 disks out of the way (frm->via), move disk n
    # (frm->to), then move those n-1 disks onto it (via->to) -- matching
    # T(n) = 2*T(n-1) + 1, T(0) = 0. Max call-stack depth is n (one frame
    # per disk count from n down to 1). Returns the total move count so the
    # caller can check it against 2**n - 1.
    if n == 0:
        return 0
    moves = hanoi(n - 1, frm, via, to)
    print("move disk %d: %s -> %s" % (n, frm, to))
    moves += 1
    moves += hanoi(n - 1, via, to, frm)
    return moves
# snippet:hanoi:end

if __name__ == "__main__":
    n = 3
    print("input: n=%d" % n)
    total = hanoi(n, "L", "R", "M")
    print("hanoi:", total)
