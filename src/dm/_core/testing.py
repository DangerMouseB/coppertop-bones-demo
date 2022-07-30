# **********************************************************************************************************************
#
#                             Copyright (c) 2020-2021 David Briant. All rights reserved.
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
from coppertop.pipe import MultiFn
from dm._core.maths import closeTo
from dm._core.structs import tvarray, tvstruct
from dm._core.types import adhoc, T1, T2, T3, T4, T5, T6, bool, pydict

_EPS = 7.105427357601E-15      # i.e. double precision



@coppertop(style=binary)
def assertEquals(actual, expected, suppressMsg=False, keepWS=False, returnResult=False, tolerance=_EPS):
    if keepWS:
        act = actual
        exp = expected
    else:
        act = actual.replace(" ", "").replace("\n", "") if isinstance(actual, (str,)) else actual
        exp = expected.replace(" ", "").replace("\n", "") if isinstance(expected, (str,)) else expected
    if isinstance(act, (int, float)) and isinstance(exp, (int, float)):
        equal = act >> closeTo(_, _, tolerance) >> exp
    else:
        equal = act == exp
    if returnResult:
        return equal
    else:
        if not equal:
            if suppressMsg:
                raise AssertionError()
            else:
                if isinstance(actual, (str,)):
                    actual = '"' + actual + '"'
                if isinstance(expected, (str,)):
                    expected = '"' + expected + '"'
                raise AssertionError(f'Expected {expected} but got {actual}')
        else:
            return None

@coppertop(style=ternary)
def check(actual, fn, expected):
    fnName = fn.name if hasattr(fn, 'name') else (fn.dispatcher.name if isinstance(fn, MultiFn) else '')
    with context(showFullType=False):
        if fn is builtins.type or fnName == 'typeOf':
            res = fn(actual)
            assert res == expected, f'Expected type <{expected}> but got type <{fn(actual)}>'
        else:
            res = fn(actual, expected)
            ppAct = repr(actual)
            ppExp = repr(expected)
            assert res == True, f'\nChecking fn \'{fn}\' failed the following:\nactual:   {ppAct}\nexpected: {ppExp}'
    return actual

@coppertop(style=binary2, supressDispatcherQuery=True)
def equal(a, b) -> bool:
    return a == b

@coppertop(style=binary2, supressDispatcherQuery=True)
def equal(a:tvarray, b:tvarray) -> bool:
    return bool((a == b).all())

@coppertop(style=binary2)
def different(a, b) -> bool:
    return a != b

@coppertop(style=binary2)
def different(a:tvarray, b:tvarray) -> bool:
    return bool((a != b).any())

@coppertop(style=binary2)
def sameLen(a, b):
    return len(a) == len(b)

@coppertop(style=binary2)
def sameShape(a, b):
    return a.shape == b.shape


# **********************************************************************************************************************
# sameNames
# **********************************************************************************************************************

@coppertop(style=binary2)
def sameKeys(a:pydict, b:pydict) -> bool:
    return a.keys() == b.keys()

@coppertop(style=binary2)
def sameNames(a:adhoc, b:adhoc) -> bool:
    return a._keys() == b._keys()

# some adhoc are defined like this (num ** account)[tvstruct]["positions"]
@coppertop(style=binary2)
def sameNames(a:(T1 ** T2)[tvstruct][T3], b:(T4 ** T2)[tvstruct][T5]) -> bool:
    return a._keys() == b._keys()


@coppertop(style=binary2)
def sameNames(a:(T1 ** T2)[tvstruct][T3], b:(T5 ** T4)[tvstruct][T6]) -> bool:
    assert a._keys() != b._keys()
    return False

# many structs should be typed (BTStruct)[tvstruct] and possibly (BTStruct)[tvstruct][T]   e.g. xy in pixels and xy in data

# if we can figure how to divide up the dispatch space (or even indicate it) this would be cool
# the total space below is T1[BTStruct][tvstruct] * T2[BTStruct][tvstruct] with
# T1[BTStruct][tvstruct] * T1[BTStruct][tvstruct] as a subspace / set
# can dispatch to the total space and then to the specific subset - with one as default
# @coppertop(style=binary2)
# def sameNames(a:T1[BTStruct][tvstruct], b:T2[BTStruct][tvstruct]) -> bool:
#     assert a._keys() != b._keys()
#     return False
#
# #@coppertop(style=binary2, memberOf=(T1[BTStruct][tvstruct]) * (T2[BTStruct][tvstruct])))
# @coppertop(style=binary2)
# def sameNames(a:T1[BTStruct][tvstruct], b:T1[BTStruct][tvstruct]) -> bool:
#     assert a._keys() == b._keys()
#     return True

# any should really be unhandles or alt or others or not default


