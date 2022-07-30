# **********************************************************************************************************************
#
#                             Copyright (c) 2017-2021 David Briant. All rights reserved.
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


import builtins, numpy

from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from dm._core.structs import tvstruct, tvarray, tvseq
from dm._core.types import adhoc, agg, T, T1, T2, T3, T4, T5, T6, N, pylist, pydict, pyfunc, pydict_keys, \
    pydict_values, pyset, pytuple
from bones.lang.metatypes import hasT

function = type(lambda x:x)


# **********************************************************************************************************************
# both
# **********************************************************************************************************************

@coppertop(style=ternary)
def both(a:pylist, f:pyfunc, b:pylist) -> pylist:
    return [f(x, y) for (x, y) in builtins.zip(a, b)]

@coppertop(style=ternary)
def both(a:pydict, f:pyfunc, b:pydict) -> pylist:
    answer = []
    for (ak, av), (bk, bv) in zip((a.items(), b.items())):
        answer.append(f(ak, av, bk, bv))
    return answer

@coppertop(style=ternary)
def both(a:(T1 ** T2)[tvstruct], fn, b:(T1 ** T2)[tvstruct]) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a:tvstruct, fn, b:tvstruct) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a:(T1 ** T2)[tvstruct][T3], fn, b:(T1 ** T2)[tvstruct][T3]) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a:tvstruct, fn, b:tvstruct) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()

@coppertop(style=ternary)
def both(a:(T1 ** T2)[tvstruct][T3], fn:pyfunc, b:(T4 ** T5)[tvstruct][T6]) -> pylist:
    return a._kvs()  \
        >> both  \
        >> (lambda aFV, bFV: fn(aFV[0], aFV[1], bFV[0], bFV[1]))  \
        >> b._kvs()


# **********************************************************************************************************************
# buffer
# **********************************************************************************************************************

@coppertop
def buffer(iter) -> pytuple:
    return tuple(iter)


# **********************************************************************************************************************
# each
# **********************************************************************************************************************

@coppertop(style=binary2)
def each(xs:pylist+pydict_keys+pydict_values+pytuple, f) -> pylist:
    return [f(x) for x in xs]

@coppertop(style=binary2)
def each(xs:pyset, f) -> pyset:
    return set([f(x) for x in xs])

# @coppertop(style=binary2)
# def each(x:(N**T1)[tvseq], f, tByT) -> tvseq & T:
# # def each(x:(N**T1)[tvseq], f:T1^T2) -> (N**T2)[tvseq]:
#     result = x._v >> each >> f
#     t = typeOf(result[0])
#     return tvseq((N**t)[tvseq], result)

def _eachHelper(xs:(N**T1)[tvseq], f:T1^T2, tByT) -> dict:
    t1 = tByT[T1]
    d, tByT_f = selectDispatcher(f, (t1,))
    t2 = d.tRet
    if hasT(t2):
        raise NotYetImplemented()
    answer = dict(tByT)
    answer[T2] = t2
    return answer

@coppertop(style=binary2, typeHelper=_eachHelper)
def each(xs:(N**T1)[tvseq], f:T1^T2, tByT) -> (N**T2)[tvseq]:
    # fxs = []
    # for x in xs:
    #     y = f(x)
    #     fxs.append(y)
    # return fxs | (N**tByT[T2])[tvseq]
    return tvseq((N**tByT[T2])[tvseq], [f(x) for x in xs])

@coppertop(style=binary2, typeHelper=_eachHelper)
def each(xs:(N**T1)[tvseq, T3], f:T1^T2, tByT) -> (N**T2)[tvseq, T3]:
    fxs = [f(x) for x in xs]
    return tvseq((N**tByT[T2])[tvseq, tByT[T3]], fxs)

@coppertop(style=binary2)
def each(a:adhoc, fn2) -> adhoc:
    answer = adhoc()
    for f, v in a._kvs():
        answer[f] = fn2(f, v)
    return answer

@coppertop(style=binary2)
def eachV(a:adhoc, fn1) -> pylist:
    answer = list()
    for v in a._values():
        answer.append(fn1(v))
    return answer

@coppertop(style=binary2)
def each(a:agg, fn1):
    inputsAndOutput = [x for x in a._values()] + [None]
    with numpy.nditer(inputsAndOutput) as it:
        for vars in it:
            vars[-1][...] = fn1(*vars[:-1])
        return it.operands[len(inputsAndOutput) - 1].view(tvarray)


# **********************************************************************************************************************
# ieach
# **********************************************************************************************************************

@coppertop(style=binary2)
def ieach(xs:pylist, f2) -> pylist:
    return [f2(i, x) for (i, x) in enumerate(xs)]


# **********************************************************************************************************************
# inject
# **********************************************************************************************************************

@coppertop(style=binary)
def inject(xs:pylist, seed, f2):
    prior = seed
    for x in xs:
        prior = f2(prior, x)
    return prior

@coppertop(style=binary)
def inject(s:adhoc, seed, f3):
    prior = seed
    for f, v in s._kvs():
        prior = f3(prior, f, v)
    return prior


