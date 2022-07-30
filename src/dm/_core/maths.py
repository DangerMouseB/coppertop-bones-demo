# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2020 David Briant. All rights reserved.
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

BONES_MODULE = 'dm.core'

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)


_EPS = 7.105427357601E-15      # i.e. double precision


import builtins, numpy, math

from bones.core.errors import NotYetImplemented
from coppertop.pipe import *
from dm._core.types import T1, T2, pylist, N, num
from dm._core.transforming import buffer

import itertools, scipy



# **********************************************************************************************************************
# permutations (arrangements) and combinations
# perms and combs are such useful variable names so use fuller name in fn
# **********************************************************************************************************************

@coppertop(style=binary)
def permutations(xs, k):
    return itertools.permutations(xs, k) >> buffer

@coppertop(style=binary)
def nPermutations(n, k):
    return math.perm(n, k)

@coppertop(style=binary)
def permutationsR(xs, k):
    return itertools.product(*([xs]*k)) >> buffer

@coppertop(style=binary)
def nPermutationsR(n, k):
    return n ** k

@coppertop(style=binary)
def combinations(xs, k):
    return itertools.combinations(xs, k) >> buffer

@coppertop(style=binary)
def nCombinations(n, k):
    return math.comb(n, k)

@coppertop(style=binary)
def combinationsR(xs, k):
    return itertools.combinations_with_replacement(xs, k) >> buffer

@coppertop(style=binary)
def nCombinationsR(n, k):
    return scipy.special.comb(n, k, exact=True)


# **********************************************************************************************************************
# comparison
# **********************************************************************************************************************

@coppertop(style=binary)
def closeTo(a, b):
    if abs(a) < _EPS:
        return abs(b) < _EPS
    else:
        return abs(a - b) / abs(a) < _EPS

@coppertop(style=binary)
def closeTo(a, b, tolerance):
    if abs(a) < tolerance:
        return abs(b) < tolerance
    else:
        return abs(a - b) / abs(a) < tolerance

@coppertop
def within(x, a, b):
    # answers true if x is in the closed interval [a, b]
    return (a <= x) and (x <= b)


# **********************************************************************************************************************
# functions
# **********************************************************************************************************************

@coppertop
def sqrt(x):
    return numpy.sqrt(x)   # answers a nan rather than throwing


# **********************************************************************************************************************
# stats
# **********************************************************************************************************************

@coppertop(style=unary1)
def min(x):
    return builtins.min(x)

@coppertop(style=unary1)
def max(x):
    return builtins.max(x)

@coppertop(style=unary1)
def sum(x):
    return builtins.sum(x)

@coppertop(style=unary1)
def sum(x:(N**T1)[pylist][T2]) -> num:
    return builtins.sum(x._v)

@coppertop(style=unary1)
def sum(x:(N**T1)[pylist]) -> num:
    return builtins.sum(x._v)


# **********************************************************************************************************************
# rounding
# **********************************************************************************************************************

@coppertop(style=unary1)
def roundDown(x):
    # i.e. [roundDown(-2.9), roundDown(2.9,0)] == [-3, 2]
    return math.floor(x)

@coppertop(style=unary1)
def roundUp(x):
    # i.e. [roundUp(-2.9), roundUp(2.9,0)] == [-2, 3]
    return math.ceil(x)

@coppertop(style=unary1)
def roundHalfToZero(x):
    # i.e. [round(-2.5,0), round(2.5,0)] == [-2.0, 2.0]
    return round(x)

@coppertop(style=unary1)
def roundHalfFromZero(x):
    raise NotYetImplemented()

@coppertop(style=unary1)
def roundHalfToNeg(x):
    raise NotYetImplemented()

@coppertop(style=unary1)
def roundHalfToPos(x):
    raise NotYetImplemented()


