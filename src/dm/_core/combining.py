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


from coppertop.pipe import *
from bones.core.errors import NotYetImplemented
from dm._core.structs import tvstruct, tvseq

from dm._core.types import adhoc, agg, txt, N, pylist, T1, pytuple, pydict
from dm._core.misc import fitsWithin



# **********************************************************************************************************************
# interleave
# **********************************************************************************************************************

@coppertop(style=binary2)
def interleave(xs:pylist+pytuple, b) -> pylist:
    answer = xs[0]
    for x in xs[1:]:
        answer = answer >> join >> b >> join >> x
    return answer

@coppertop(style=binary2)
def interleave(a:(N**T1)[tvseq], b: T1) -> (N**T1)[tvseq]:
    raise NotYetImplemented()

@coppertop(style=binary2)
def interleave(a:(N**T1)[tvseq], b: (N**T1)[tvseq]) -> (N**T1)[tvseq]:
    raise NotYetImplemented()

@coppertop(style=binary2)
def interleave(xs:N**txt, sep:txt) -> txt:
    # ['hello', 'world'] >> joinAll(_,' ')
    return sep.join(xs)

@coppertop(style=binary2)
def interleave(xs:pylist+pytuple, sep:txt) -> txt:
    return sep.join(xs)


# **********************************************************************************************************************
# join
# **********************************************************************************************************************

@coppertop(style=binary2)
def join(xs:pylist, ys:pylist) -> pylist:
    return xs + ys

@coppertop(style=binary2)
def join(xs:(N**T1)[tvseq], ys:(N**T1)[tvseq], tByT) -> (N**T1)[tvseq]:
    return tvseq((N**(tByT[T1]))[tvseq], xs.data + ys.data)

@coppertop(style=binary2)
def join(s1:txt, s2:txt) -> txt:
    return s1 + s2

@coppertop(style=binary2)
def join(d1:pydict, d2:pydict) -> pydict:
    answer = dict(d1)
    for k, v in d2.items():
        if k in answer:
            raise KeyError(f'{k} already exists in d1 - use underride or override to merge (rather than join) two pydicts')
        answer[k] = v
    return answer


# **********************************************************************************************************************
# joinAll
# **********************************************************************************************************************

@coppertop
def joinAll(xs:N**txt) -> txt:
    return ''.join(xs)

@coppertop
def joinAll(xs:pylist+pytuple) -> txt + ((N**T1)[tvseq]) + pylist + pytuple:
    # could be a list of strings or a list of (N**T1) & tvseq
    # answer a string if no elements
    if not xs:
        return ''
    typeOfFirst = typeOf(xs[0])
    if typeOfFirst >> fitsWithin >> txt:
        return ''.join(xs)
    elif typeOfFirst >> fitsWithin >> (N**T1)[tvseq]:
        elements = []
        for x in xs:
            # could check the type of each list using metatypes.fitsWithin
            elements.extend(x.data)
        return tvseq(xs[0]._t, elements)
    elif typeOfFirst >> fitsWithin >> pylist:
        answer = []
        for e in xs:
            answer += e
        return answer
    elif typeOfFirst >> fitsWithin >> pytuple:
        answer = ()
        for e in xs:
            answer += e
        return answer


# **********************************************************************************************************************
# merge - answers A with everything either overridden or added from B
# **********************************************************************************************************************

@coppertop(style=binary2)
def merge(a:pydict, b:pydict) -> pydict:
    answer = dict(a)
    answer.update(b)
    return answer

@coppertop(style=binary2)
def merge(a:pydict, b:tvstruct) -> pydict:
    answer = dict(a)
    answer.update(b._kvs())
    return answer

@coppertop(style=binary2)
def merge(a:adhoc, b:adhoc) -> adhoc:
    answer = adhoc(a)
    answer._update(b._kvs())
    return answer

@coppertop(style=binary2)
def merge(a:tvstruct, b:tvstruct) -> tvstruct:
    answer = tvstruct(a)
    answer._update(b._kvs())
    return answer

@coppertop(style=binary2)
def merge(a:tvstruct, b:pydict) -> tvstruct:
    answer = tvstruct(a)
    answer._update(b)
    return answer


# **********************************************************************************************************************
# override - for each in A replace with the one in B if it exists
# **********************************************************************************************************************

@coppertop(style=binary2)
def override(a:tvstruct, b:tvstruct) -> tvstruct:
    answer = tvstruct(a)
    for k, v in b._kvs():
        if k in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer


# **********************************************************************************************************************
# underride
# **********************************************************************************************************************

@coppertop(style=binary2)
def underride(a:tvstruct, b:tvstruct) -> tvstruct:
    answer = tvstruct(a)
    for k, v in b._kvs():
        if k not in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer

@coppertop(style=binary2)
def underride(a:tvstruct, b:pydict) -> tvstruct:
    answer = tvstruct(a)
    for k, v in b.items():
        if k not in answer:
            answer[k] = v
        # answer._setdefault(k, v)      # this doesn't respect insertion order!!
    return answer


# **********************************************************************************************************************
# agg joins
# **********************************************************************************************************************

@coppertop(style=binary2)
def lj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def rj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def ij(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def oj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def uj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


@coppertop(style=binary2)
def aj(agg1:agg, agg2:agg):
    raise NotYetImplemented()


