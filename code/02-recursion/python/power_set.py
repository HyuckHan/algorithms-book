"""Power Set."""

DATA = ["a", "b", "c"]

# snippet:power-set:start
def power_set(k, n, include):
    # Base case: k == n (all n elements decided; prints the current
    # selection, including the empty set). Recursive case: exclude
    # data[k] first, then include it -- this exclude-before-include
    # order at every level makes the printed order match the
    # state-space tree's left-to-right leaf order exactly (see
    # 13-power-set-tree). Progress measure: k -> k+1. Max call-stack
    # depth is n. `include` is caller-owned (no module-level/global
    # state), threaded through by parameter.
    if k == n:
        selected = [DATA[i] for i in range(n) if include[i]]
        print("{%s}" % ",".join(selected))
        return
    include[k] = False
    power_set(k + 1, n, include)
    include[k] = True
    power_set(k + 1, n, include)
# snippet:power-set:end

if __name__ == "__main__":
    n = len(DATA)
    print("input: {a,b,c}")
    power_set(0, n, [False] * n)
