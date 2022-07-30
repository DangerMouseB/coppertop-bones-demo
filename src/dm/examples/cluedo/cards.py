# **********************************************************************************************************************
#
#                             Copyright (c) 2021-2022 David Briant. All rights reserved.
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

from enum import IntEnum

__all__ = [
    'TBI',
    'Gr', 'Mu', 'Or', 'Pe', 'Pl', 'Sc',
    'Ca', 'Da', 'Le', 'Re', 'Ro', 'Wr',
    'Ki', 'Ba', 'Co', 'Bi', 'Li', 'St', 'Ha', 'Lo', 'Di',
    'people', 'weapons', 'rooms',
    'Card',
]

ppLongNames = [
    'TBI',
    'Green', 'Mustard', 'Orchid', 'Peacock', 'Plum', 'Scarlet',
    'Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Wrench',
    'Ballroom', 'Billiard Room', 'Conservatory', 'Dining Room', 'Hall', 'Kitchen', 'Library', 'Lounge', 'Study'
]

ppShortNames = [
    'TBI',
    'Gr', 'Mu', 'Or', 'Pe', 'Pl', 'Sc',
    'Ca', 'Da', 'Le', 'Re', 'Ro', 'Wr',
    'Ba', 'Bi', 'Co', 'Di', 'Ha', 'Ki', 'Li', 'Lo', 'St'
]


class Card(IntEnum):
    TBI = 0

    Gr = 1
    Mu = 2
    Or = 3
    Pe = 4
    Pl = 5
    Sc = 6

    Ca = 7
    Da = 8
    Le = 9
    Re = 10
    Ro = 11
    Wr = 12

    Ba = 13
    Bi = 14
    Co = 15
    Di = 16
    Ha = 17
    Ki = 18
    Li = 19
    Lo = 20
    St = 21

    def __str__(self):
        return ppLongNames[self]
    def __repr__(self):
        return ppShortNames[self]

TBI = Card.TBI

Gr = Card.Gr
Mu = Card.Mu
Or = Card.Or
Pe = Card.Pe
Pl = Card.Pl
Sc = Card.Sc

Ca = Card.Ca
Da = Card.Da
Le = Card.Le
Re = Card.Re
Ro = Card.Ro
Wr = Card.Wr

Ba = Card.Ba
Bi = Card.Bi
Co = Card.Co
Di = Card.Di
Ha = Card.Ha
Ki = Card.Ki
Li = Card.Li
Lo = Card.Lo
St = Card.St

people = [Gr, Mu, Or, Pe, Pl, Sc]
weapons = [Ca, Da, Le, Re, Ro, Wr]
rooms = [Ki, Ba, Co, Bi, Li, St, Ha, Lo, Di]
