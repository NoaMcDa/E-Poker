import string, math, random
import tkinter

from PIL import ImageTk, Image

RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
  # has to have user and money
users = {"Amy": "11"}
SUITS = ('S', 'D', 'H', 'C')


def cutCard(location, CardDeck):
    x, y = location
    left = x
    right = x + 100
    top = y
    bottom = y + 130

    card = CardDeck.crop((left, top, right, bottom))
    card = ImageTk.PhotoImage(card)

    return card


class Player(object):

    def __init__(self,hand,money,name,currect_bet,fold):
        self.hand = hand
        self.money = money
        self.name = name
        self.currect_bet = currect_bet
        self.fold = fold

    def canbet(self):
        if self.money >0:
            return True
        return False
    def bet(self, money):
        if (self.canbet()):
            if (self.money > money):
                self.money -= money
            else:
                self.money = 0
            self.currect_bet += money
        else:
            print("cant bet anymore")

    def clean_bets (self):
        self.currect_bet = 0

    def folds(self):
        self.fold = True
class Card(object):
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

    SUITS = ('S', 'D', 'H', 'C')

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        if self.rank == 14:
            rank = 'A'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 11:
            rank = 'J'
        else:
            rank = self.rank
        return str(rank) + self.suit

    def __eq__(self, other):
        return (self.rank == other.rank)

    def __ne__(self, other):
        return (self.rank != other.rank)

    def __lt__(self, other):
        return (self.rank < other.rank)

    def __le__(self, other):
        return (self.rank <= other.rank)

    def __gt__(self, other):
        return (self.rank > other.rank)

    def __ge__(self, other):
        return (self.rank >= other.rank)


class Deck(object):  # creating deck of 54 cards
    Cards = []

    def __init__(self):
        self.deck = {}
        self.xDeck = 0
        self.yDeck = 0
        for suit in Card.SUITS:  # creating sorted deck
            for rank in Card.RANKS:
                card = (rank, suit)
                self.deck[card] = (self.xDeck, self.yDeck)
                self.xDeck += 100
            self.xDeck = 0
            self.yDeck += 140

    def shuffle(self):
        Cards = list(self.deck.keys())
        random.shuffle(Cards)  # shuffeling the cards
        NewDeck = {}
        i = 0
        for key in self.deck:
            NewDeck[Cards[i]] = self.deck[Cards[i]]
            i += 1
        self.deck = NewDeck
        """
        for key in self.deck:
            print (key , self.deck[key])
        """

    def __len__(self):
        return len(self.deck)

    def deal(self):
        Cards = list(self.deck.keys())
        if len(self) == 0:
            return None
        else:
            return (Cards[0], self.deck.pop(Cards.pop(0)))  # returns a tuple!!!


class Poker(object):  # the whole game mechanics
    global deck
    deck = Deck()

    def __init__(self, numHands):
        deck.shuffle()
        self.hands = []
        self.Players = []
        self.tlist = []  # create a list to store total_point
        self.savecards = {}
        self.flop = {}
        numCards_in_Hand = 2

        for i in range(numHands):  # serving cards to each player
            hand = {}
            card = (0, 'a')
            TheCard = (card, (0, 0))
            for j in range(numCards_in_Hand):
                TheCard = deck.deal()
                hand[TheCard[0]] = TheCard[1]
            player = Player(hand,1000,str(i),0,False) #change definition
            self.Players.append(player)
            self.hands.append(hand)

    def sortHand(self, hand):  # supposed to be 7 cards now
        cards = []
        for c in hand:
            cards.append((c[0], c[1]))
        cards = sorted(cards, reverse=True)
        newhand = {}
        for card in cards:
            newhand[card] = hand[card]

        return newhand

    def play(self):
        # needs to get early bets
        # if everyone is out the last hand wins
        self.flop = {}
        self.savecards = {}
        deck.shuffle()
        for i in range(len(self.hands)):
            hand = ''
            for card in self.hands[i]:
                hand = hand + str(card) + ' '
            print('Hand ' + str(i + 1) + ': ' + hand)

        self.StartRound(True)
        self.flop3()

    def manage_blinds(self):
        smallblind = 10
        bigblind = 20
        try:
            self.Players[0].bet(smallblind)

            self.Players[1].bet(bigblind)
        except:
            print("not enough players")

    def StartRound(self,bool):
        flag = False
        if (bool):
            self.manage_blinds()
            GameTurn = 2
        else:
            GameTurn = 0
        num_players = len(self.Players)
        while True:
            maxbet = self.find_max_bet()
            if (self.Players[GameTurn%num_players].fold == False):
                stop = self.manageBets(self.Players[GameTurn%num_players],maxbet)
            else:
                stop = False
            GameTurn +=1
            maxbet = self.find_max_bet()

            if (GameTurn>=num_players ):
                if stop:
                    flag = self.check_finish(maxbet)
                if flag:
                    break
    def check_finish(self,maxbet):
        '''
        checks if the turns are finished
        '''
        for player in self.Players:
            if (player.fold!= True):
                if (player.money > 0 and player.currect_bet != maxbet):
                    return False
        return True



    def manageBets(self,player,maxbet):
        '''
        getting the action from player
        '''
        actions = ["call","bet","fold","check"]

        if(player.money> 0):
            print("player {} current bet {}".format(player.name, player.currect_bet))
            if ( player.currect_bet==maxbet):

                actions.remove("call")
            else:
                actions.remove("check")
            boole =  self.client_respond(actions,player,maxbet)
        else:
            print("player %s doesnt have money" %player.name)

        return boole

    def client_respond(self,actions,player,maxbet):
        flag = True
        while flag:
            print(" player {}: {} {} or {} ?".format(player.name,actions[0],actions[1],actions[2]))
            response = input()
            data = response.split(" ")
            if data[0] in actions:
                if data[0] == "bet":
                    try:
                        if (maxbet*2 <= int(data[1])+player.currect_bet or player.money < maxbet*2):
                            player.bet(int(data[1])-player.currect_bet)
                            print("player {} betted {}".format(player.name, data[1]))
                            print(player.name, player.currect_bet)
                            flag = False
                        else:
                            print("needs to bet x2 from max bet which is %s or more." %maxbet)

                    except:
                        print("not a number try again")
                if data[0] == "call":
                    flag = False
                    player.bet(maxbet-player.currect_bet)
                    print("player {} called {}".format(player.name,player.currect_bet))
                if data[0] == "check":
                    flag = False
                    print("player %s check"  %player.name)
                    print(player.name, player.currect_bet)
                    return True
                if data[0] == "fold":
                    flag = False
                    print("player fold", player.name)
                    player.folds()


        return False


    def find_max_bet(self):
        maxbet = self.Players[0].currect_bet
        for player in self.Players:
            if (player.currect_bet > maxbet):
                maxbet = player.currect_bet

        return maxbet

    def clear_current_bets(self):
        for player in self.Players:
            player.clean_bets()

    def flop3(self):
        self.clear_current_bets()

        # if everyone is out the last hand wins
        flopnum = 3
        card = (0, 'a')
        TheCard = (card, (0, 0))
        for j in range(flopnum):
            TheCard = deck.deal()
            self.flop[TheCard[0]] = TheCard[1]
            print(TheCard[0], TheCard[1])

        self.StartRound(False)
        # needs to get bets
        self.flop4()

    def flop4(self):
        self.clear_current_bets()
        # if everyone is out the last hand wins
        flopnum = 1
        card = (0, 'a')
        TheCard = (card, (0, 0))
        for j in range(flopnum):
            TheCard = deck.deal()
            self.flop[TheCard[0]] = TheCard[1]
            print(TheCard[0], TheCard[1])
        # needs to get bets
        self.StartRound(False)
        self.flop5()

    def flop5(self):
        self.clear_current_bets()
        # if everyone is out the last hand wins
        flopnum = 1
        card = (0, 'a')
        TheCard = (card, (0, 0))
        for j in range(flopnum):
            TheCard = deck.deal()
            self.flop[TheCard[0]] = TheCard[1]
            print(TheCard[0], TheCard[1])

        self.StartRound(False)

        for hand in self.hands:
            cards = list(hand.keys())
            for c in cards:
                self.savecards[c] = hand[c]
        for hand in self.hands:
            for card in self.flop:
                hand[card] = self.flop[card]
            self.sortHand(hand)
            # needs to get bets
            self.isRoyal(hand)

    def point(self, hand):  # point()function to calculate partial score - needs to be AT THE END
        sortedHand = sorted(hand, reverse=True)
        c_sum = 0
        ranklist = []
        for card in sortedHand:
            ranklist.append(card.rank)
        c_sum = ranklist[0] * 13 ** 4 + ranklist[1] * 13 ** 3 + ranklist[2] * 13 ** 2 + ranklist[3] * 13 + ranklist[4]
        return c_sum

    def isRoyal(self,
                hand):  # returns the total_point and prints out 'Royal Flush' if true, if false, pass down to isStraightFlush(hand)
        # add best hand
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 10
        Currank = 14

        index = 0
        for cardsuit in listcards:
            Cursuit = cardsuit[1]
            total_point = h * 13 ** 5
            royalflash = [(Currank, Cursuit), (Currank - 1, Cursuit), (Currank - 2, Cursuit), (Currank - 3, Cursuit),
                          (Currank - 4, Cursuit)]
            res = True
            for card in royalflash:
                if (card not in listcards):
                    res = False
                    break
            if (res == False):
                index += 1
            else:
                break
            if (index == 3):
                flag = False
                break
        if flag:
            print('Royal Flush')
            self.tlist.append(total_point)
        else:
            self.isStraightFlush(sortedHand)

    def isStraightFlush(self,
                        hand):  # returns the total_point and prints out 'Straight Flush' if true, if false, pass down to isFour(hand)
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 9
        index = 0
        for cardsuit in listcards:
            Cursuit = cardsuit[1]
            Currank = cardsuit[0]
            if (Currank != 14):
                straightFlush = [(Currank, Cursuit), (Currank - 1, Cursuit), (Currank - 2, Cursuit),
                                 (Currank - 3, Cursuit),
                                 (Currank - 4, Cursuit)]
                res = True
                for card in straightFlush:
                    if (card not in listcards):
                        res = False
                        break
            else:
                straightFlush = [(Currank, Cursuit), (2, Cursuit), (3, Cursuit), (4, Cursuit),
                                 (5, Cursuit)]
                res = True
                for card in straightFlush:
                    if (card not in listcards):
                        res = False
                        break
            total_point = h * 13 ** 5  # fix
            if (res == False):
                index += 1
            else:
                break
            if (index == 3):
                flag = False
                break
        if flag:
            print('Straight Flush')
            self.tlist.append(total_point)
        else:
            self.isFour(sortedHand)

    def isFour(self,
               hand):  # returns the total_point and prints out 'Four of a Kind' if true, if false, pass down to isFull()
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        flag = False
        h = 8
        index = 0
        total_point = h * 13 ** 5
        for currcard in listcards:
            Currank = currcard[0]
            Four = [(Currank, SUITS[0]), (Currank, SUITS[1]), (Currank, SUITS[2]), (Currank, SUITS[3])]
            res = True
            for i in range(len(Four)):
                if (Four[i] not in listcards):
                    res = False
                    break
            if (res == False):
                index += 1
            else:
                flag = True
                break
            if (index == 4):
                break
        if flag == False:
            self.tlist.append(total_point)

            self.isFull(sortedHand)
        else:
            flag = True
            print('Four of a Kind')
            # fix

    def isFull(self,
               hand):  # returns the total_point and prints out 'Full House' if true, if false, pass down to isFlush()
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 7
        isFullHouse = {}
        total_point = h * 13 ** 5  # fix
        for card in sortedHand:
            if card[0] in isFullHouse.keys():
                isFullHouse[card[0]] += 1
            else:
                isFullHouse[card[0]] = 1

        if (3 not in isFullHouse.values()):
            flag = False
            self.isFlush(sortedHand)
        else:
            count2 = 0
            count3 = 0
            for card in isFullHouse.keys():
                if (isFullHouse[card] == 3):
                    count3 += 1
                if (isFullHouse[card] == 2):
                    count2 += 1
            if (count3 == 1 and count2 < 1):
                flag = False
            else:
                flag = True
                # we need to get the highest ranks
            if (flag == True):
                print('Full House')
                self.tlist.append(total_point)
            else:
                self.isFlush(sortedHand)

    def isFlush(self,
                hand):  # returns the total_point and prints out 'Flush' if true, if false, pass down to isStraight()
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        h = 6
        IsFlush = {}
        flag = True
        total_point = h * 13 ** 5  # fix
        for card in listcards:
            if card[1] in IsFlush.keys():
                IsFlush[card[1]] += 1
            else:
                IsFlush[card[1]] = 1
        if 5 not in IsFlush.values() and 6 not in IsFlush.values() and 7 not in IsFlush.values():
            flag = False

        if flag:
            print('Flush')
            self.tlist.append(total_point)

        else:
            self.isStraight(sortedHand)

    def isStraight(self, hand):
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        listranks = []
        for card in listcards:
            listranks.append(card[0])

        flag = True
        h = 5
        total_point = h * 13 ** 5  # fix
        index = 0
        for card in listranks:

            if (card != 14):
                straight = [card, card - 1, card - 2, card - 3, card - 4]
                res = True
                for elem in straight:
                    if (elem not in listranks):
                        res = False
                        break
                if res == False:
                    index += 1
                else:
                    flag = True
                    break
            else:
                straight1 = [card, card - 1, card - 2, card - 3, card - 4]
                straight2 = [14, 2, 3, 4, 5]
                res1 = True
                res2 = True
                for elem in straight1:
                    if (elem not in listranks):
                        res1 = False
                        break
                for elem in straight2:
                    if (elem not in listranks):
                        res2 = False
                        break
                if (res1 == False and res2 == False):
                    index += 1
                else:
                    flag = True
                    break
            if (index == 3):
                flag = False
                break
        if flag:
            print('Straight')
            self.tlist.append(total_point)
        else:
            self.isThree(sortedHand)

    def isThree(self, hand):
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 4
        total_point = h * 13 ** 5
        isThree = {}
        total_point = h * 13 ** 5  # fix
        for card in sortedHand:
            if card[0] in isThree.keys():
                isThree[card[0]] += 1
            else:
                isThree[card[0]] = 1

        if (3 not in isThree.values()):
            flag = False
            self.isTwo(sortedHand)
        else:
            print("Three of a Kind")
            self.tlist.append(total_point)

    def isTwo(self, hand):  # returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 3
        total_point = h * 13 ** 5
        isTwoPair = {}
        for card in sortedHand:
            if card[0] in isTwoPair.keys():
                isTwoPair[card[0]] += 1
            else:
                isTwoPair[card[0]] = 1

        count2 = 0
        for card in isTwoPair.keys():
            if (isTwoPair[card] == 2):
                count2 += 1
        if (count2 < 2):
            flag = False
        else:
            flag = True
        if flag:
            print("Two Pair")
        else:
            self.isOne(sortedHand)

    def isOne(self, hand):  # returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 2
        total_point = h * 13 ** 5  # fixx
        isPair = {}
        for card in sortedHand:
            if card[0] in isPair.keys():
                isPair[card[0]] += 1
            else:
                isPair[card[0]] = 1

        count2 = 0
        for card in isPair.keys():
            if (isPair[card] == 2):
                count2 += 1
        if (count2 == 0):
            flag = False
            self.isHigh(sortedHand)
        else:
            flag = True
            print("One Pair")
            self.tlist.append(total_point)

    def isHigh(self, hand):  # returns the total_point and prints out 'High Card'
        sortedHand = self.sortHand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 1
        total_point = h * 13 ** 5  # fixx
        print("High Card")
        self.tlist.append(total_point)

    def EndGame(self):
        savedCard = list(self.savecards.keys())
        for card in savedCard:
            deck.deck[card] = self.savecards[card]
        for card in self.flop:
            deck.deck[card] = self.flop[card]
        deck.shuffle()
        self.hands = []
        self.tlist = []  # create a list to store total_point
        self.savecards = {}
        self.flop = {}


def main():

    Game = Poker(3)
    i = 0
    Game.play()
    Game.EndGame()
    print("\n \n")
    Game = Poker(3)


if __name__ == '__main__':
    main()
