import random
from sys import argv

def getcard():
    suit = ['C', 'S', 'H', 'D'][random.randint(0, 3)]
    # 14 is an ace, 13 king
    card = random.randint(2, 14)
    
    return (card, suit)

def gethand():
    hand = []
    while len(hand) < 5:
        c = getcard()
        if c not in hand:
            hand.append(c)
    return hand

# sorting function to make comparisons later
def sorthand(hand):
    hand.sort(lambda x, y: cmp(x[0],y[0]))
    return hand

# groups equal ranked cards together
def groupequal(hand):
    prts = []
    val = None
    for card in hand:
        if val and card[0] == val: 
            prt.append(card)
        elif val:
            prts.append(prt)
            prt = [card]
            val = card[0]
        else:
            prt = [card]
            val = card[0]
    prts.append(prt)
    return prts

def ofkind(num, hand):
    # partition the hand and see how many groups we get
    prts = groupequal(hand)

    for prt in prts:
        if len(prt) == num: return True
    return False

# all these assume hand is sorted
def royalflush(hand):
    suit = None
    for hand, rank in zip(hand, range(10, 15)):
        if hand[0] != rank: return False
        if suit and hand[1] != suit: return False
        suit = hand[1]
    return True

def straight(hand):
    lastcard = None
    for card in hand:
        if lastcard and lastcard[0] != card[0]-1: return False
        lastcard = card
    return True
    
def flush(hand):
    lastcard = None
    for card in hand:
        if lastcard and lastcard[1] != card[1]: return False
        lastcard = card
    return True

def straightflush(hand):
    return straight(hand) and flush(hand)

def ofkind4(hand):
    return ofkind(4, hand)

def ofkind3(hand):
    return ofkind(3, hand)

def pair(hand):
    return ofkind(2, hand)

def fullhouse(hand):
    # partition the hand and see how many groups we get
    prts = groupequal(hand)

    return len(prts) == 2 and \
           (len(prts[0]) == 2 and len(prts[1]) == 3) or \
           (len(prts[0]) == 3 and len(prts[1]) == 2)

def pair2(hand):
    # partition the hand and see how many groups we get
    prts = groupequal(hand)
    numpair = 0
    for prt in prts:
        if len(prt) == 2: numpair += 1
        if numpair == 2: return True
    return False

# function to evaluate the hand
def evalhand(hand):
    hand = sorthand(hand)
    # ordering is important since many hands overlap but we take most valuable
    if royalflush(hand): return 250
    elif straightflush(hand): return 50
    elif ofkind4(hand): return 25
    elif fullhouse(hand): return 9
    elif flush(hand): return 6
    elif straight(hand): return 4
    elif ofkind3(hand): return 3
    elif pair2(hand): return 2
    elif pair(hand): return 1
    else: return 0

if __name__ == '__main__':

    numhands = 100000
    if(len(argv)>1):
        numhands = int(argv[1])

    # hands for testing
    #rf = [(10, 'D'), (11, 'D'), (12, 'D'), (13, 'D'), (14, 'D')]
    #sf = [(8, 'D'), (9, 'D'), (11, 'D'), (12, 'D'), (10, 'D')]
    #pr = [(8, 'D'), (8, 'H'), (9, 'D'), (12, 'D'), (13, 'D')]
    #fh = [(8, 'D'), (8, 'H'), (9, 'D'), (9, 'H'), (9, 'S')]
   
    for i in range(numhands):
        h = gethand()
        print evalhand(h)


