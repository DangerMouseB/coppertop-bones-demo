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
from dm._core.structs import tvstruct
from dm._core.types import adhoc, agg, pydict, pylist, pyfunc


# **********************************************************************************************************************
# sort
# **********************************************************************************************************************

@coppertop(style=unary1)
def sort(x:pydict) -> pydict:
    return dict(sorted(x.items(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:tvstruct) -> tvstruct:
    return tvstruct(sorted(x._kvs(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:adhoc) -> adhoc:
    return adhoc(sorted(x._kvs(), key=None, reverse=False))

@coppertop(style=unary1)
def sort(x:pylist) -> pylist:
    return sorted(x, key=None, reverse=False)


# **********************************************************************************************************************
# sortBy
# **********************************************************************************************************************

@coppertop
def sortBy(x:agg, fields):
    raise NotYetImplemented()

@coppertop
def sortBy(x:agg, fields, directions):
    raise NotYetImplemented()


# **********************************************************************************************************************
# sortRev
# **********************************************************************************************************************

@coppertop(style=unary1)
def sortRev(x:pylist) -> pylist:
    return sorted(x, key=None, reverse=True)

@coppertop(style=unary1)
def sortRev(x:pydict) -> pydict:
    return dict(sorted(x.items(), key=None, reverse=True))


# **********************************************************************************************************************
# sortRevUsing
# **********************************************************************************************************************

@coppertop(style=binary2)
def sortRevUsing(x:pylist, key:pyfunc) -> pylist:
    return sorted(x, key=key, reverse=True)

@coppertop(style=binary2)
def sortRevUsing(x:pydict, key:pyfunc) -> pydict:
    return dict(sorted(x.items(), key=key, reverse=True))


# **********************************************************************************************************************
# sortUsing
# **********************************************************************************************************************

@coppertop(style=binary2)
def sortUsing(x:pylist, key:pyfunc) -> pylist:
    return sorted(x, key=key, reverse=False)

@coppertop(style=binary2)
def sortUsing(x:pydict, key:pyfunc) -> pydict:
    return dict(sorted(x.items(), key=key, reverse=False))

@coppertop(style=binary)
def sortUsing(soa, f):
    raise NotYetImplemented()

