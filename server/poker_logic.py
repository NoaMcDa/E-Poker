import random
from typing import List

from shared import constants
from shared import protocol
from shared.protocol import NetworkConnection

RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

SUITS = ('S', 'D', 'H', 'C')


# TODO: MIGHT HAVE SOME TYPE IFS THAT ARE BAD -FIX THAT

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
    def __init__(self, network_connection):
        """
        :type network_connection: NetworkConnection
        """
        self._network_connection = network_connection

        self.hand = None
        self.money = None
        self.name = None
        self.correct_bet = None
        self.fold = None

    def send_name(self):
        self._network_connection.send_obj(protocol.SendNameMessage(self.name))

    def send_its_your_turn(self):
        self._network_connection.send_obj(protocol.ItsYourTurnMessage())

    def send_hand(self):
        self._network_connection.send_obj(protocol.HandPerUser(self.hand))

    def send_move_of_another_player(self, player_move):
        self._network_connection.send_obj(player_move)

    def recv_money(self):
        money = self._network_connection.recv_obj()
        return money

    def send_winner(self, player_list):
        player_names = [player.name for player in player_list]
        self._network_connection.send_obj(protocol.PlayerWinnerMessage(player_names))

    def recv_move(self):
        """
        :return:
        """
        move = self._network_connection.recv_obj()
        # TODO: MAYBE ASSERT
        return move

    def send_blind_sum(self, blind_sum):
        """
        takes a certain amount of starting money at the beginning
        :param blind_sum: int
        :return:
        """
        self._network_connection.send_obj(protocol.SendBlindMessage(blind_sum))

    def send_flop_cards(self, array_flop):
        self._network_connection.send_obj(protocol.SendCardFlop(array_flop))

    def send_turn_state(self, turn_state):  # success or failure
        turn_state_object = protocol.TurnStateMessage(turn_state)
        self._network_connection.send_obj(turn_state_object)

    def send_sum_money(self, sum_money):
        self.money += sum_money
        self._network_connection.send_obj(protocol.SendTotalSumOnTable(sum_money))

    def start_game(self, hand, money, name, correct_bet, fold):
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


class Deck(object):  # creating deck of 54 cards
    Cards = []

    def __init__(self):
        self.deck = {}
        self.xDeck = 0
        self.yDeck = 0
        for suit in SUITS:  # creating sorted deck
            for rank in RANKS:
                card = (rank, suit)
                self.deck[card] = (self.xDeck, self.yDeck)
                self.xDeck += 100
            self.xDeck = 0
            self.yDeck += 130

    def shuffle(self):
        Cards = list(self.deck.keys())
        random.shuffle(Cards)  # shuffling the cards
        NewDeck = {}
        i = 0
        for _ in self.deck:
            NewDeck[Cards[i]] = self.deck[Cards[i]]
            i += 1
        self.deck = NewDeck

    def __len__(self):
        return len(self.deck)

    def deal(self):
        Cards = list(self.deck.keys())
        if len(self) == 0:
            return None
        else:
            return Cards[0], self.deck.pop(Cards.pop(0))  # returns a tuple!!!


class Poker(object):  # the whole game mechanics
    def __init__(self, client_connections: List[NetworkConnection]):
        """
        :type client_connections: int
        :param client_connections: NetworkConnection
        """

        num_hands = len(client_connections)
        self.client_connections = client_connections
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.players = []
        self.tlist = []  # create a list to store total_point
        self.save_cards = {}
        self.flop = {}
        self.sum_money = 0
        numCards_in_Hand = 2

        for i in range(num_hands):  # serving cards to each player
            hand = {}
            card = (0, 'a')
            the_card = (card, (0, 0))
            for j in range(numCards_in_Hand):
                the_card = self.deck.deal()
                hand[the_card[0]] = the_card[1]

            # RECIVING MONEY FROM CLIENT AND SENDING NAME AND HAND
            player = Player(self.client_connections[i])
            player.start_game(hand, 1000, str(i), 0, False)
            player.send_name()
            player.send_hand()
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
            for i in range(len(self.players)):
                if i % len(self.players) == 0:
                    self.players[i].bet(small_blind)
                    self.players[i].send_blind_sum(small_blind)
                elif i % len(self.players) == 1:
                    self.players[i].bet(big_blind)
                    self.players[i].send_blind_sum(big_blind)
                else:
                    self.players[i].send_blind_sum(0)

            self.sum_money += small_blind + big_blind
            print(self.sum_money)
        except:  # TODO: catch the correct exception.
            print("not enough players")

    def start_round(self, game_beginning):
        if game_beginning:
            self.manage_blinds()
            game_turn = 2
        else:
            game_turn = 0
        num_players = len(self.players)
        while True:
            max_bet = self.find_max_bet()
            if not self.players[game_turn % num_players].fold:
                self.players[game_turn % num_players].send_its_your_turn()  # SEND TO THE PLAYER ITS TURN
                stop, client_move = self.manage_bets(self.players[game_turn % num_players], max_bet)  # GETS THE ACTION
            else:
                stop = False

            for player in self.players:
                if (player is not self.players[game_turn % num_players]):  # SENDS EVERYONE THE OPPONENT MOVE
                    player.send_move_of_another_player(client_move)

            game_turn += 1
            max_bet = self.find_max_bet()
            players_not_folded = []
            for player in self.players:
                if not player.fold:
                    players_not_folded.append(player)
            if len(players_not_folded) == 1:
                for player in self.players:
                    player.send_winner(players_not_folded)  # SENDING THE NAME OF THE WINNER
            elif game_turn >= num_players:
                if stop:
                    if self.check_finish(max_bet):
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
        actions = [constants.MOVE_CALL, constants.MOVE_BET, constants.MOVE_FOLD, constants.MOVE_CHECK]
        check_finish_true = False

        if player.money > 0 and not player.fold:
            print("player {} current bet {}".format(player.name, player.correct_bet))
            if player.correct_bet == max_bet:

                actions.remove(constants.MOVE_CALL)
            else:
                actions.remove(constants.MOVE_CHECK)

            check_finish_true, client_move = self.client_respond(actions, player, max_bet)
        elif player.fold:
            print("player folded")
        else:
            print(
                "player %s doesnt have money " % player.name)  # TODO : DONT EVEN GET TO THIS SITUATION - ALLOW CLIENTS WITH MONEY TO ENTER

        return check_finish_true, client_move

    def client_respond(self, actions, player, max_bet):
        """
        :param actions:
        :param player:
        :param max_bet:
        :return:
        """
        flag = True
        while flag:
            print(" player {}: {} {} or {} ?".format(player.name, actions[0], actions[1], actions[2]))
            response = player.recv_move()

            if type(response) is protocol.PlayerMoveBetMessage:
                try:
                    if max_bet * 2 <= int(response.bet_amount) + player.correct_bet or player.money < max_bet * 2:
                        player.bet(int(response.bet_amount) - player.correct_bet)
                        self.sum_money += int(response.bet_amount)
                        print(self.sum_money)
                        print("player {} betted {}".format(player.name, response.bet_amount))
                        player.send_turn_state(constants.TURN_SUCCESS)
                        flag = False
                    else:
                        print("needs to bet x2 from max bet which is %s or more." % max_bet)
                        player.send_turn_state(constants.TURN_FAIL + " BET_FAIL")

                except:
                    print("not a number try again")
                    player.send_turn_state(constants.TURN_FAIL + " BET_FAIL")

            if type(response) is protocol.PlayerMoveCallMessage:
                if constants.MOVE_CALL in actions:

                    flag = False
                    player.bet(max_bet - player.correct_bet)
                    self.sum_money += max_bet
                    print(self.sum_money)
                    player.send_turn_state(constants.TURN_SUCCESS)
                    print("player {} called {}".format(player.name, player.correct_bet))
                else:
                    player.send_turn_state(constants.TURN_FAIL)
            if type(response) is protocol.PlayerMoveCheckMessage:
                if constants.MOVE_CHECK in actions:

                    print("player %s check" % player.name)
                    print(player.name, player.correct_bet)
                    player.send_turn_state(constants.TURN_SUCCESS)
                    return True, response
                else:
                    player.send_turn_state(constants.TURN_FAIL)
            if type(response) is protocol.PlayerMoveFoldMessage:
                flag = False
                print("player fold", player.name)
                player.folds()
                # player.send_turn_state(constants.TURN_SUCCESS)

        return False, response

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
        array_flop_to_clients = []
        for j in range(flop_num):
            the_card = self.deck.deal()
            self.flop[the_card[0]] = the_card[1]
            array_flop_to_clients.append((the_card[0], the_card[1]))
            print(the_card[0], the_card[1])

        for player in self.players:
            player.send_flop_cards(array_flop_to_clients)

        self.start_round(False)

        # needs to get bets
        self.flop4()

    def flop4(self):
        self.clear_current_bets()

        # if everyone is out the last hand wins
        flop_num = 1
        array_flop_to_clients = []

        for j in range(flop_num):
            the_card = self.deck.deal()
            self.flop[the_card[0]] = the_card[1]
            array_flop_to_clients.append((the_card[0], the_card[1]))
            print(the_card[0], the_card[1])

        for player in self.players:
            player.send_flop_cards(array_flop_to_clients)
        # needs to get bets
        self.start_round(False)
        self.flop5()

    def flop5(self):
        self.clear_current_bets()
        # if everyone is out the last hand wins
        flop_num = 1
        array_flop_to_clients = []

        for j in range(flop_num):
            the_card = self.deck.deal()
            self.flop[the_card[0]] = the_card[1]
            array_flop_to_clients.append((the_card[0], the_card[1]))
            print(the_card[0], the_card[1])

        for player in self.players:  # sending the clients the flop cards
            player.send_flop_cards(array_flop_to_clients)

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
        ranklist = [card[0] for card in sortedHand]

        c_sum = ranklist[0] * 13 ** 4 + ranklist[1] * 13 ** 3 + ranklist[2] * 13 ** 2 + ranklist[3] * 13 + ranklist[4]
        return c_sum

    def point_order(self, hand):

        c_sum = (hand[0])[0] * 13 ** 4 + (hand[1])[0] * 13 ** 3 + (hand[2])[0] * 13 ** 2 + (hand[3])[0] * 13 + \
                (hand[4])[0]
        return c_sum

    def point_straight(self, hand):

        c_sum = (hand[0]) * 13 ** 4 + (hand[1]) * 13 ** 3 + (hand[2]) * 13 ** 2 + (hand[3]) * 13 + (hand[4])
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

            total_point = h * 13 ** 5
            if res == False:
                index += 1
            else:
                total_point = total_point + self.point(straightFlush)
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
            self.is_full(sortedHand)
        else:
            biggest_rank_in_hand = 0
            biggest_rank_in_hand_suit = 'X'
            for card in hand:
                if card not in Four:
                    if (card[0] > biggest_rank_in_hand):
                        biggest_rank_in_hand = card[0]
                        biggest_rank_in_hand_suit = card[1]
            Four.append((biggest_rank_in_hand, biggest_rank_in_hand_suit))
            total_point = h * 13 ** 5 + self.point(Four)
            self.tlist.append(total_point)

            flag = True
            print('Four of a Kind')

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
            saved_suits = []
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
                biggest_rank_three = 0
                biggest_rank_three_suits = []
                biggest_rank_two = 0
                biggest_rank_two_suits = []
                for card in sortedHand:
                    if (isFullHouse[card[0]] == 3):
                        if (biggest_rank_three < card[0]):
                            biggest_rank_three = card[0]
                            biggest_rank_three_suits = []
                            biggest_rank_three_suits.append(card[1])
                        elif (biggest_rank_three == card[0]):
                            biggest_rank_three_suits.append(card[1])
                for card in sortedHand:
                    if (isFullHouse[card[0]] == 3 and biggest_rank_three != card[0] or isFullHouse[card[0]] == 2):
                        if (biggest_rank_two < card[0]):
                            biggest_rank_two = card[0]
                            biggest_rank_two_suits = []
                            biggest_rank_two_suits.append(card[1])
                        elif (biggest_rank_two == card[0]):
                            biggest_rank_two_suits.append(card[1])
                FullHouse = [(biggest_rank_three, biggest_rank_three_suits[0]),
                             (biggest_rank_three, biggest_rank_three_suits[1]),
                             (biggest_rank_three, biggest_rank_three_suits[2]),
                             (biggest_rank_two, biggest_rank_two_suits[0]),
                             (biggest_rank_two, biggest_rank_two_suits[1])]
                print('Full House')
                total_point = h * 13 ** 5 + self.point_order(FullHouse)
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
        is_flush_ranks = {}
        is_flush_ranks["S"] = []
        is_flush_ranks["D"] = []
        is_flush_ranks["H"] = []
        is_flush_ranks["C"] = []
        flag = True
        total_point = h * 13 ** 5
        for card in list_cards:
            if card[1] in is_flush.keys():
                is_flush[card[1]] += 1
                is_flush_ranks[card[1]].append(card)
            else:
                is_flush[card[1]] = 1
                is_flush_ranks[card[1]].append(card)

        if 5 not in is_flush.values() and 6 not in is_flush.values() and 7 not in is_flush.values():
            flag = False
        else:
            for card in list_cards:
                if is_flush[card[1]] > 4:
                    total_point += self.point(is_flush_ranks[card[1]])
                    break

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
        straight_hand = []
        flag = True
        h = 5
        total_point = h * 13 ** 5
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
                    straight_hand = straight
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
                    if res1 is True:
                        straight_hand = straight1
                    else:
                        straight_hand = straight2
                    break
            if index == 3:
                flag = False
                break
        if flag:
            print('Straight')
            total_point += self.point_straight(straight_hand)
            self.tlist.append(total_point)

        else:
            self.isThree(sortedHand)

    def isThree(self, hand):
        sortedHand = self.sort_hand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 4
        isThree = {}

        for i in range(14):
            isThree[i + 1] = []

        total_point = h * 13 ** 5  # fix
        for card in sortedHand:
            isThree[card[0]].append(card)

        if 3 != len(isThree.values()):
            flag = False
            self.isTwo(sortedHand)
        else:
            three_of_a_kind = []
            for key in isThree:
                if len(isThree[key]) == 3:
                    three_of_a_kind.extend(isThree[key])
                    break

            temp = 0
            for card in listcards:
                if card not in three_of_a_kind:
                    three_of_a_kind.append(card)
                    temp += 1
                    if temp == 2:
                        break
            print(three_of_a_kind)
            total_point += self.point_order(three_of_a_kind)
            print("Three of a Kind")
            self.tlist.append(total_point)

    def isTwo(self, hand):
        """
        returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
        """
        sortedHand = self.sort_hand(hand)
        list_cards = list(sortedHand.keys())
        list_keys = []
        list_two_pair = []
        flag = True
        h = 3
        total_point = h * 13 ** 5
        isTwoPair = {}
        for i in range(14):
            isTwoPair[i + 1] = []

        for card in sortedHand:
            isTwoPair[card[0]].append(card)

        count2 = 0
        for card in isTwoPair.keys():
            if len(isTwoPair[card]) == 2:
                list_keys.append(card)
                count2 += 1
        if count2 < 2:
            flag = False
        if flag:

            print("Two Pair")
            list_keys.sort(reverse=True)
            for i in range(2):
                list_two_pair.extend(isTwoPair[list_keys[i]])

            temp = 0
            for card in list_cards:
                if card[0] not in list_keys:
                    list_two_pair.append(card)
                    temp += 1
                    if temp == 1:
                        break
            total_point += self.point_order(list_two_pair)
            self.tlist.append(total_point)

        else:
            self.is_one(sortedHand)

    def is_one(self, hand):
        """
        Returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
        """
        sorted_hand = self.sort_hand(hand)
        list_cards = list(sorted_hand.keys())
        list_pairs = []
        flag = True
        h = 2
        total_point = h * 13 ** 5
        isPair = {}
        for i in range(14):
            isPair[i + 1] = []
        for card in sorted_hand:
            isPair[card[0]].append(card)

        count2 = 0
        for card in isPair.keys():
            if len(isPair[card]) == 2:
                list_pairs.extend(isPair[card])
                count2 += 1
                break
        if count2 == 0:
            flag = False
            self.is_high(sorted_hand)
        else:
            flag = True
            print("One Pair")
            temp = 0
            for card in list_cards:
                if card[0] not in list_pairs:
                    list_pairs.append(card)
                    temp += 1
                    if temp == 3:
                        break

            total_point += self.point_order(list_pairs)
            self.tlist.append(total_point)

    def is_high(self, hand):
        """
        returns the total_point and prints out 'High Card'
        """
        sortedHand = self.sort_hand(hand)
        listcards = list(sortedHand.keys())
        flag = True
        h = 1
        total_point = (listcards[0])[0] * 13 ** 4 + (listcards[1])[0] * 13 ** 3 + (listcards[2])[0] * 13 ** 2 + \
                      (listcards[3])[0] * 13 + (listcards[4])[0]
        print("High Card")
        self.tlist.append(total_point)

    def winner_of_game(self):
        dict_players = {}

        print(self.tlist)
        index = 0
        for player in self.players:
            print(player.hand)
            dict_players[self.tlist[index]] = []
            index += 1
        index = 0
        for player in self.players:
            dict_players[self.tlist[index]].append(player)
            index += 1

        self.tlist.sort(reverse=True)

        winner = dict_players[self.tlist[0]]
        return winner

    def end_game(self):
        winner = self.winner_of_game()
        for player in self.players:
            player.send_winner(winner)
        if len(winner) == 1:
            print("the winner is ", winner[0].name)
            print(self.sum_money)
            winner[0].send_sum_money(self.sum_money)
        else:
            print("the winners are: ")
            for player in winner:
                print("player : ", player.name)
                player.send_sum_money(self.sum_money // len(winner))

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
        self.sum_money = 0



def test_poker_logic(connections):
    game = Poker(connections)
    game.play()
    game.end_game()


if __name__ == '__main__':
    test_poker_logic()
