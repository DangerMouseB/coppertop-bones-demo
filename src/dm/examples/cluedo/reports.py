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

from coppertop.pipe import *
from dm.core import keys, each, count, tvseq, to, tvstruct, first, values, append, join, joinAll, drop, \
    interleave, pad as padWith
from ribs.types import txt, N, pylist, pydict

from .core import cluedo_pad, YES, NO, MAYBE, TBI
from .utils import display_table, hjoin
from .cards import *


# coercers - # OPEN: can these be sensibly defaulted in metatypes or templated?
(Card^txt).setCoercer(anon)
(N**Card)[tvseq].setCoercer(tvseq)


@coppertop
def ppCell(cell, stat, cfg):
    txtSuggest = ('' if stat.tbi != MAYBE else (str(cell.suggestions >> count) if cell.suggestions else "")) >> padWith(_, 2)
    txtState = cell.state #(YES if cell.state == YES else ' ') if stat.tbi == YES else cell.state
    txtLike = f'{int(cell.posterior._target * 100)}%' if cell.posterior else ''
    return f'{txtSuggest} {txtState} {txtLike}' >> padWith(_, cfg.cellWidth)


@coppertop
def ppCardSummary(card, player, pad, stats, cfg, cHands):
    t1 = ('' if stats[card].tbi == MAYBE else stats[card].tbi) >> padWith(_, left=cfg.hasWidth)
    t2 = ('' if stats[card].tbi in (YES, NO) else str(cHands - stats[card].noCount)) >> padWith(_, left=cfg.noCountWidth)
    t3 = (f'S{stats[card].sumMaybeSuggests}' if stats[card].sumMaybeSuggests else '') >> padWith(_, left=cfg.suggestCountWidth)
    t4 = (f'{int(stats[card].mulPriors * 100)}%' if stats[card].mulPriors else '') >> padWith(_, left=cfg.likeWidth)
    return t1 + t2 + t3 + t4


@coppertop
def rep1(pad:cluedo_pad, handId:Card) -> display_table:
    cfg = tvstruct(nameWidth=17, cellWidth=12, hasWidth=2, noCountWidth=5, suggestCountWidth=3, likeWidth=7)

    handIds = (pad >> values >> first >> keys >> to(_, pylist) | (N**Card)[tvseq]) >> drop >> TBI

    titlesPadding = ' ' * (cfg.nameWidth + cfg.hasWidth + cfg.noCountWidth + cfg.suggestCountWidth + cfg.likeWidth)
    tTitle = [titlesPadding + (
        handIds
            >> each >> ((lambda hId: ('Me' if hId == handId else repr(hId)) >> padWith(_, left=cfg.cellWidth)) | Card^txt)
            >> joinAll
    )] | display_table

    tNames = (people, weapons, rooms)  \
        >> each >> (lambda cards: cards >> each >> str) \
        >> interleave >> ['----']  \
        >> each >> (lambda c: c >> padWith(_, left=cfg.nameWidth)) | display_table

    # show TBI, countHands - noCount, sum priors, sum suggests
    stats = genStats(pad, handId)

    cHands = handIds >> count   # i.e. the number of players in the game, the number of hands less the TBI hand
    tSummary = (people, weapons, rooms)  \
        >> each >> (lambda g: g
            >> each >> (lambda c: c
                >> ppCardSummary(_, handId, pad, stats, cfg, cHands)
            )
        )  \
        >> interleave >> ['']  \
        >> each >> (lambda c: c >> padWith(_, left=cfg.nameWidth))  \
        | display_table

    tHands = (people, weapons, rooms)  \
        >> each >> (lambda g: g
            >> each >> (lambda c: handIds  \
                >> each >> ((lambda hId:  \
                    pad[c][hId] >> ppCell(_, stats[c], cfg)
                ) | Card^txt)
                >> joinAll
            )
        )  \
        >> interleave >> ['']  \
        >> each >> (lambda c: c >> padWith(_, left=cfg.nameWidth))  \
        | display_table

    return tTitle >> join >> (tNames >> hjoin >> tSummary >> hjoin >> tHands | display_table)


@coppertop
def ppFnOfCard(fn, sep='') -> display_table:
    return tvseq(display_table,
        people >> each >> fn >> append >> sep
        >> join >> (weapons >> each >> fn >> append >> sep)
        >> join >> (rooms >> each >> fn)
    )


@coppertop
def genStats(pad:pydict, handId) -> tvstruct:
    stats = tvstruct()
    handIds = pad >> values >> first >> keys
    for c in pad >> keys:
        noCount = 0
        sumMaybeSuggests = 0
        mulPriors = 0
        for hId in handIds:
            if hId == TBI or hId == handId:
                continue
            else:
                e = pad[c][hId]
                noCount += e.state == NO
                sumMaybeSuggests += e.suggestions >> count if e.state == MAYBE else 0
                mulPriors += e.posterior if e.state == MAYBE else 0
        stats[c] = tvstruct(
            tbi=pad[c][TBI].state,
            noCount=noCount,
            sumMaybeSuggests=sumMaybeSuggests,
            mulPriors=mulPriors
        )
    return stats

