import pickle
import select
import socket
import struct


class NetworkConnection(object):
    """ Responsible for all network interactions """

    def __init__(self, sock: socket.socket = None, ip=None, port=None):
        if sock is None:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._sock.connect((ip, port))
        else:
            self._sock = sock

    def is_data_available(self):
        """
        Use select to poll the socket
        :return: bool if data is available to receive
        """
        readable, _, _ = select.select([self._sock], [], [], 0)
        return len(readable) != 0

    def send_bytes(self, byte_arr):
        """
        In poker protocol, for every byte object we send, the size is sent first
        """

        self._sock.send(struct.pack('>I', len(byte_arr)))
        self._sock.send(byte_arr)

    def recv_bytes(self):
        """
        Receive bytes
        """
        size = struct.unpack('>I', self._sock.recv(4))[0]
        return self._sock.recv(size)

    def send_string(self, string):
        """
        Send string
        """
        self.send_bytes(string.encode())

    def recv_string(self):
        """
        Receive string
        """
        return self.recv_bytes().decode()

    def send_obj(self, obj):
        """
        Send an object
        """
        self.send_bytes(pickle.dumps(obj))

    def recv_obj(self):
        """
        Recv an object
        """
        return pickle.loads(self.recv_bytes())


# Protocol messages

class AbstractMessage(object):
    pass


class LoginRegisterMessage(AbstractMessage):
    def __init__(self, username: str, password: str, is_register: bool = False):
        """
        if is_register:
            those details will be used to register a new user
        """
        self.username = username
        self.password = password
        self.is_register = is_register


class MoveMessage(AbstractMessage):
    pass


class PlayerMoveBetMessage(MoveMessage):
    def __init__(self, name, bet_amount):
        self.bet_amount = bet_amount
        self.name = name


class SendNameMessage(AbstractMessage):
    def __init__(self, name):
        self.name = name


class ItsYourTurnMessage(AbstractMessage):
    pass


class PlayerMoveCallMessage(MoveMessage):
    def __init__(self, name, call_amount):
        self.name = name
        self.call_amount = call_amount


class PlayerMoveCheckMessage(MoveMessage):
    def __init__(self, name):
        self.name = name


class PlayerMoveFoldMessage(MoveMessage):
    def __init__(self, name):
        self.name = name


class PlayerWinnerMessage(AbstractMessage):
    def __init__(self, players_list):
        self.players_list = players_list


class TurnStateMessage(AbstractMessage):
    def __init__(self, turn_state):
        self.turn_state = turn_state


class HandPerUser(AbstractMessage):
    def __init__(self, player_hand):
        self.player_hand = player_hand


class MoneyPerUser(AbstractMessage):
    def __init__(self, player_money):
        self.player_money = player_money


class SendCardFlop(AbstractMessage):
    def __init__(self, cards_to_display):
        self.cards_to_display = cards_to_display


class SendTotalSumOnTable(AbstractMessage):
    def __init__(self, sum):
        self.sum = sum


class SendBlindMessage(AbstractMessage):
    def __init__(self, sum):
        self.sum = sum
