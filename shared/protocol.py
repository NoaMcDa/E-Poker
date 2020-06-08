import pickle
import socket
import struct


class NetworkConnection(object):
    def __init__(self, ip, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.connect((ip, port))

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
class ProtocolMessage(object):
    def encode(self):
        """
        Get a textual representation (string) of the message (that can be sent via a socket)
        """
        raise NotImplementedError()


class PlayerMoveMessage(ProtocolMessage):
    def __init__(self, bet_amount):
        """
        :param bet_amount: The amount to bet, -1 for folding
        :type  bet_amount: int
        """
        self._bet_amount = bet_amount

    def encode(self):
        return "PLAYER_MOVE {}".format(self._bet_amount)
