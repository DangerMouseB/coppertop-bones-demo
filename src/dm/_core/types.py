# **********************************************************************************************************************
#
#                             Copyright (c) 2021 David Briant. All rights reserved.
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

import sys, builtins
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

from coppertop.pipe import _BonesTByPythonT
from bones.lang.metatypes import BTPrimitive as _BTAtom, BType as _BType, weaken as _weaken, tv
from bones.core.sentinels import Missing, dict_keys, dict_items, dict_values, function
from coppertop.types import *
from dm._core.structs import tvstruct as _tvstruct

adhoc = _BTAtom.define('adhoc').setConstructor(_tvstruct)
agg = _BTAtom.define('agg').setConstructor(_tvstruct)


class tvint(int):
    def __new__(cls, t, v, *args, **kwargs):
        instance = super(cls, cls).__new__(cls, v)
        instance._t_ = t
        return instance
    @property
    def _v(self):
        return super().__new__(int, self)
    @property
    def _t(self):
        return self._t_
    def __repr__(self):
        return f'{self._t}{super().__repr__()}'
    def _asT(self, t):
        self._t_ = t
        return self
tvint = i64['tvint'].setCoercer(tvint)


ascii = _BTAtom.define('ascii').setCoercer(tvtxt).setExclusive


anon = _BTAtom.define('anon').setOrthogonal
named = _BTAtom.define('named').setOrthogonal
aliased = _BTAtom.define('aliased').setImplicit
_weaken(anon, aliased)
_weaken(named, aliased)


void = _BTAtom.ensure('void')    # nothing returned on the stack from this function (should not be assignable)

# NB a 1x1 matrix is assumed to be a scalar, e.g. https://en.wikipedia.org/wiki/Dot_product#Algebraic_definition

vec = (N**num)          # N**num is common so don't name it
matrix = (N**N**num).nameAs('matrix').setNonExclusive
colvec = matrix['colvec'].setNonExclusive
rowvec = matrix['rowvec'].setNonExclusive

I = _BTAtom.define('I')
square = _BTAtom.define('square')
right = _BTAtom.define('right')
left = _BTAtom.define('left')
upper = _BTAtom.define('upper')
lower = _BTAtom.define('lower')
orth = _BTAtom.define('orth')
diag = _BTAtom.define('diag')
tri = _BTAtom.define('tri')
cov = _BTAtom.define('cov')

ccy = _BTAtom.define('ccy').setExplicit
fx = _BTAtom.define('fx').setExplicit

matrix[tv].setConstructor(tv).setExclusive    # tv provides a coercion method so matrix[tv] doesn't need to

pair = _BTAtom.define('pair')

# add more python equivalences
_BonesTByPythonT.update({
    builtins.list : pylist,
    builtins.dict : pydict,
    builtins.tuple : pytuple,
    builtins.set : pyset,
    dict_keys : pydict_keys,
    dict_items : pydict_items,
    dict_values : pydict_values,
    function : pyfunc,
})


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')


