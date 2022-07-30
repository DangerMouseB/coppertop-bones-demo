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


import builtins
from coppertop.pipe import *
from coppertop.pipe import typeOf
from bones.lang.metatypes import cacheAndUpdate, fitsWithin as _fitsWithin, BTPrimitive as _BTAtom
from dm._core.transforming import inject
from dm._core.types import tv, T


_SBT = _BTAtom.define('ShouldBeTyped')      # temporary type to allow"  'DE000762534' >> box | tISIN - i.e. make the box then type it

@coppertop
def box(v) -> _SBT:
    return tv(_SBT, v)

@coppertop
def box(v, t:T) -> T:
    return tv(t, v)

@coppertop
def getAttr(x, name):
    return getattr(x, name)

@coppertop
def compose(x, fs):
    return fs >> inject(_, x, _) >> (lambda x, f: f(x))

def not_(b):
    return False if b else True
Not = coppertop(style=unary1, newName='Not')(not_)
not_ = coppertop(style=unary1, newName='not_')(not_)

repr = coppertop(style=unary1, newName='repr')(builtins.repr)

@coppertop(style=unary1)
def _t(x):
    return x._t

@coppertop(style=unary1)
def _v(x):
    return x._v

@coppertop(style=binary2, supressDispatcherQuery=True)
def fitsWithin(a, b):
    doesFit, tByT, distances = cacheAndUpdate(_fitsWithin(a, b), {})
    return doesFit

@coppertop(style=binary2, supressDispatcherQuery=True)
def doesNotFitWithin(a, b):
    does = a >> fitsWithin >> b
    return does >> not_

@coppertop
def PP(x):
    print(str(x))
    return x

