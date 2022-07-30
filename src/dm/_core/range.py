# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2020 David Briant. All rights reserved.
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

from __future__ import annotations

BONES_MODULE = 'dm.core.range'

import sys, types

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from dm._core._irange import IInputRange, IRandomAccessInfinite
from dm._core._range import EachFR, ChainAsSingleFR, UntilFR, FileLineIR, ListOR, toIndexableFR, \
    ChunkUsingSubRangeGeneratorFR, RaggedZipIR, FnAdapterFR, ChunkFROnChangeOf, EMPTY

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - imports done')


@coppertop
def rZip(r):
    raise NotYetImplemented()

@coppertop
def rInject(r, seed, f):
    raise NotYetImplemented()

@coppertop
def rFilter(r, f):
    raise NotYetImplemented()

@coppertop
def rTakeBack(r, n):
    raise NotYetImplemented()

@coppertop
def rDropBack(r, n):
    raise NotYetImplemented()

@coppertop
def rFind(r, value):
    while not r.empty:
        if r.front == value:
            break
        r.popFront()
    return r

@coppertop
def put(r, x):
    return r.put(x)

@coppertop(style=unary1)
def front(r):
    return r.front

@coppertop(style=unary1)
def back(r):
    return r.back

@coppertop(style=unary1)
def empty(r):
    return r.empty

@coppertop(style=unary1)
def popFront(r):
    r.popFront()
    return r

@coppertop(style=unary1)
def popBack(r):
    r.popBack()
    return r


each_ = coppertop(style=binary2, newName='each_')(EachFR)
rChain = coppertop(style=unary1, newName='rChain')(ChainAsSingleFR)
rUntil = coppertop(style=binary2, newName='rUntil')(UntilFR)


@coppertop(style=unary1)
def fileLineIR(f):
    return FileLineIR(f)

@coppertop(style=unary1)
def listOR(l):
    return ListOR(l)

@coppertop
def chunkUsingSubRangeGeneratorFR(r, f):
    return ChunkUsingSubRangeGeneratorFR(r, f)

@coppertop(style=unary1)
def raggedZipIR(r):
    return RaggedZipIR(r)

@coppertop(style=unary1)
def fnAdapterFR(r):
    return FnAdapterFR(r)

@coppertop
def chunkFROnChangeOf(r, f):
    return ChunkFROnChangeOf(r, f)

@coppertop(style=unary1)
def fnAdapterEager(f):
    answer = []
    i = 0
    while (x := f(i)) != EMPTY:
        answer.append(x)
        i += 1
    return answer

@coppertop
def replaceWith(haystack, needle, replacement):
    return haystack >> each_ >> (lambda e: replacement if e == needle else e)

@coppertop(style=binary2)
def pushAllTo(inR, outR):
    while not inR.empty:
        outR.put(inR.front)
        inR.popFront()
    return outR

def _materialise(r):
    answer = list()
    while not r.empty:
        e = r.front
        if isinstance(e, IInputRange) and not isinstance(e, IRandomAccessInfinite):
            answer.append(_materialise(e))
            if not r.empty:  # the sub range may exhaust this range
                r.popFront()
        else:
            answer.append(e)
            r.popFront()
    return answer

materialise = coppertop(style=unary1, newName='materialise')(_materialise)


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
