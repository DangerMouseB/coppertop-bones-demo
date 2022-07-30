# **********************************************************************************************************************
#
#                             Copyright (c) 2022 David Briant. All rights reserved.
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

from bones.lang.metatypes import BTPrimitive, S
from dm.core import tvstruct
from coppertop.core import Missing
from ribs.types import pydict, count, txt
from dm.examples.cluedo.cards import TBI # the hand with the people, weapon and room - To Be Inferred


card = BTPrimitive.ensure('card')
handId = BTPrimitive.ensure('handId')
ndmap = BTPrimitive.ensure('ndmap')
pad_element = S(has=txt, suggestions=count, like=count)
cluedo_pad = ((card*handId)**pad_element)[ndmap] & BTPrimitive.ensure('cluedo_pad')
cluedo_pad = pydict #& BTPrimitive.ensure('cluedo_pad') once we have tvmao we can do this
cluedo_bag = (tvstruct & BTPrimitive.ensure('_cluedo_bag')).nameAs('cluedo_bag')


YES = 'X'
NO = '-'
MAYBE = '?'

class HasOne(object):
    def __init__(self, handId=Missing):
        self.handId = handId
    def __rsub__(self, handId):     # handId / has
        assert self.handId == Missing, 'Already noted a handId'
        return HasOne(handId)
one = HasOne()
