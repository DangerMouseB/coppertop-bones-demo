# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
#
# BSD 3-Clause License
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
#    following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
#    following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
#    products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# **********************************************************************************************************************

from coppertop.pipe import *
from bones.lang.metatypes import BTPrimitive
from dm.core.types import txt, N, index, pylist, pyset, pydict_keys, pydict_values, T1, T2, pytuple, tv, pyfunc,\
    T, N2
from dm.core import count, equal, tvseq, each, max, pad, PP as _PP, format, check, nCombinations, sum
from dm.utils import formatStruct
from dm.pmf import PMF, L

from dm.core.types import void


display_table = (N**txt)[tvseq][BTPrimitive.ensure('table')].setCoercer(tvseq)

@coppertop
def PP(t:display_table) -> display_table:
    for string in t:
        string >> _PP
    return t

@coppertop(style=binary)
def hjoin(a:display_table, b:display_table, options={}) -> display_table:
    assert (a >> count) == (b >> count)
    answer = tvseq(display_table, [])
    for i in range(len(a)):
        answer.append(a[i] + options.get('sep', '') + b[i])
    return answer

@coppertop(style=binary)
def join(a:display_table, b:display_table, options={}) -> display_table:
    return tvseq(display_table, a.data + b.data) >> ljust

@coppertop
def ljust(rows:display_table, width:index=0, fillchar:txt=' ') -> display_table:
    maxLength = rows >> each >> count >> max
    return rows >> each >> pad(_, left=max((maxLength, width)), pad=fillchar) | display_table

@coppertop(style=binary2)
def aside(x:T1, fn:T1^T2) -> T1:
    fn(x)
    return x

@coppertop(style=binary2)
def aside(x:pylist, fn) -> pylist:
    fn(x)
    return x

@coppertop(style=binary2)
def countIf(xs, fn):
    c = 0
    for x in xs:
        c += fn(x)
    return c

@coppertop(style=binary2)
def minus(a:pyset, b:pyset+pylist+pydict_keys+pydict_values) -> pyset:
    return a.difference(b)

@coppertop(style=binary2)
def minus(a:pylist+pytuple, b:pyset+pylist+pydict_keys+pydict_values) -> pyset:
    return set(a).difference(b)

@coppertop
def only(a:pyset):
    return list(a)[0]

@coppertop(style=binary2)
def append(rows:display_table, row:txt) -> display_table:
    rows.append(row)
    return rows >> ljust

formatPmf = formatStruct(_, 'PMF', '.3f', '.3f', ', ')
formatL = formatStruct(_, 'L', '.3f', '.3f', ', ')

@coppertop
def PP(x, f:pyfunc):
    f(x) >> _PP
    return x

@coppertop
def PP(x, fmt:txt):
    x >> format(_, fmt) >> _PP
    return x

@coppertop
def PP(x:L):
    x >> formatL >> _PP
    return x

@coppertop
def PP(x:PMF):
    x >> formatPmf >> _PP
    return x

@coppertop
def nHandCombinations(handSizes):
    nCards = handSizes >> sum
    total = 1
    for hs in handSizes:
        total = total * (nCards >> nCombinations >> hs)
        nCards -= hs
    return total

@coppertop(style=binary)
def partitions(xs:pylist+pytuple, sizes:pylist+pytuple) -> N**N**N**T:
# def partitions(xs:N**T, sizes:N**index) -> N**N**N**T:
    sizes >> sum >> check >> equal >> (xs >> count)
    return _partitions(list(xs), xs >> count, sizes)

def _partitions(xs:N**T, n:index, sizes:N**index) -> N**N**N**T:
    if sizes:
        answer = []
        for comb, rest in _combRest(xs, n, sizes[0]):
            for partitions in _partitions(rest, n - sizes[0], sizes[1:]):
                answer.append([comb] + partitions)
        return answer
    else:
        return [[]]

def _combRest(xs:N**T, n:index, m:index) -> N**( (N**T)*(N**T) ):
    '''answer [m items chosen from n items, the rest]'''
    if m == 0:
        return [([], xs)]
    elif m == n:
        return [(xs, [])]
    else:
        firstPart = [ (xs[0:1] + x, y) for x, y in _combRest(xs[1:], n - 1, m - 1)]
        secondPart = [ (x, xs[0:1] + y) for x, y in _combRest(xs[1:], n - 1, m)]
        return firstPart + secondPart

# %timeit partitions_(range(13), [5,4,4]) >> count >> PP
# 166 ms ± 2.01 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


