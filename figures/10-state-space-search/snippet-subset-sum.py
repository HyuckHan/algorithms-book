def subset_sum(weights, target):
    n = len(weights)
    remaining_total = sum(weights)
    result = []

    def recurse(i, current_sum, remaining, selected):
        if current_sum == target:
            result.append(tuple(selected))
            return
        if i == n or current_sum > target or current_sum + remaining < target:
            return
        selected.append(i)
        recurse(i + 1, current_sum + weights[i], remaining - weights[i], selected)
        selected.pop()
        recurse(i + 1, current_sum, remaining - weights[i], selected)

    recurse(0, 0, remaining_total, [])
    return result
