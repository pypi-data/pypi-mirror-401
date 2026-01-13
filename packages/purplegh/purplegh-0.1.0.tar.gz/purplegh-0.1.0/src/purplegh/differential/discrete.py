def diff(t, x):
    # check that both lists have the same length
    if len(t) != len(x):
        print("Length MismatchO")
        return []

    n = len(t)
    v = []
    for i in range(n):
        v.append(0)

    for i in range(1, n):
        v[i] = (x[i] - x[i - 1]) / (t[i] - t[i - 1])

    return v
