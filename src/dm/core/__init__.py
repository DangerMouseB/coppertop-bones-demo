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

import sys

if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

import inspect
from coppertop.pipe import _DispatcherBase, _MultiDispatcher, MultiFn, _, sig
from dm._core._structs._tvarray import tvarray
from dm._core._structs._tvstruct import tvstruct

_mfByName = {}



def _collectDispatchers(mfByName, module):
    members = inspect.getmembers(module)
    members = [(name, o) for (name, o) in members if (name[0:1] != '_')]         # remove private
    members = [(name, mf) for (name, mf) in members if isinstance(mf, MultiFn)]
    for name, mf in members:
        mfByName.setdefault(name, []).append(mf)



# aggregation protocols
from dm._core import accessing as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import combining as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import complex as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import converting as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import dividing as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import generating as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import reordering as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import searching as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import transforming as _mod; _collectDispatchers(_mfByName, _mod)

# other protocols
from dm._core import files as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import linalg as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import maths as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import misc as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import stdio as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import testing as _mod; _collectDispatchers(_mfByName, _mod)
from dm._core import text as _mod; _collectDispatchers(_mfByName, _mod)
# from dm._core import types as _mod; _collectDispatchers(_mfByName, _mod)

# aggregation protocols
from dm._core.accessing import *
from dm._core.combining import *
from dm._core.complex import *
from dm._core.converting import *
from dm._core.dividing import *
from dm._core.generating import *
from dm._core.reordering import *
from dm._core.searching import *
from dm._core.transforming import *

# other protocols
from dm._core.files import *
from dm._core.linalg import *
from dm._core.maths import *
from dm._core.misc import *
from dm._core.stdio import *
from dm._core.testing import *
from dm._core.text import *
# from dm._core.types import *

from dm._core.misc import _t, _v   # needs doing separately as _ generally indicates it is pvt



__all__ = list(_mfByName.keys()) + ['_', 'tvarray', 'agg', '_t', '_v', 'typeOf', 'sig']
__all__.sort()


if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__ + ' - done')
