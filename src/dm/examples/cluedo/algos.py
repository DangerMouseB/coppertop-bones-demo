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
from dm.core import equal, keys, tvstruct, count, atPut, join, drop, each, select, dropAll, combinations, \
    nCombinations, to, append, joinAll, pair, intersects, PP
from dm.core.types import void
from bones.core.errors import ProgrammerError, UnhappyWomble
from bones.core.sentinels import Missing
from ribs.types import txt, pylist, pydict, index, N, pyset, num
from bones.lang.metatypes import BTStruct, BTPrimitive

from dm.examples.cluedo.core import cluedo_bag, YES, NO, MAYBE, TBI, HasOne
from dm import pmf
from .cards import people, weapons, rooms, Card
from .utils import minus, only, countIf, aside, Void



# we track all possible card locations (state is YES, NO or MAYBE) for the following:
#  - the hand of the player (whose pad this is),
#  - the hand to be inferred TBI,
#  - the hand of each opponent
# we track suggestions and responses as lists in each hand (i.e. without aggregating them)


ndmap = BTPrimitive('ndmap')

#SHOULDDO these are currently ficticious and need implementing
possibleHand = (N**txt)[pyset]['possibleHand']
cell = BTStruct(
    state=txt,
    suggestions=pylist,
    prior=num,
    posterior=num
)
handTracker = BTStruct(
    ys=(N**txt)[pyset],
    ns=(N**txt)[pyset],
    ms=(N**txt)[pyset],
    combs=N**possibleHand,      # this is a shame - {{1,2},{1,3}} -> TypeError: unhashable type: 'set'
    prior=(N**txt)**(num),
    posterior=(N**txt)**(num),
)
_cluedo_bag = BTStruct(
    handId=txt,
    hand=(N**txt)[pylist],
    sizeByHandId=(txt**index)[pydict],
    pad=(txt**(txt**cell))[ndmap],
    trackerByHandId=(txt**handTracker)[pydict],
    otherHandIds=(N**txt)[pylist],
)



@coppertop(style=binary)
def figureKnown(bag:cluedo_bag, events) -> cluedo_bag:
    _.pad = bag.pad
    bag.pad = Missing
    handId = bag.handId
    _.handIds = bag.sizeByHandId >> keys

    # extract everything known from history (starting with this players hand which we convert into event format)
    _.suggestionId = 1

    hId, pe, we, ro = Missing, Missing, Missing, Missing

    for ev in bag.hand >> each >> (lambda c: [handId, c]) >> join >> events:

        if isinstance(ev, list) and len(ev) == 4:
            hId, pe, we, ro = ev            # the current suggestion state
            _.pad[pe][hId].suggestions.append(_.suggestionId)
            _.pad[we][hId].suggestions.append(_.suggestionId)
            _.pad[ro][hId].suggestions.append(_.suggestionId)
            _.suggestionId += 1

        elif ev >> typeOf >> equal >> HasOne:
            pass  # leave for second pass

        # if a card location is known to be YES in one handId it must be NO in all other handIds
        elif isinstance(ev, list) and len(ev) == 2:
            hId, c = ev
            ensureDefinitely(c, hId, YES)
            _.handIds >> drop >> hId >> each >> ensureDefinitely(c, _, NO)        # mark other hands as definite NOs

        # the player indicated they don't have a match with the suggestion - thus we know three NOs
        else:
            hId = ev
            (pe, we, ro) >> each >> ensureDefinitely(_, hId, NO)


    del _.suggestionId       # pop ctx

    hId, pe, we, ro = Missing, Missing, Missing, Missing


    # run the inference rules

    _.changed = True
    while _.changed:
        _.changed = False

        # check each handId to see if the YES count equals the hand size - if so mark any MAYBEs as NO
        # should we do the reverse rule?
        _.allYesCardsNotInTBI = []
        for hId in _.handIds:
            # two outputs - the count (which we use to determine if a hand is fully known) and which hand a known card is in
            yesCount = 0
            for c in _.pad >> keys:
                if _.pad[c][hId].state == YES:
                    yesCount += 1
                    if hId != TBI:
                        _.allYesCardsNotInTBI.append(c)
            if yesCount == bag.sizeByHandId[hId]:
                _.pad >> keys >> each >> ensureDefinitely(_, hId, NO)
            elif yesCount > bag.sizeByHandId[hId]:
                raise UnhappyWomble()

        # for each card check if all hands but one have NO - in which case the remaining one must be a YES
        for c in _.pad >> keys:
            noHands = _.handIds >> select >> (lambda hId: _.pad[c][hId].state == NO)
            remaining = set(_.handIds) >> minus >> noHands
            if len(remaining) == 1:
                remaining >> only >> ensureDefinitely(c, _, YES)

        # for each group in the TBI hand, check:
        #   - for a single YES - if found, others must be NO
        #   - if all but one are NO - if so, the remaining one is a YES
        (people, weapons, rooms) >> each >> checkAndUpdateTbiHand

        # for each group if we know the location of all but one card (inspectable from hIdByYesCard) then we can
        # infer that the remaining card must be in TBI hand
        x = (people, weapons, rooms) >> each >> (lambda group: set(group) >> minus >> _.allYesCardsNotInTBI)
        x = x  \
            >> select >> (lambda remaining: remaining >> count == 1)  \
            >> each >> only  \
            >> aside >> (lambda cInferredInTBI:
                cInferredInTBI >> each >> ensureDefinitely(_, TBI, YES)
            )  \
            >> aside >> (lambda cInferredInTBI:
                cInferredInTBI >> each >> (lambda c:
                    _.handIds >> each >> ensureDefinitely(c, _, NO)
               )
            )

        del _.allYesCardsNotInTBI

    bag.pad = _.pad
    del _.pad
    del _.handIds
    del _.changed
    return bag


@coppertop
def checkAndUpdateTbiHand(group) -> void:
    # check the given group in the TBI hand for definite YES and definite NO
    yesCards = group >> select >> (lambda c: _.pad[c][TBI].state == YES)        # could merge these so loops only once
    noCount = group >> countIf >> (lambda c: _.pad[c][TBI].state == NO)
    if yesCards:
        if yesCards >> count > 1: raise UnhappyWomble()
        group >> dropAll >> yesCards >> each >> ensureDefinitely(_, TBI, NO)
    elif noCount == count(group) - 1:
        group >> each >> ensureDefinitely(_, TBI, YES)
    return Void


# for a function to match it must ensure ignore ctx inputs and outputs are met too
# it's not going to be super trivial to add however the improvement in readabilty will be worth it?
@coppertop #(ctx=S(pad)) or could make a kwarg? ctx:S(pad=cluedo_pad)
def ensureDefinitely(c, hId, knownState) -> void: # * ctx(changed=bool, pad=cluedo_pad):
    if _.pad[c][hId].state == MAYBE:
        _.pad[c][hId].state = knownState        # <--- immutable update in the style of deep mutable update :)
        _.changed = True
    return Void


@coppertop(style=binary)
def processResponses(bag:cluedo_bag, events:pylist) -> cluedo_bag:
    # we can figure a prior from the responses where a player shows another player a held card
    _.pad = bag.pad
    _.trackerByHandId = bag.trackerByHandId
    bag.pad = Missing
    bag.trackerByHandId = Missing
    handId = bag.handId

    for hId in bag.otherHandIds:
        ys, ns, ms = _.pad >> yesNoMaybesFor(_, hId)
        # (ys, ns, ms) >> each >> count >> PP
        numUnknowns = bag.sizeByHandId[hId] - (ys >> count) #>> PP
        _.trackerByHandId[hId].combs = ms >> combinations >> numUnknowns
        _.trackerByHandId[hId].ys = ys
        _.trackerByHandId[hId].ns = ns
        _.trackerByHandId[hId].ms = ms
        # _.trackerByHandId[hId >> PP].combs >> count >> PP

    for ev in events:
        if isinstance(ev, list) and len(ev) == 4:
            accuser, pe, we, ro = ev
            suggestion = (pe, we, ro)
        elif ev >> typeOf >> equal >> HasOne:
            respondant = ev.handId
            ys = _.trackerByHandId[respondant].ys
            ms = _.trackerByHandId[respondant].ms
            ns = _.trackerByHandId[respondant].ns
            if _.trackerByHandId[respondant].ys.intersection(suggestion):
                f'We know {respondant} has {_.trackerByHandId[respondant].ys.intersection(suggestion)}' >> PP
                #suggestion intersects with a card we know the respondant has so no additional information
                pass
            else:
                possibleCards = _.trackerByHandId[respondant].ms.intersection(suggestion)
                if len(possibleCards) == 1:
                    # We've determined a player definitely has a certain card. This means this information needs
                    # adding to the knowns and the previous inference up to this point needs redoing
                    # for the moment print the data and throw an error so the user can add it to the events list
                    f'{respondant} has {possibleCards}' >> PP
                    1 / 0
                else:
                    # we are left with 2 or 3 possible cards the player has so filter the hand combinations
                    newCombs = _.trackerByHandId[respondant].combs \
                        >> select >> (lambda comb: comb >> intersects >> possibleCards)
                    f'{respondant}: {_.trackerByHandId[respondant].combs >> count} -> {newCombs >> count}' >> PP
                    _.trackerByHandId[respondant].combs = newCombs

    # as a temporary stop gap let's put the prob into the score - later we'll do the prior and update the PP code
    for hId in bag.otherHandIds:
        combs = _.trackerByHandId[hId].combs
        nCombs = combs >> count
        # for c in _.pad >> keys:
        #     p = 0
        #     for comb in combs:
        #         if c in combs:
        #             p += _.trackerByHandId[hId].posterior[comb]
        #     _.pad[c][hId].prior = p
        # _.trackerByHandId[hId].prior = combs >> pair >> ([1] * nCombs) >> to(_, pydict)
        _.trackerByHandId[hId].posterior = combs >> pair >> ([1] * nCombs) >> to(_, pydict)

    bag.pad = _.pad
    bag.trackerByHandId = _.trackerByHandId
    del _.pad
    del _.trackerByHandId
    return bag


@coppertop(style=binary)
def processSuggestions(bag:cluedo_bag, events:pylist, like:pydict) -> cluedo_bag:
    _.pad = bag.pad
    _.trackerByHandId = bag.trackerByHandId
    bag.pad = Missing
    bag.trackerByHandId = Missing

    for ev in events:
        if isinstance(ev, list) and len(ev) == 4:
            accuser, pe, we, ro = ev
            if accuser != bag.handId:
                suggestion = set([pe, we, ro])
                combs = _.trackerByHandId[accuser].combs
                for comb in combs:
                    overlap = suggestion.intersection(comb)
                    _.trackerByHandId[accuser].posterior[comb] = \
                        _.trackerByHandId[accuser].posterior[comb] * like[len(overlap)] #>> PP

    # divide by P(data)
    for hId in bag.otherHandIds:
        sum = 0
        for comb in _.trackerByHandId[hId].combs:
            sum += _.trackerByHandId[hId].posterior[comb]
        sum >> PP
        for comb in _.trackerByHandId[hId].combs:
            p = _.trackerByHandId[hId].posterior[comb] / sum
            _.trackerByHandId[hId].posterior[comb] = p
            # _.trackerByHandId[hId].posterior[comb] >> PP
        # _.trackerByHandId[hId].posterior >> PPPost

    # as a temporary stop gap let's put the prob into the score - later we'll do the prior and update the PP code
    for hId in bag.otherHandIds:
        combs = _.trackerByHandId[hId].combs
        nCombs = combs >> count
        for c in _.pad >> keys:
            p = 0
            for comb in combs:
                if c in comb:
                    p += _.trackerByHandId[hId].posterior[comb]
            _.pad[c][hId].posterior = p #>> PP
        # _.trackerByHandId[hId].prior = combs >> pair >> ([1] * nCombs) >> to(_, pydict)
        # _.trackerByHandId[hId].posterior = combs >> pair >> ([1] * nCombs) >> to(_, pydict)

    bag.pad = _.pad
    bag.trackerByHandId = _.trackerByHandId
    del _.pad
    del _.trackerByHandId

    return bag

@coppertop
def PPPost(pByComb):
    for k, v in pByComb.items():
        f'{k} -> {v}' >> PP

@coppertop
def yesNoMaybesFor(pad, hId):
    ys, ns, ms = set(), set(), set()
    for c in pad >> keys:
        s = pad[c][hId]
        if s.state == YES:
            ys.add(c)
        elif s.state == NO:
            ns.add(c)
        elif s.state == MAYBE:
            ms.add(c)
        else:
            raise ProgrammerError()
    return ys, ns, ms


@coppertop
def createBag(handId:Card, hand:pylist, otherHandSizesById:pydict) -> cluedo_bag:

    sizeByHandId = {TBI:3} \
        >> atPut(_, handId, hand >> count) \
        >> join >> otherHandSizesById

    handsToTrack = sizeByHandId >> keys

    # SHOULDDO replace these with struct creation
    @coppertop
    def newPadCell(c, hId):
        return tvstruct(state=MAYBE, suggestions=[], prior=0, posterior=0)

    def newHandTracker(hId):
        return tvstruct(ys=Missing, ns=Missing, ms=Missing, combs=Missing, prior=Missing)

    @coppertop
    def newRow(c, hIds):
        return hIds >> pair >> (hIds >> each >> newPadCell(c, _)) >> to(_,pydict)

    cards = (people, weapons, rooms) >> joinAll
    pad = cards >> pair >> (cards >> each >> newRow(_, handsToTrack)) >> to(_, pydict)
    # in bones we should certainly be able to tell the difference between a list of tuples and a tuple of lists (i.e. a
    # product of exponentials and a exponential of products) even if we can't in python very easily

    otherHandIds = otherHandSizesById >> keys
    trackerByHandId = otherHandIds >> pair >> (otherHandIds >> each >> newHandTracker) >> to(_, pydict)

    return tvstruct(cluedo_bag,
        handId=handId,
        hand=hand,
        sizeByHandId=sizeByHandId,
        pad=pad,
        trackerByHandId=trackerByHandId,
        otherHandIds=otherHandIds,
    )

_cluedo_bag.setConstructor(createBag)
