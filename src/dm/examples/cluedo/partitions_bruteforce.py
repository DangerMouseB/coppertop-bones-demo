# we can use permutaion code and filter for only groups in order - profoundly slow but okay to test small handSizes

@coppertop
def handCombinations(cards, handSizes):
    slices = []
    s1 = 0
    for handSize in handSizes:
        s2 = s1 + handSize
        slices.append((s1, s2))
        s1 = s2
    perms = filter(
        lambda perm: groupsInOrder(perm, slices),
        itertools.permutations(cards, cards >> count)
    )
    return perms

def groupsInOrder(xs, slices):
    for s1, s2 in slices:
        if not isAsc(xs[s1:s2]): return False
    return True

def isAsc(xs):
    p = xs[0]
    for n in xs[1:]:
        if n <= p: return False
        p = n
    return True
