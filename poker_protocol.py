import pickle
import struct


def send_bytes(sock, byte_arr):
    """
    In poker protocol, for every byte object we send, the size is sent first
    """

    sock.send(struct.pack('>I', len(byte_arr)))
    sock.send(byte_arr)


def recv_bytes(sock):
    """
    Receive bytes
    """
    size = struct.unpack('>I', sock.recv(4))[0]
    return sock.recv(size)


def send_string(sock, string):
    """
    Send string
    """
    send_bytes(sock, string.encode())


def recv_string(sock):
    """
    Receive string
    """
    return recv_bytes(sock).decode()


def send_obj(sock, obj):
    """
    Send an object
    """
    send_bytes(sock, pickle.dumps(obj))


def recv_obj(sock):
    """
    Recv an object
    """
    return pickle.loads(recv_bytes(sock))
