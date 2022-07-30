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


import os, os.path, json
from io import TextIOWrapper
from coppertop.pipe import *
from dm._core.types import txt, pylist
from dm._core.text import strip
from dm._core.transforming import each

getCwd = coppertop(style=unary1, newName='getCwd')(os.getcwd)
isFile = coppertop(style=unary1, newName='isFile')(os.path.isfile)
isDir = coppertop(style=unary1, newName='isDir')(os.path.isdir)
dirEntries = coppertop(style=unary1, newName='dirEntries')(os.listdir)

@coppertop(style=binary2)
def joinPath(a, b):
    return os.path.join(a, *(b if isinstance(b, (list, tuple)) else [b]))

@coppertop
def readlines(f:TextIOWrapper) -> pylist:
    return f.readlines()

@coppertop
def linesOf(pfn:txt):
    with open(pfn) as f:
        return f >> readlines >> each >> strip(_,'\\n')

@coppertop(style=binary)
def copyTo(src, dest):
    raise NotImplementedError()

@coppertop
def readJson(pfn:txt):
    with open(pfn) as f:
        return json.load(f)

@coppertop
def readJson(f:TextIOWrapper):
    return json.load(f)

