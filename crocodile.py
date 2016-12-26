import itertools as it
import numpy as np
import collections as co
import copy as copy


def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in iter(range((len(lst)-n+1))))


def score_hand(hand, verbose=False):

    hand = np.sort(hand)

    scores = {}

    pairscores = []

    pairscore = sum(map(lambda p: 2*int(p[0] == p[1]), it.combinations(hand, 2)))
    for pair in it.combinations(hand, 2):
        if pair[0] == pair[1]:
            pairscores.append(pair)
    scores['pairs'] = pairscores

    fifteenscores = []
    fifteenscore = 0
    for numcards in np.arange(2, len(hand)+1):
        for combo in it.combinations(hand, numcards):
            npcombo = np.array(combo)
            npcombo[np.where(npcombo > 10)] = 10
            if np.sum(npcombo) == 15:
                fifteenscores.append(combo)
            fifteenscore += 2 * int(np.sum(npcombo) == 15)
    scores['15s'] = fifteenscores

    rundict = {}
    for runlength in np.arange(3, len(hand)+1):
        ncardruns = []
        for sequence in it.combinations(hand, runlength):
            isrun = False
            for idx in np.arange(0, runlength-1):
                if sequence[idx+1] != sequence[idx]+1:
                    isrun = False
                    break
                if idx == runlength-2:
                    isrun = True
            if isrun:
                ncardruns.append(sequence)
        if ncardruns:
            rundict[runlength] = ncardruns

    sortedrundict = co.OrderedDict(sorted(rundict.items()))

    for runlength in list(sortedrundict.keys())[:-1]:
        runNlist = sortedrundict[runlength]
        runNp1list = sortedrundict[runlength+1]
        for idx, runN in enumerate(runNlist):
            for runNp1 in runNp1list:
                if contains_sublist(runNp1, runN):
                    sortedrundict[runlength][idx] = []

    runscore = 0
    runscores = []
    for length, value in sortedrundict.items():
        for run in value:
            if run:
                runscore += length
                runscores.append(run)
    scores['runs'] = runscores

    totalscore = pairscore + fifteenscore + runscore

    if verbose:
        print('\nhand:', hand, '\n')
        print('pairs: ', pairscore)
        print('15s  : ', fifteenscore)
        print('runs : ', runscore)
        print('total: ', totalscore, 'points\n')

        for item in scores.items():
            print(item)

    return totalscore, pairscore, fifteenscore, runscore


def unit_test(hand, tsx, psx, fsx, rsx, testname):
    ts, ps, fs, rs = score_hand(hand, False)
    status = ts == tsx and ps == psx and fs == fsx and rs == rsx
    if testname:
        if status:
            print('- pass', testname)
        else:
            print('- fail', testname)
    return status


def run_unit_tests():
    J = 11
    Q = 12
    K = 13
    A = 1

    ok = True

    ok = ok and unit_test([3, 4, 7], 0, 0, 0, 0, 'null')

    ok = ok and unit_test([A, A], 2, 2, 0, 0, 'single pair')
    ok = ok and unit_test([A, A, A], 6, 6, 0, 0, 'single triple')
    ok = ok and unit_test([A, A, A, A], 12, 12, 0, 0, 'single quad')

    ok = ok and unit_test([10, 5], 2, 0, 2, 0, 'single fifteen 5-10')
    ok = ok and unit_test([13, 5], 2, 0, 2, 0, 'single fifteen 5-K')
    ok = ok and unit_test([5, 5, 5], 8, 6, 2, 0, 'single fifteens 5-5-5')
    ok = ok and unit_test([10, 5, 5], 6, 2, 4, 0, 'two fifteens 5-5-10')
    ok = ok and unit_test([13, 5, 5], 6, 2, 4, 0, 'two fifteens 5-5-K')

    ok = ok and unit_test([A, 2, 3], 3, 0, 0, 3, 'A 3-card run')
    ok = ok and unit_test([A, 2, 3, 4], 4, 0, 0, 4, 'A 4-card run')
    ok = ok and unit_test([A, 2, 3, 4, 5], 7, 0, 2, 5, 'A 5-card run')

    ok = ok and unit_test([A, 2, 3, 6, 7, 8], 12, 0, 6, 6, '2 separate 3-card runs')
    ok = ok and unit_test([A, 2, 3, 3], 8, 2, 0, 6, 'double 3-card run')

    ok = ok and unit_test([A, 2, 3, 4, 4], 10, 2, 0, 8, 'double 4-card run A2344')
    ok = ok and unit_test([A, 2, 3, 3, 4], 10, 2, 0, 8, 'double 4-card run A2334')

    ok = ok and unit_test([0, 0, A, 2, 3, 4], 12, 2, 0, 10, 'double 5-card run')

    ok = ok and unit_test([5, 5, 10, 10, J, J, Q, K, K], 68, 8, 28, 32,
                          'crazy hand: 5-5-A0-A0-J-J-Q-K-K')

    ok = ok and unit_test([A, A, A, A, 4, 4, 4, 10], 50, 18, 32, 0,
                          'crazy hand: A-A-A-A-4-4-4-A0')

    ok = ok and unit_test([A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K], 71, 0, 58, 13,
                          'crazy hand: A-->K')

    if ok:
        print('\nPASS\n\n')
    else:
        print('\nFAIL\n\n')

    return ok


def card_to_remove(deal, numtogive):
    print('dealt the hand:', deal, '\n')
    giveupdict = {}
    for cards in it.combinations(deal, numtogive):
        hand = copy.deepcopy(deal)
        for card in cards:
            hand.remove(card)
        ts, ps, fs, rs = score_hand(hand, False)
        giveupdict[cards] = ts

    sortedlist = sorted(giveupdict.items(), key=lambda x: x[1])

    for (giveup, points) in reversed(sortedlist):
        print('give up', giveup, 'to get', points, 'points')