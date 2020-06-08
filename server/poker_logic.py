import random

RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)
# has to have user and money
users = {"Amy": "11"}
SUITS = ('S', 'D', 'H', 'C')


def cut_card(location, card_deck):
    x, y = location
    left = x
    right = x + 100
    top = y
    bottom = y + 130

    card = card_deck.crop((left, top, right, bottom))
    card = ImageTk.PhotoImage(card)

    return card


class Player(object):
    def __init__(self, hand, money, name, correct_bet, fold):
        self.hand = hand
        self.money = money
        self.name = name
        self.correct_bet = correct_bet
        self.fold = fold

    def can_bet(self):
        return self.money > 0

    def bet(self, money):
        if self.can_bet():
            if self.money > money:
                self.money -= money
            else:
                # money = self.money # isn't this missing?
                self.money = 0  # ????????????????????????????????????????????
            self.correct_bet += money
        else:
            print("cant bet anymore")

    def clean_bets(self):
        self.correct_bet = 0

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
        return self.rank == other.rank

    def __ne__(self, other):
        return self.rank != other.rank

    def __lt__(self, other):
        return self.rank < other.rank

    def __le__(self, other):
        return self.rank <= other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __ge__(self, other):
        return self.rank >= other.rank


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
        random.shuffle(Cards)  # shuffling the cards
        NewDeck = {}
        i = 0
        for _ in self.deck:
            NewDeck[Cards[i]] = self.deck[Cards[i]]
            i += 1
        self.deck = NewDeck

        # for key in self.deck:
        #     print (key , self.deck[key])

    def __len__(self):
        return len(self.deck)

    def deal(self):
        Cards = list(self.deck.keys())
        if len(self) == 0:
            return None
        else:
            return Cards[0], self.deck.pop(Cards.pop(0))  # returns a tuple!!!

class GameState(object):
    """
    sending the client the gamestate, positions of all players and his turn, so we can present it in the graphics
    """
    def __init__(self,player,turn,end_game,array_players):
        self.turn = turn
        self.player = player
        self.end_game = end_game
        self.display_players = array_players
        """
    def arrange_positions(self,players):
        '''
        sending the client the current positions of each players on the gameboard
        supposed to work beacuse each player is on the players list
        '''
        DisplayPlayers = []
        for i in len(players):
            if players[i] == self.player:
                if (self.end_game):
                    for p in players:
                        if p != self.player:
                            DisplayPlayers.append(p)
                else:
                    for p in players:
                        if p != self.player:
                            p
                            DisplayPlayers.append(p)
                break
                
        return DisplayPlayers

    def myTurn(self):
        '''
        changing the turn
        '''
        self.turn = not self.turn
        
    def UpdateClientInfo(self):        
        '''
        sending the client himself, bool turn , and the arranged positions of the other players
        '''
        return self.player,self.turn,self.arrange_positions()
 """
class Poker(object):  # the whole game mechanics
    def __init__(self, num_hands):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.players = []
        self.tlist = []  # create a list to store total_point
        self.save_cards = {}
        self.flop = {}
        numCards_in_Hand = 2

        for i in range(num_hands):  # serving cards to each player
            hand = {}
            card = (0, 'a')
            the_card = (card, (0, 0))
            for j in range(numCards_in_Hand):
                the_card = self.deck.deal()
                hand[the_card[0]] = the_card[1]
            player = Player(hand, 1000, str(i), 0, False)  # change definition
            self.players.append(player)
            self.hands.append(hand)

    @staticmethod
    def sort_hand(hand):  # supposed to be 7 cards now
        cards = []
        for c in hand:
            cards.append((c[0], c[1]))
        cards = sorted(cards, reverse=True)
        new_hand = {}
        for card in cards:
            new_hand[card] = hand[card]

        return new_hand

    def play(self):
        # needs to get early bets
        # if everyone is out the last hand wins
        self.flop = {}
        self.save_cards = {}
        self.deck.shuffle()
        for i in range(len(self.hands)):
            hand = ''
            for card in self.hands[i]:
                hand = hand + str(card) + ' '
            print('Hand ' + str(i + 1) + ': ' + hand)

        self.start_round(True)
        self.flop3()

    def manage_blinds(self):
        small_blind = 10
        big_blind = 20
        try:
            self.players[0].bet(small_blind)
            self.players[1].bet(big_blind)
        except:  # TODO: catch the correct exception.
            print("not enough players")


    def start_round(self, game_beginning):
        flag = False
        if game_beginning:
            self.manage_blinds()
            GameTurn = 2
        else:
            GameTurn = 0
        num_players = len(self.players)
        while True:
            max_bet = self.find_max_bet()
            if not self.players[GameTurn % num_players].fold:
                stop = self.manage_bets(self.players[GameTurn % num_players], max_bet)
            else:
                stop = False
            GameTurn += 1
            max_bet = self.find_max_bet()

            if GameTurn >= num_players:
                if stop:
                    flag = self.check_finish(max_bet)
                if flag:
                    break

    def check_finish(self, max_bet):
        """
        checks if the turns are finished
        """
        for player in self.players:
            if not player.fold and player.money > 0 and player.correct_bet != max_bet:
                return False
        return True

    def manage_bets(self, player, max_bet):
        """
        getting the action from player
        """
        actions = ["call", "bet", "fold", "check"]
        check_finish_true = False

        if player.money > 0:
            print("player {} current bet {}".format(player.name, player.correct_bet))
            if player.correct_bet == max_bet:

                actions.remove("call")
            else:
                actions.remove("check")

            check_finish_true = self.client_respond(actions, player, max_bet)
        else:
            print("player %s doesnt have money" % player.name)

        return check_finish_true

    @staticmethod
    def client_respond(actions, player, max_bet):
        flag = True
        while flag:
            print(" player {}: {} {} or {} ?".format(player.name, actions[0], actions[1], actions[2]))
            response = input()
            data = response.split(" ")
            if data[0] in actions:
                if data[0] == "bet":
                    try:
                        if max_bet * 2 <= int(data[1]) + player.correct_bet or player.money < max_bet * 2:
                            player.bet(int(data[1]) - player.correct_bet)
                            print("player {} betted {}".format(player.name, data[1]))
                            print(player.name, player.correct_bet)
                            flag = False
                        else:
                            print("needs to bet x2 from max bet which is %s or more." % max_bet)

                    except:
                        print("not a number try again")
                if data[0] == "call":
                    flag = False
                    player.bet(max_bet - player.correct_bet)
                    print("player {} called {}".format(player.name, player.correct_bet))
                if data[0] == "check":
                    print("player %s check" % player.name)
                    print(player.name, player.correct_bet)
                    return True
                if data[0] == "fold":
                    flag = False
                    print("player fold", player.name)
                    player.folds()

        return False

    def find_max_bet(self):
        max_bet = self.players[0].correct_bet
        for player in self.players:
            if player.correct_bet > max_bet:
                max_bet = player.correct_bet

        return max_bet

    def clear_current_bets(self):
        for player in self.players:
            player.clean_bets()

    def flop3(self):
        self.clear_current_bets()

        # if everyone is out the last hand wins
        flop_num = 3
        card = (0, 'a')
        the_card = (card, (0, 0))
        for j in range(flop_num):
            the_card = self.deck.deal()
            self.flop[the_card[0]] = the_card[1]
            print(the_card[0], the_card[1])

        self.start_round(False)

        # needs to get bets
        self.flop4()

    def flop4(self):
        self.clear_current_bets()

        # if everyone is out the last hand wins
        flopnum = 1
        card = (0, 'a')
        the_card = (card, (0, 0))
        for j in range(flopnum):
            the_card = self.deck.deal()
            self.flop[the_card[0]] = the_card[1]
            print(the_card[0], the_card[1])

        # needs to get bets
        self.start_round(False)
        self.flop5()

    def flop5(self):
        self.clear_current_bets()
        # if everyone is out the last hand wins
        flop_num = 1
        card = (0, 'a')
        the_card = (card, (0, 0))
        for j in range(flop_num):
            the_card = self.deck.deal()
            self.flop[the_card[0]] = the_card[1]
            print(the_card[0], the_card[1])

        self.start_round(False)

        for hand in self.hands:
            cards = list(hand.keys())
            for c in cards:
                self.save_cards[c] = hand[c]
        for hand in self.hands:
            for card in self.flop:
                hand[card] = self.flop[card]
            self.sort_hand(hand)
            # needs to get bets
            self.is_royal(hand)

    def point(self, hand):
        """
        Calculate partial score - needs to be AT THE END
        """
        sortedHand = sorted(hand, reverse=True)
        c_sum = 0
        ranklist = []
        for card in sortedHand:
            ranklist.append(card.rank)
        c_sum = ranklist[0] * 13 ** 4 + ranklist[1] * 13 ** 3 + ranklist[2] * 13 ** 2 + ranklist[3] * 13 + ranklist[4]
        return c_sum

    def is_royal(self, hand):
        """
        Returns total_point and prints out 'Royal Flush' if true, if false, pass down to isStraightFlush(hand)
        """

        # add best hand
        sortedHand = self.sort_hand(hand)
        list_cards = list(sortedHand.keys())
        flag = True
        h = 10
        currank = 14

        index = 0
        for card_suit in list_cards:
            cursuit = card_suit[1]
            total_point = h * 13 ** 5
            royal_flash = [(currank, cursuit), (currank - 1, cursuit), (currank - 2, cursuit), (currank - 3, cursuit),
                           (currank - 4, cursuit)]
            res = True
            for card in royal_flash:
                if card not in list_cards:
                    res = False
                    break
            if not res:
                index += 1
            else:
                break
            if index == 3:
                flag = False
                break
        if flag:
            print('Royal Flush')
            self.tlist.append(total_point)
        else:
            self.isStraightFlush(sortedHand)

    def isStraightFlush(self, hand):
        """
         Returns the total_point and prints out 'Straight Flush' if true, if false, pass down to isFour(hand)
        """
        sortedHand = self.sort_hand(hand)
        list_cards = list(sortedHand.keys())
        flag = True
        h = 9
        index = 0
        for card_suit in list_cards:
            cursuit = card_suit[1]
            currank = card_suit[0]
            if currank != 14:
                straightFlush = [
                    (currank, cursuit), (currank - 1, cursuit), (currank - 2, cursuit),
                    (currank - 3, cursuit), (currank - 4, cursuit)
                ]
                res = True
                for card in straightFlush:
                    if card not in list_cards:
                        res = False
                        break
            else:
                straightFlush = [(currank, cursuit), (2, cursuit), (3, cursuit), (4, cursuit),
                                 (5, cursuit)]
                res = True
                for card in straightFlush:
                    if card not in list_cards:
                        res = False
                        break
            total_point = h * 13 ** 5  # fix
            if res == False:
                index += 1
            else:
                break
            if index == 3:
                flag = False
                break
        if flag:
            print('Straight Flush')
            self.tlist.append(total_point)
        else:
            self.is_four(sortedHand)

    def is_four(self, hand):
        """
        Returns the total_point and prints out 'Four of a Kind' if true, if false, pass down to isFull()
        """

        sortedHand = self.sort_hand(hand)
        list_cards = list(sortedHand.keys())
        flag = False
        h = 8
        index = 0
        total_point = h * 13 ** 5
        for currcard in list_cards:
            currank = currcard[0]
            Four = [(currank, SUITS[0]), (currank, SUITS[1]), (currank, SUITS[2]), (currank, SUITS[3])]
            res = True
            for i in range(len(Four)):
                if Four[i] not in list_cards:
                    res = False
                    break
            if res == False:
                index += 1
            else:
                flag = True
                break
            if index == 4:
                break
        if not flag:
            self.tlist.append(total_point)
            self.is_full(sortedHand)
        else:
            flag = True
            print('Four of a Kind')
            # TODO fix

    def is_full(self,
                hand):  # returns the total_point and prints out 'Full House' if true, if false, pass down to isFlush()
        sortedHand = self.sort_hand(hand)
        # listcards = list(sortedHand.keys())
        flag = True
        h = 7
        isFullHouse = {}
        total_point = h * 13 ** 5  # fix
        for card in sortedHand:
            if card[0] in isFullHouse.keys():
                isFullHouse[card[0]] += 1
            else:
                isFullHouse[card[0]] = 1

        if 3 not in isFullHouse.values():
            flag = False
            self.is_flush(sortedHand)
        else:
            count2 = 0
            count3 = 0
            for card in isFullHouse.keys():
                if isFullHouse[card] == 3:
                    count3 += 1
                if isFullHouse[card] == 2:
                    count2 += 1
            if count3 == 1 and count2 < 1:
                flag = False
            else:
                flag = True
                # we need to get the highest ranks
            if flag:
                print('Full House')
                self.tlist.append(total_point)
            else:
                self.is_flush(sortedHand)

    def is_flush(self, hand):
        """
        Returns the total_point and prints out 'Flush' if true, if false, pass down to isStraight()
        """
        sortedHand = self.sort_hand(hand)
        list_cards = list(sortedHand.keys())
        h = 6
        is_flush = {}
        flag = True
        total_point = h * 13 ** 5  # TODO fix
        for card in list_cards:
            if card[1] in is_flush.keys():
                is_flush[card[1]] += 1
            else:
                is_flush[card[1]] = 1
        if 5 not in is_flush.values() and 6 not in is_flush.values() and 7 not in is_flush.values():
            flag = False

        if flag:
            print('Flush')
            self.tlist.append(total_point)
        else:
            self.is_straight(sortedHand)

    def is_straight(self, hand):
        sortedHand = self.sort_hand(hand)
        list_cards = list(sortedHand.keys())
        list_ranks = []
        for card in list_cards:
            list_ranks.append(card[0])

        flag = True
        h = 5
        total_point = h * 13 ** 5  # TODO fix
        index = 0
        for card in list_ranks:

            if card != 14:
                straight = [card, card - 1, card - 2, card - 3, card - 4]
                res = True
                for elem in straight:
                    if elem not in list_ranks:
                        res = False
                        break
                if not res:
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
                    if elem not in list_ranks:
                        res1 = False
                        break
                for elem in straight2:
                    if elem not in list_ranks:
                        res2 = False
                        break
                if res1 is False and res2 is False:
                    index += 1
                else:
                    flag = True
                    break
            if index == 3:
                flag = False
                break
        if flag:
            print('Straight')
            self.tlist.append(total_point)
        else:
            self.isThree(sortedHand)

    def isThree(self, hand):
        sortedHand = self.sort_hand(hand)
        # listcards = list(sortedHand.keys())
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

        if 3 not in isThree.values():
            flag = False
            self.isTwo(sortedHand)
        else:
            print("Three of a Kind")
            self.tlist.append(total_point)

    def isTwo(self, hand):
        """
        returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
        """
        sortedHand = self.sort_hand(hand)
        list_cards = list(sortedHand.keys())
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
            if isTwoPair[card] == 2:
                count2 += 1
        if count2 < 2:
            flag = False
        else:
            flag = True
        if flag:
            print("Two Pair")
        else:
            self.is_one(sortedHand)

    def is_one(self, hand):
        """
        Returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
        """
        sorted_hand = self.sort_hand(hand)
        list_cards = list(sorted_hand.keys())
        flag = True
        h = 2
        total_point = h * 13 ** 5  # TODO fix
        isPair = {}
        for card in sorted_hand:
            if card[0] in isPair.keys():
                isPair[card[0]] += 1
            else:
                isPair[card[0]] = 1

        count2 = 0
        for card in isPair.keys():
            if isPair[card] == 2:
                count2 += 1
        if count2 == 0:
            flag = False
            self.is_high(sorted_hand)
        else:
            flag = True
            print("One Pair")
            self.tlist.append(total_point)

    def is_high(self, hand):
        """
        returns the total_point and prints out 'High Card'
        """
        sortedHand = self.sort_hand(hand)
        # listcards = list(sortedHand.keys())
        flag = True
        h = 1
        total_point = h * 13 ** 5  # TODO fix
        print("High Card")
        self.tlist.append(total_point)

    def end_game(self):
        savedCard = list(self.save_cards.keys())
        for card in savedCard:
            self.deck.deck[card] = self.save_cards[card]
        for card in self.flop:
            self.deck.deck[card] = self.flop[card]
        self.deck.shuffle()
        self.hands = []
        self.tlist = []  # create a list to store total_point
        self.save_cards = {}
        self.flop = {}


def test_poker_logic():
    Game = Poker(3)
    i = 0
    Game.play()
    Game.end_game()
    print("\n \n")
    Game = Poker(3)


if __name__ == '__main__':
    test_poker_logic()
