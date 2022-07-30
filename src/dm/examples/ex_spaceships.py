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

from coppertop.pipe import *
from dm.core import PP, check, equal
from bones.lang.metatypes import BTPrimitive, tv
from bones.core.sentinels import Null

from ribs.types import txt, null


# Inspired by the wikipedia article on multi-dispatch - https://en.wikipedia.org/wiki/Multiple_dispatch
# Hopefully this is even more readable than Julia

tAsteroid = BTPrimitive.ensure('asteroid').setCoercer(tv)
tShip = BTPrimitive.ensure('ship').setCoercer(tv)
tEvent = BTPrimitive.ensure('event').setCoercer(tv)


@coppertop
def collide(a:tAsteroid, b:tAsteroid) -> tEvent:
    return f'{a._v} split {b._v} (collide<:asteroid,asteroid:>)' | tEvent

@coppertop
def collide(a:tShip, b:tAsteroid) -> tEvent:
    return f'{a._v} tried to ram {b._v} (collide<:ship,asteroid:>)' | tEvent

@coppertop
def collide(a:tAsteroid, b:tShip) -> tEvent:
    return f'{a._v} destroyed {b._v} (collide<:asteroid,ship:>)' | tEvent

@coppertop
def collide(a:tShip, b:tShip) -> null:
    return Null
#    return f'{a} bounced {b} (collide<:ship,ship:>)' >> to(_,tEvent)

@coppertop
def process(e:tEvent) -> txt:
    return e._v

@coppertop
def process(e:null) -> txt:
    return 'nothing happened'

# @coppertop
# def process(e:tEvent+null) -> txt:
#     return 'nothing happened' if e._t == null else e._v


borg = tShip['borg'].setCoercer(tv)

@coppertop
def collide(a:borg, b:tShip) -> tEvent:
    return f'{a._v} subsumes {b._v} (collide<:borg,ship:>)' | tEvent

@coppertop
def collide(a:borg, b:borg) -> tEvent:
    return f'{a._v} merges with {b._v} (collide<:borg,big:>)' | tEvent



def testCollide(pp=False):
    ship1 = 'ship1' | tShip
    ship2 = 'ship2' | tShip
    ast1 = 'big asteroid' | tAsteroid
    ast2 = 'small asteroid' | tAsteroid
    b = 'borg' | borg

    if pp:
        ship1 >> collide(_, ship2) >> process >> PP
        ship1 >> collide(_, ast1) >> process >> PP
        ship2 >> collide(ast2, _) >> process >> PP
        ast1 >> collide(_, ast2) >> process >> PP
        b >> collide(_, ship2) >> process >> PP
        b >> collide(_, ast1) >> process >> PP
        b >> collide(ast2, _) >> process >> PP
        ship1 >> collide(_, b) >> process >> PP
        b >> collide(_, b) >> process >> PP
    else:
        ship1 >> collide(_, ship2) >> process >> check >> equal >> 'nothing happened'
        # 'ship1 tried to ram big asteroid (collide<:ship,asteroid:>)'
        # 'small asteroid destroyed ship2 (collide<:asteroid,ship:>)'
        # 'big asteroid split small asteroid (collide<:asteroid,asteroid:>)'


def main():
    testCollide()


if __name__ == '__main__':
    testCollide(True)
    print('pass')
