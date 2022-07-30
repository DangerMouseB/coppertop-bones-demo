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

import datetime

from coppertop.core import *
from coppertop.pipe import *
from dm.examples.cluedo.cards import *
from dm.examples.cluedo.core import one
from dm.examples.cluedo.algos import createBag, figureKnown, processResponses, cluedo_bag, processSuggestions
from dm.examples.cluedo.reports import rep1


@coppertop
def PP(bag:cluedo_bag) -> cluedo_bag:
    bag.pad >> rep1(_, bag.handId) >> PP
    return bag


def game1():
    Me = Sc

    events = [
        [Or, Bi],
        [Or, Mu],
        [Mu, Re],
        [Pl, Ca],

        [Gr, Pe, Ro, Bi], Mu, Or - one,


        [Gr, Pe, Ro, Bi], Mu, Or - one,
        [Mu, Mu, Ro, Li], Or - one,
        [Or, Gr, Ca, Ba], Sc, Pe - one,
        [Me, Or, Da, Ki], Pe, [Pl, Da],
        [Pe, Mu, Re, Co], Pl, Gr, Mu - one,
        [Pl, Sc, Wr, Ba], Gr, Mu, Or, [Me, Sc],
        [Gr, Pl, Le, Di], Mu - one,
        [Mu, Pe, Ro, Li], Or, Sc, Pe - one,
        [Or, Pl, Le, Di], Me, Pe - one,
        [Me, Pe, Wr, Ba], [Pe, Pe],
        [Pe, Or, Da, Ki], Pl - one,
        [Pl, Pl, Re, Ki], Gr, Mu - one,
        [Gr, Sc, Wr, Ha], Mu, Or, [Me, Sc],
        [Mu, Gr, Le, St], Or, Me, Pe - one,
        [Or, Mu, Ca, St], Me, Pe, Pl - one,
        [Me, Or, Me, St], Pe, Pl, [Gr, St],

        [Pe, Or, Ro, Di], Pl - one,
        [Pl, Pl, Wr, St], Gr - one,
        [Gr, Pl, Wr, Ha], Mu, Or, [Me, Ha],
        [Mu, Pl, Re, Li], Or, Me, Pe, Pl, Gr,

    ]

    handsByPlayer = {Me: [Ha, Co, Sc], Pe: 3, Pl: 3, Gr: 3, Mu: 3, Or: 3}


    createBag(Me, handsByPlayer)  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> PP



def game2():
    Me = Pl

    events = [
        [Sc, Pl],
        [Pe, Ha],
        [Sc, Sc],
        [Or, Mu],

        [Me, Mu, Da, Di], Gr, [Mu, Di],
        [Gr, Gr, Da, Li], Mu, Or, Sc, Pe, [Me, Gr],
        [Mu, Pl, Da, Lo], Or, Sc - one,
        [Or, Sc, Da, Ha], Sc - one,
        [Sc, Or, Da, Ha], Pe - one,
        [Pe, Or, Ca, Ba], Me, Gr - one,

        [Me, Or, Ca, Lo], [Gr, Or],
        [Gr, Pe, Ca, Bi], Mu, Or, Sc, Pe - one,
        [Mu, Sc, Da, Ha], Or, Sc - one,
        [Or, Pl, Da, Ha], Sc - one,
        [Sc, Or, Da, Di], Pe, Me, Gr - one,
        [Pe, Mu, Da, Bi], Me, Gr, Mu, Or - one,

        [Me, Gr, Ro, Li], [Gr, Li],

    ]

    createBag(Me, [Gr, Ro, Lo], {Gr: 3, Mu: 3, Or: 3, Sc: 3, Pe: 3})  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> PP

def game3():
    Me = Pl

    events = [
        [Or, Ro],

        [Gr, Mu, Da, Bi], Or - one,
        [Or, Gr, Re, Ba], Pe - one,
        [Pe, Gr, Wr, Ki], [Me, Wr],
        [Me, Gr, Da, Ba], [Gr, Gr],

        [Gr, Pe, Le, Bi], Or, Pe - one,
        # Or misses a go
        [Pe, Sc, Da, Li], [Me, Sc],
        [Me, Pe, Le, Bi], Gr, Or, [Pe, Pe],

        [Gr, Gr, Ro, Li], Or - one,
        [Or, Pl, Wr, Di], Pe, [Me, Wr],
        [Pe, Pl, Le, Bi], Me, Gr, Or,

    ]

    createBag(Me, [St, Li, Di, Wr, Sc], {Gr: 5, Or: 4, Pe: 4})  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> PP

def game4():
    Me = Pl

    events = [
        [Gr, Pl, Da, Di], Or, Pe-one,
        [Or, Mu, Le, Bi], Pe-one,
        [Pe, Mu, Wr, Ba], [Me, Mu],
        [Me, Sc, Da, Di], Gr, [Or, Sc],

        [Gr, Pe, Le, Ba], Or, Pe-one,
        [Or, Gr, Ro, Li], Pe, [Me, Gr],
        [Pe, Gr, Da, Ki], [Me, Gr],
        [Me, Pl, Da, Di], Gr, Or, [Pe, Pl],

        [Gr, Or, Re, St], Or-one,
        [Or, Mu, Wr, St], Pe, [Me, Mu],
        [Pe, Or, Da, Di], Me, Gr, Or,

    ]

    createBag(Me, [Lo, Wr, Pe, Mu, Gr], {Gr: 5, Or: 4, Pe: 4})  \
        >> figureKnown >> events  \
        >> processResponses >> events  \
        >> PP

    #                                   Me          Green       Orchid      Peacock
    # Green            -                   X           -           -           -
    # Mustard          -                   X           -           -           -
    # Orchid           X                   -           -           -           -
    # Peacock          -                   X           -           -           -
    # Plum             -         L1        -           -           -           X L1
    # Scarlet          -                   -           -           X           -
    # ----
    # Candlestick        4                 -           ?           ?           ?
    # Dagger             2    S2 L1     2  -        1  -           -        2  ? L1
    # Lead Pipe          3    S1 L4        -        1  ?        1  -           ? L4
    # Revolver           4    S1 L2        -        1  ?           ? L2        ?
    # Rope               3    S1           -           ?        1  ?           -
    # Wrench           -                   X           -           -           -
    # ----
    # Kitchen            4    S1           -           ?           ?        1  ?
    # Ballroom           3    S2 L2        -        1  ?           -        1  ? L2
    # Conservatory       4                 -           ?           ?           ?
    # Billiard Room      4    S1 L2        -           ?        1  ?           ? L2
    # Library            3    S1           -           ?        1  ?           -
    # Study              3    S2 L2        -        1  ?        1  ? L2        -
    # Hall               4                 -           ?           ?           ?
    # Lounge           -                   X           -           -           -
    # Dining Room        2    S1 L1     2  -        1  -           -        1  ? L1

def game5():
    Me = Pl
    events = [

        [Me, Gr, Re, Ba], [Gr, Ba],
        [Gr, Mu, Re, Ki], Or - one,
        [Or, Or, Ro, Lo], Pe - one,
        [Pe, Gr, Da, Co], [Me, Da],

        [Me, Or, Wr, Co], Gr, Or, [Pe, Or],
        [Gr, Sc, Ca, Ki], Or, Pe, [Me, Ca],
        [Or, Pe, Ro, Ba], Pe, Me, Gr - one,
        [Pe, Mu, Re, Co], Me, Gr, Or - one,

        [Me, Sc, Wr, Bi], [Gr, Bi],         # Sc, Wr, Co
        [Gr, Sc, Le, Ba], Or, Pe, [Me, Le],
        [Or, Pe, Re, Co], Pe, Me, Gr,   # won

    ]

    like = {0:100, 1:10, 2:5, 3:0}
    bag = createBag(Me, [Ki, Di, Le, Da, Ca], {Gr: 5, Or: 4, Pe: 4}) \
        >> figureKnown >> events \
        >> processResponses >> events \
        >> processSuggestions(_, _, like) >> events
    bag >> PP;

def main():
    # game1()
    t1 = datetime.datetime.now()
    game5()
    t2 = datetime.datetime.now()
    f'\n{(t2 - t1).microseconds / 1000}ms' >> PP

    import coppertop._singletons
    f'{int(coppertop._singletons._numNotCopied / (coppertop._singletons._numNotCopied + coppertop._singletons._numCopies)*100)}%' >> PP

    # totalCombs =
    #     num(people) - num(my people) - num(TBI people)
    #     * num(weapons) - num(my weapons) - num(TBI weapons)
    #     * num(rooms) - num(my rooms) - num(TBI rooms)
    #     * perms (remaining cards, num other players)

if __name__ == '__main__':
    main()
