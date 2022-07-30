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

import operator, random
import numpy as np
import scipy.stats
from coppertop.pipe import *
from dm.core import sort, both, zip, kvs, values, keys, merge, select, to
from dm.core.structs import tvstruct, tvarray
from dm.core.linalg import matrix
from dm.core.types import adhoc, num, T, T1, T2, T3, pylist, pydict, index, pytuple, num
from bones.lang.metatypes import BTPrimitive

from dm.core import sequence


# numsEtAl models the storage mechanism for a pmf or likelihood and the multiplication thereof pre
# normalise, i.e. the numbers may not add up to one. Additionally for compactness we wish to be able
# to add tags, e.g to label a pmf as `d6`, etc, or to a likelihood with the data such as `PDoorBIf`


# str**str and num**str above imply a dynamic type - i.e. return type depends on key value - however
# the reality is that the programmer always knows which one is needed

# bag1994.Red -> can always be dispatched to num
# d6[1] -> can be dispatched to num
#
# but
#
# jar.tag -> should be disallowed
# jar >> at[tag] can be allowed but is ambiguouse as str weakens to str
# conclusion type wise we need a tag discrimination

tbTag = BTPrimitive.ensure('dm.tbTag')         # since we don't have a tvtxt we either box or add a subclass TBD


def _makePmf(*args, **kwargs):
    return _normalisedInPlaceAdhoc(tvstruct(*args, **kwargs))

numsEtAl = BTPrimitive.ensure('numsEtAl')[tvstruct].setConstructor(tvstruct)
PMF = numsEtAl['PMF'].setConstructor(_makePmf).setPP('PMF')
L = numsEtAl['L'].setConstructor(tvstruct).setPP('L')        # likelihood
CMF = numsEtAl['CMF'].setConstructor(tvstruct).setPP('CMF')


# we conceptualise a PMF as a pair of lists rather than a range - so materialise the dict_keys etc

@coppertop(style=unary1)
def kvs(x: numsEtAl[T]) -> pylist:
    return list(x._kvs())

@coppertop(style=unary1)
def values(x: numsEtAl[T]) -> pylist:
    return list(x._values())

@coppertop(style=unary1)
def keys(x: numsEtAl[T]) -> pylist:
    return list(x._keys())




_matrix = matrix & tvarray



@coppertop(style=unary1)
def normalise(pmf:numsEtAl+L+adhoc) -> PMF:
    # immutable, asssumes non-numeric values are tags and all numeric values are part of pmf
    return _normalisedInPlaceAdhoc(adhoc(pmf)) | PMF

def _normalisedInPlaceAdhoc(pmf):
    total = 0
    for k, v in pmf._kvs():
        if isinstance(v, (float, int)):
            total += v
    factor = 1 / total
    for k, v in pmf._kvs():
        if isinstance(v, (float, int)):
            pmf[k] = v * factor
    return pmf


@coppertop(style=unary1)
def normalise(pmf:pydict) -> PMF:
    # immutable, asssumes non-numeric values are tags and all numeric values are part of pmf
    return PMF(_normalisedInPlacePydict(pmf))

def _normalisedInPlacePydict(pmf:pydict) -> pydict:
    total = 0
    for k, v in pmf.items():
        if isinstance(v, (float, int)):
            total += v
    factor = 1 / total
    for k, v in pmf.items():
        if isinstance(v, (float, int)):
            pmf[k] = v * factor
    return pmf


@coppertop(style=unary1)
def uniform(nOrXs:pylist) -> PMF:
    '''Makes a uniform PMF. xs can be sequence of values or [length]'''
    # if a single int it is a count else there must be many xs
    answer = adhoc() | PMF
    if len(nOrXs) == 1:
        if isinstance(nOrXs[0], int):
            n = nOrXs[0]
            p = 1.0 / n
            for x in sequence(0, n-1):
                answer[float(x)] = p
            return answer
    p = 1.0 / len(nOrXs)
    for x in nOrXs:
        answer[float(x)] = p
    return answer


@coppertop(style=unary1)
def mix(args:pylist) -> PMF:
    """answer a mixture pmf, each arg is (beta, pmf) or pmf"""
    t = {}
    for arg in args:
        beta, pmf = arg if isinstance(arg, (tuple, list)) else (1.0, arg)
        for x, p in pmf._kvs():
            t[x] = t.setdefault(x, 0) + beta * p
    return t >> sort >> normalise


@coppertop(style=unary1)
def mean(pmf:PMF) -> num:
    fs = pmf >> keys
    ws = pmf >> values
    try:
        return np.average(fs, weights=ws) >> to(_,num)
    except TypeError:
        fs, ws = list([fs, ws] >> zip) >> select >> (lambda fv: not isinstance(fv[0], str)) >> zip
        return np.average(fs, weights=ws) >> to(_,num)
    # if pmf:
    #     answer = 0
    #     for x, p in pmf >> kvs:
    #         answer += x * p
    #     return answer
    # else:
    #     return np.nan


@coppertop
def gaussian_kde(data) -> scipy.stats.kde.gaussian_kde:
    return scipy.stats.gaussian_kde(data)

@coppertop
def to(xs:pylist, t:PMF, kde:scipy.stats.kde.gaussian_kde) -> adhoc:
    answer = adhoc()
    answer._kde = kde
    for x in xs:
        answer[x] = kde.evaluate(x)[0]
    return answer >> normalise

@coppertop
def toCmf(pmf:PMF) -> CMF:
    running = 0.0
    answer = CMF()
    answer2 = dict()
    # for k, v in pmf._kvs():
    for k, v in pmf >> kvs:
        if isinstance(v, float):
            running += v
            answer[k] = running
        else:
            answer2[k] = v
    cmf = np.array(list(answer._kvs()))
#    cmf[:, 1] = np.cumsum(cmf[:, 1])
    answer = answer >> merge >> answer2
    answer['_cmf'] = cmf
    return answer

@coppertop(style=binary2)
def merge(a:numsEtAl[T1], b:tvstruct&T2, tByT) -> numsEtAl[T1]:
    answer = tvstruct(tByT[T1], a)
    answer._update(b._kvs())
    return answer

@coppertop(style=binary2)
def sample(cmf:adhoc, n:index) -> _matrix:
    vals = []
    sortedCmf = cmf['_cmf']
    for _ in range(n):
        p = random.random()
        i = np.searchsorted(sortedCmf[:, 1], p, side='left')
        vals.append(sortedCmf[i, 0])
    return _matrix(vals)

@coppertop(style=binary2)
def sample(kde:scipy.stats.kde.gaussian_kde, n:index) -> _matrix:
    return kde.resample(n).flatten()



@coppertop(style=binary2)
def pmfMul(lhs:numsEtAl[T1], rhs:numsEtAl[T2]) -> numsEtAl:
    # pmf(lhs kvs '{(x.k, x.v*(y.v)} (rhs kvs)) normalise
    return adhoc(both(
        lhs >> kvs,
        lambda fv1, fv2: (fv1[0], fv1[1] * fv2[1]),
        rhs >> kvs
    )) | numsEtAl



@coppertop(style=binary2)
def rvAdd(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.add)

@coppertop(style=binary2)
def rvSub(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.sub)

@coppertop(style=binary2)
def rvMul(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.mul)

@coppertop(style=binary2)
def rvDiv(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, operator.truediv)

@coppertop(style=binary2)
def rvMax(lhs:PMF, rhs:PMF) -> PMF:
    return _rvOp(lhs, rhs, max)

def _rvOp(lhs, rhs, op):
    xps = {}
    for x1, p1 in lhs._kvs():
        for x2, p2 in rhs._kvs():
            x = op(x1, x2)
            xps[x] = xps.setdefault(x, 0.0) + p1 * p2
    return _normalisedInPlaceAdhoc(adhoc(
        sorted(
            xps.items(),
            key=lambda xp: xp[0]
        )
    )) | PMF


@coppertop(style=unary1)
def toXsPs(pmf:PMF) -> pytuple:
    return tuple(zip(pmf._kvs()))

@coppertop(style=unary)
def percentile(pmf:PMF, percentage:num):
    total = 0
    for k, v in pmf._kvs():
        total += v
        if total >= percentage:
            return k

@coppertop(style=unary)
def percentile(cmf:CMF, percentage:num):
    for k, v in cmf._kvs():
        if v >= percentage:
            return k


