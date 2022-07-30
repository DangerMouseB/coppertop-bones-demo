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

import scipy.linalg, numpy
from coppertop.pipe import *
from dm._core.structs import tvarray
from dm._core.converting import to         # extended below
from dm._core.types import matrix, colvec, rowvec, vec, N, num, offset, pytuple, pylist


_matrix = matrix[tvarray]
_colvec = colvec[tvarray]
_rowvec = rowvec[tvarray]

_vec = vec[tvarray].setConstructor(tvarray)

def _to_matrix(t, x) -> _matrix:
    answer = tvarray(t, x)
    ndims = len(answer.shape)
    if ndims == 0:
        if t in (_rowvec, _colvec, _matrix):
            answer.shape = (1, 1)
        else:
            raise TypeError('Huh')
    elif ndims == 1:
        if t in (_colvec, _matrix):
            answer.shape = (answer.shape[0], 1)
            answer = answer._asT(_colvec)
        elif t is _rowvec:
            answer.shape = (1, answer.shape[0])
        else:
            raise TypeError('Huh')
    elif ndims == 2:
        if t is _rowvec and answer.shape[0] != 1:
            raise TypeError('x is not a row vec')
        if t is _colvec and answer.shape[1] != 1:
            raise TypeError('x is not a col vec')
    elif ndims > 2:
        raise TypeError('x has more than 2 dimensions')
    return answer
matrix[tvarray].setConstructor(_to_matrix)
colvec[tvarray].setConstructor(_to_matrix)
rowvec[tvarray].setConstructor(_to_matrix)



@coppertop
def at(xs:_matrix, o:offset):
    return xs[o]

@coppertop
def at(xs:_matrix, os:pylist):
    return xs[os]

@coppertop(style=unary1)
def min(x:_matrix):
    return numpy.min(x)

@coppertop(style=unary1)
def max(x:_matrix):
    return numpy.max(x)

@coppertop(style=ternary)
def both(a: _matrix, f, b:_matrix) -> _matrix:
    with numpy.nditer([a, b, None]) as it:
        for x, y, z in it:
            z[...] = f(x,y)
        return it.operands[2].view(tvarray) | _matrix

@coppertop
# def to(x:pylist, t:matrix[tvarray]) -> matrix[tvarray]:
def to(x:pylist, t:_matrix) -> _matrix:
    return _to_matrix(t, x)

@coppertop
def inv(A:_matrix) -> _matrix:
    return numpy.linalg.inv(A)

@coppertop(style=binary2)
def dot(A:colvec[tvarray], B:colvec[tvarray]) -> num:
    return float(numpy.dot(A, B))

@coppertop(style=binary2)
def solveTriangular(R:_matrix, b:_matrix) -> _matrix:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.solve_triangular.html
    return scipy.linalg.solve_triangular(R, b).view(tvarray) | _matrix

@coppertop(style=unary1)
def shape(x:_matrix) -> pytuple:
    return x.shape

@coppertop(style=unary1)
def T(A:_matrix) -> _matrix:
    return A.T

__all__ = ['at', 'min', 'max', 'both', 'to', 'inv', 'dot', 'solveTriangular', 'shape', 'T']
