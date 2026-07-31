def choose_permutation(n, k):
    result = []
    used = [False] * n
    choice = [0] * k

    def recurse(depth):
        if depth == k:
            result.append(tuple(choice))
            return
        for value in range(n):
            if not used[value]:
                used[value] = True
                choice[depth] = value
                recurse(depth + 1)
                used[value] = False

    recurse(0)
    return result


def choose_combination(n, k):
    result = []
    choice = [0] * k

    def recurse(start, depth):
        if depth == k:
            result.append(tuple(choice))
            return
        for value in range(start, n - (k - depth) + 1):
            choice[depth] = value
            recurse(value + 1, depth + 1)

    recurse(0, 0)
    return result
