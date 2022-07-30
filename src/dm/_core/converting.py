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


import numpy, datetime, csv

from coppertop.pipe import *
from coppertop.core import Missing
from dm._core.structs import tvarray, tvseq, tvstruct
from dm._core.accessing import values
from dm._core.datetime import toCTimeFormat, parseDate
from dm._core.transforming import each
from dm._core.types import agg, adhoc, txt, pylist, pydict, T1, N, pytuple, pydict_keys, pydict_values, date, index, num, \
    npfloat, pair as tPair
from bones.lang.metatypes import BType




@coppertop
def fromCsv(pfn:txt, renames:pydict, conversions:pydict, cachePath=Missing) -> agg:
    with open(pfn, mode='r') as f:
        r = csv.DictReader(f)
        d = {}
        for name in r.fieldnames:
            d[name] = list()
        for cells in r:
            for k, v in cells.items():
                d[k].append(v)
        a = agg()
        for k in d.keys():
            newk = renames.get(k, k)
            fn = conversions.get(newk, lambda l: tvarray(l, Missing))     ## we could insist the conversions return tvarray s
            a[newk] = fn(d[k])
    return a


# **********************************************************************************************************************
# to
# **********************************************************************************************************************

@coppertop(style=binary2)
def pair(a, b):
    return tvstruct(tPair[tvstruct], a=a, b=b)


# **********************************************************************************************************************
# to
# **********************************************************************************************************************

@coppertop
def to(x:pydict+pylist, t:adhoc) -> adhoc:
    return t(x)

@coppertop
def to(x, t):
    if isinstance(t, BType):
        return t(x)
    try:
        return t(x)
    except:
        raise TypeError(f'Catch all can\'t convert to {repr(t)}')

@coppertop(style=unary1)
def to(x:pydict_keys+pydict_values, t:pylist) -> pylist:
    return list(x)

@coppertop(style=unary1)
def to(x, t:pylist) -> pylist:
    return list(x)

@coppertop(style=unary1)
def to(x:adhoc, t:pydict) -> pydict:
    return dict(x._kvs())

@coppertop(style=unary1)
def to(x, t:pydict) -> pydict:
    return dict(x)

@coppertop(style=unary1)
def to(p:tPair, t:pydict) -> pydict:
    return dict(zip(p.a, p.b))

@coppertop
def to(x:txt, t:date, f:txt) -> date:
    return parseDate(x, toCTimeFormat(f))

@coppertop(style=unary1)
def to(x, t:txt) -> txt:
    return str(x)

@coppertop(style=unary1)
def to(v:T1, t:T1) -> T1:
    return v

@coppertop
def to(x, t:index) -> index:
    return int(x)

@coppertop
def to(x, t:num) -> num:
    return float(x)

@coppertop
def to(a:agg, t:tvarray) -> tvarray:
    return numpy.vstack(a >> values >> each >> (lambda n: n)).T.view(tvarray)

@coppertop
def to(x:pylist+pytuple, t:(N**T1)[tvseq], tByT) -> (N**T1)[tvseq]:
    return tvseq((N**tByT[T1])[tvseq], x)
