import crocodile as cc

J = 11
Q = 12
K = 13
A = 1


def make_hand_array(i):
    try:
        i = i.replace('K', '13')
        i = i.replace('Q', '12')
        i = i.replace('J', '11')
        i = i.replace('A', '1')
        hand = list(map(int, i.split(',')))
        for card in hand:
            if card > 13:
                print('card value', card, 'is too high!',)
                raise ValueError
        return hand
    except:
        print('hey you messed up, try again!')
        return None

hand = None

while True:
    try:
        i = input('\nwhat to do? ')
        if i == 'exit':
            break
        elif 'hand ' in i:
            i = i.replace('hand ', '')
            hand = make_hand_array(i)
        elif 'score' in i:
            i = i.replace('score ', '')
            if hand:
                cc.score_hand(hand, True)
            else:
                print('you need to type in a valid hand!')
        elif 'crib?' in i:
            i = i.replace('crib? ', '')
            ncrib = int(i)
            cc.card_to_remove(hand, ncrib)
        elif 'crib ' in i:
            i = i.replace('crib ', '')
            cribbed = make_hand_array(i)
            if hand:
                allinhand = True
                for card in cribbed:
                    if card not in hand:
                        print('card', card, ' is not in your hand!')
                        allinhand = False
                if allinhand:
                    for card in cribbed:
                        idx = hand.index(card)
                        del hand[idx]
            else:
                print('you need to type in a valid hand!')
        elif 'hand?' in i:
            print(hand)
        elif '' in i:
            print(hand)
        else:
            print('available commands are:')
            print('- hand [cards]')
            print('- score')
            print('- give [num]')
            print('- crib [cards]')
            print('- show')
            raise NameError('You messed up!')
    except NameError:
        print('caught a messup, try again')
    print('\n\n')
