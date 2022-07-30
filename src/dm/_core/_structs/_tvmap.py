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

import sys
if hasattr(sys, '_TRACE_IMPORTS') and sys._TRACE_IMPORTS: print(__name__)

import abc
from collections import UserDict
from typing import Iterable


dict_keys = type({}.keys())
dict_values = type({}.values())
tZip = type(zip([]))


class tvstruct(UserDict):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._t_ = cls
        return instance

    def __init__(self, *args, **kwargs):
        super().__init__()
        if len(args) == 0:
            # tvstruct(), tvstruct(**kwargs)
            if kwargs:
                super().update(kwargs)
        elif len(args) == 1:
            arg = args[0]
            if isinstance(arg, (dict, list, tuple, zip)):
                # tvstruct(dictEtc)
                super().update(arg)
            elif isinstance(arg, tvstruct):
                # tvstruct(tvmapOrSubclass)
                self._t_ = arg._t
                super().update(arg)
            else:
                # tvstruct(t)
                self._t_ = arg
                #tvstruct(t, **kwargs)
                if kwargs:
                    super().update(kwargs)
        else:
            # tvstruct(t, dictEtc)
            arg1, arg2 = args
            self._t_ = arg1
            super().update(arg2)

            if kwargs:
                raise TypeError('No kwargs allowed when 2 args are provided')

    def __dir__(self) -> Iterable[str]:
        answer = list(super().keys())
        return answer

    def _asT(self, t):
        self._t_ = t
        return self

    def __getattribute__(self, name):

        if name[0:2] == '__':
            if name == '__class__':
                return tvstruct
            raise AttributeError()

        if name[0:1] == "_":
            if name == '_asT':
                return super().__getattribute__('_asT')
            if name == '_v':
                return self

            if name == '_t':
                return super().__getattribute__('__dict__')['_t']

            data = super().__getattribute__('__dict__')['data']

            if name == '_keys':
                return data.keys
            if name == '_kvs':
                return data.items
            if name == '_values':
                return data.values
            if name == '_pop':
                return data.pop
            if name == '_update':
                return data.update
            if name == '_setdefault':
                return data.setdefault
            if name == '_get':
                return data.get
            raise AttributeError()

        # I think we can get away without doing the following
        # if name == 'items':
        #     # for pycharm :(   - pycharm knows we are a subclass of dict so is inspecting us via items
        #     # longer term we may return a BTStruct instead of struct in response to __class__
        #     return {}.items

        if name == 'items':
            return super().__getattribute__('items')

        if name == 'keys':
            return super().__getattribute__('keys')

        if name == 'data':
            return super().__getattribute__('__dict__')['data']

        try:
            return super().__getattribute__('__dict__')['data'][name]
        except KeyError:
            raise AttributeError(f"'tvstruct' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name == '_t':
            raise AttributeError(f"Can't set _t on tvstruct")
        if name == '_v':
            raise AttributeError(f"Can't set _v on tvstruct")
        __dict__ = super().__getattribute__('__dict__')
        if name == 'data':
            return __dict__.__setitem__(name, value)
        if name == '_t_':
            return __dict__.__setitem__('_t', value)
        return __dict__['data'].__setitem__(name, value)

    def __call__(self, **kwargs):
        __dict__ = super().__getattribute__('__dict__')
        data = __dict__['data']
        for name, value in kwargs.items():
            data.__setitem__(name, value)
        return self

    def __getitem__(self, nameOrNames):
        if isinstance(nameOrNames, (list, tuple)):
            kvs = {name: self[name] for name in nameOrNames}
            return tvstruct(kvs)
        else:
            return super().__getattribute__('__dict__')['data'].__getitem__(nameOrNames)

    def __repr__(self):
        __dict__ = super().__getattribute__('__dict__')
        data = __dict__['data']
        itemStrings = (f"{str(k)}={repr(v)}" for k, v in data.items())
        if type(self._t) is abc.ABCMeta:
            name = self._t.__name__
        else:
            name = str(self._t)
        rep = f'{name}({", ".join(itemStrings)})'
        return rep

