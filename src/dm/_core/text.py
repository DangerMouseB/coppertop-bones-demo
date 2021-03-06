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



from coppertop.core import Missing
from coppertop.pipe import *
from dm._core.types import pylist, pytuple, pydict, txt, index


@coppertop
def strip(s, chars=Missing):
    if chars is Missing:
        return s.strip()
    else:
        return s.strip(chars)

@coppertop(style=binary)
def split(s1, s2, maxsplit=Missing):
    if maxsplit is Missing:
        return s1.split(s2)
    else:
        return s1.split(s2, maxsplit)

# @coppertop
# def ljust(s:txt, n:index, pad:txt=' ') -> txt:
#     return s.ljust(n, pad)
#
# @coppertop
# def rjust(s:txt, n:index, pad:txt=' ') -> txt:
#     return s.rjust(n, pad)
#
# @coppertop
# def cjust(s:txt, n:index, pad:txt=' ') -> txt:
#     return s.center(n, pad)

@coppertop
def pad(s:txt, left:index=Missing , right:index=Missing, center:index=Missing, pad:txt=' '):
    if right is not Missing:
        return s.rjust(right, pad)
    if center is not Missing:
        return s.center(center, pad)
    return s.ljust(left, pad)

# see https://realpython.com/python-formatted-output/ and https://www.python.org/dev/peps/pep-3101/
@coppertop
def format(arg, f:txt, **kwargs) -> txt:
    return f.format(arg, **kwargs)
@coppertop
def format(args:pylist, f:txt, **kwargs) -> txt:
    return f.format(*args, **kwargs)
@coppertop
def format(args:pytuple, f:txt, **kwargs) -> txt:
    return f.format(*args, **kwargs)
@coppertop
def format(kwargs:pydict, f:txt) -> txt:
    return f.format(**kwargs)

@coppertop
def replace(haystack:txt, needle:txt, alt:txt) -> txt:
    return haystack.replace(needle, alt)