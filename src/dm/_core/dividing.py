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


import itertools, builtins

from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from dm._core.structs import tvstruct
from dm._core.types import T1, T2, T3, pylist, pydict, pydict_values, pydict_keys, pytuple, adhoc, agg



# **********************************************************************************************************************
# chunkBy
# **********************************************************************************************************************

@coppertop
def chunkBy(a:agg, keys):
    "answers a range of range of row"
    raise NotYetImplemented()


# **********************************************************************************************************************
# chunkUsing
# **********************************************************************************************************************

@coppertop(style=binary2)
def chunkUsing(iter, fn2):
    answer = []
    i0 = 0
    for i1, (a, b) in enumerate(_pairwise(iter)):
        if not fn2(a, b):
            answer += [iter[i0:i1+1]]
            i0 = i1 + 1
    answer += [iter[i0:]]
    return answer
def _pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return builtins.zip(a, b)


# **********************************************************************************************************************
# select and reject - https://en.wikipedia.org/wiki/Filter_(higher-order_function)
# **********************************************************************************************************************

@coppertop(style=binary2)
def select(d:pydict, f2) -> pydict:
    filteredKVs = []
    for k, v in d.items():
        if f2(k, v): filteredKVs.append((k,v))
    return dict(filteredKVs)

@coppertop(style=binary2)
def select(d:adhoc, f2) -> adhoc:
    filteredKVs = []
    for k, v in d._kvs():
        if f2(k, v): filteredKVs.append((k,v))
    return adhoc(filteredKVs)

@coppertop(style=binary2)
def select(pm:tvstruct, f2) -> tvstruct:
    filteredKVs = []
    for k, v in pm._kvs():
        if f2(k, v): filteredKVs.append((k,v))
    return tvstruct(pm._t, filteredKVs)

@coppertop(style=binary2)
def select(pm:(T1**T2)[tvstruct], f2) -> (T1**T2)[tvstruct]:
    filteredKVs = []
    for k, v in pm._kvs():
        if f2(k, v): filteredKVs.append((k,v))
    return tvstruct(pm._t, filteredKVs)

@coppertop(style=binary2)
def select(pm:(T1**T2)[tvstruct][T3], f2) -> (T1**T2)[tvstruct][T3]:
    filteredKVs = []
    for k, v in pm._v._kvs():
        if f2(k, v): filteredKVs.append((k,v))
    return tvstruct(pm._t, filteredKVs)

@coppertop(style=binary2)
def select(xs:pylist+pydict_keys+pydict_values, f) -> pylist:
    return [x for x in xs if f(x)]

@coppertop(style=binary2)
def select(xs:pytuple, f) -> pytuple:
    return tuple(x for x in xs if f(x))

@coppertop(style=binary2)
def select(a:agg, fn1) -> agg:
    fs = a._keys()
    cols = [c for c in a._values()] #a >> values >> std.each >> anon(lambda c: c)
    # collate the offsets that fn1 answers true
    os = []
    for o in range(cols[0].shape[0]):
        r = tvstruct(zip(fs, [c[o] for c in cols]))
        if fn1(r): os.append(o)
    # create new cols from the old cols and the offsets
    newCols = [c[os] for c in cols]
    return agg(zip(fs, newCols))

@coppertop(style=binary2)
def divide(xs:pytuple, f1):        # could be called filter but that would probably confuse
    selected = []
    rejected = []
    for x in xs:
        if f1(x):
            selected.append(x)
        else:
            rejected.append(x)
    return tuple(selected), tuple(rejected)



# **********************************************************************************************************************
# groupBy
# **********************************************************************************************************************

@coppertop
def groupBy(a:agg, keys):
    "answers a collection of groups"
    raise NotYetImplemented()

@coppertop
def groupBy(a:agg, keys, directions):
    "answers a collection of groups"
    raise NotYetImplemented()


