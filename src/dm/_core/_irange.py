# **********************************************************************************************************************
#
#                             Copyright (c) 2019-2021 David Briant. All rights reserved.
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

# see https://kotlinlang.org/docs/sequences.html#sequence

BONES_MODULE = 'dm.core.range'

from coppertop.pipe import *
from ribs.types import bool, index

class IInputRange(object):
    @property
    def empty(self) -> bool:
        raise NotImplementedError()
    @property
    def front(self):
        raise NotImplementedError()
    def popFront(self):
        raise NotImplementedError()
    def moveFront(self):
        raise NotImplementedError()

    # assignable
    @front.setter
    def front(self, value):
        raise NotImplementedError()

    # python iterator interface - so we can use ranges in list comprehensions and for loops!!! ugh
    # this is convenient but possibly too convenient and it may muddy things hence the ugly name
    @property
    def _getIRIter(self):
        return IInputRange._Iter(self)

    class _Iter(object):
        def __init__(self, r):
            self.r = r
        def __iter__(self):
            return self
        def __next__(self):
            if self.r.empty: raise StopIteration
            answer = self.r.front
            self.r.popFront()
            return answer

@coppertop
def getIRIter(r):
    # the name is deliberately semi-ugly to discourage but not prevent usage - see comment above
    return r._getIRIter


class IForwardRange(IInputRange):
    def save(self):
        raise NotImplementedError()


class IBidirectionalRange(IForwardRange):
    @property
    def back(self):
        raise NotImplementedError()
    def moveBack(self):
        raise NotImplementedError()
    def popBack(self):
        raise NotImplementedError()

    # assignable
    @back.setter
    def back(self, value):
        raise NotImplementedError()


class IRandomAccessFinite(IBidirectionalRange):
    def moveAt(self, i: int):
        raise NotImplementedError()
    def __getitem__(self, i: index+slice):
        raise NotImplementedError()
    @property
    def length(self) -> index:
        raise NotImplementedError()

    # assignable
    def __setitem__(self, i: int, value):
        raise NotImplementedError()


class IRandomAccessInfinite(IForwardRange):
    def moveAt(self, i: int):
        raise NotImplementedError()

    def __getitem__(self, i: int):
        """Answers an element"""
        raise NotImplementedError()


class IOutputRange(object):
    def put(self, value):
        """Answers void"""
        raise NotImplementedError()




