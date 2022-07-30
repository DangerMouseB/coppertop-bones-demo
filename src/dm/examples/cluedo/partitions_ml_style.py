

# partitions :: [Int] -> [[[Int]]]
def partitions(sizes):
    '''Ordered partitions of sizes.'''
    n = sum(sizes)
    xs = enumFromTo(1)(n)

    def go(xs, n, sizes):
        return [
            [l] + r
            for (l, rest) in choose(xs)(n)(sizes[0])
            for r in go(rest, n - sizes[0], sizes[1:])
        ] if sizes else [[]]

    return go(xs, n, sizes)


# choose :: [Int] -> Int -> Int -> [([Int], [Int])]
def choose(xs):
    '''(m items chosen from n items, the rest)'''

    def go(xs, n, m):
        f = cons(xs[0])
        choice = choose(xs[1:])(n - 1)
        return [([], xs)] if 0 == m else (
            [(xs, [])] if n == m else (
                    [first(f)(xy) for xy in choice(m - 1)] +
                    [second(f)(xy) for xy in choice(m)]
            )
        )

    return lambda n: lambda m: go(xs, n, m)


# cons :: a -> [a] -> [a]
def cons(x):
    '''Construction of a list from x as head, and xs as tail.'''
    return lambda xs: [x] + xs


# enumFromTo :: Int -> Int -> [Int]
def enumFromTo(m):
    '''Integer enumeration from m to n.'''
    return lambda n: list(range(m, 1 + n))


# first :: (a -> b) -> ((a, c) -> (b, c))
def first(f):
    '''A simple function lifted to a function over a tuple, with f applied only the first of two values.'''
    return lambda xy: (f(xy[0]), xy[1])


# second :: (a -> b) -> ((c, a) -> (c, b))
def second(f):
    '''A simple function lifted to a function over a tuple, with f applied only the second of two values.'''
    return lambda xy: (xy[0], f(xy[1]))


# %timeit partitions([5,4,4]) >> count
# 380 ms ± 2.09 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)