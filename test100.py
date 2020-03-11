a = [
    [1,2],
    [3,4],
    [5,6]
]

def f(l):
    out = []
    for x in l:
        out.append(x + 1)
    return out



b = zip(*a)

x = map(f, b)

k = zip(*x)

print(list(k))



