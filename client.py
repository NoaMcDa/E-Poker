import socket

import constants
import poker_protocol


def login_server(sock, username, password):
    """
    Connects to server with username and password

    :return: True if connection was successful
    """
    # Send username and password
    poker_protocol.send_string(sock, username)
    poker_protocol.send_string(sock, password)

    # Receive login result
    connect_result = poker_protocol.recv_string(sock)
    if connect_result == constants.LOGIN_SUCCESS:
        return True
    if connect_result == constants.LOGIN_FAIL:
        return False
    raise Exception('Unexpected: ' + connect_result)


MENU = '1 - check\n2 - bet\n3 - fold\n4 - call'


def play_turn(sock, game_state):
    print('Current game state: TODO print the object')

    choice = -1
    while not 1 <= choice <= 4:
        print('Please choose from the following\n' + MENU)
        choice = int(input())

    if choice == 1:
        pass
    elif choice == 2:
        pass
    elif choice == 3:
        pass
    elif choice == 4:
        pass


def client_main():
    # For now lets assume I am registered.
    # TODO: add register feature

    # Connect to server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((constants.DEFAULT_SERVER_IP, constants.DEFAULT_SERVER_PORT))

    print('Enter username and password')
    username, password = input().split()

    username, password = username.trim(), password.trim()  # remove whitespace
    if not login_server(sock, username, password):
        print('Failed to login, please register TODO')
        exit(1)

    # We are now logged in.

    # Wait to start game (blocking call)
    start_message = poker_protocol.recv_string(socket)
    if constants.START_MESSAGE != start_message:
        print('Unexpected string: ' + start_message)
        exit(1)

    # Choice loop
    while True:
        game_state = poker_protocol.recv_obj(sock)  # Receive GameState object

        # TODO: if game_state.is_my_turn(), then play turn
        play_turn(sock, game_state)


if __name__ == '__main__':
    client_main()


#################################################################
def bet(client, Money):
    in_data = client.recv(1024)
    print(in_data.decode())
    out_data = input()
    loop = True
    while loop:
        if "bet" in out_data:
            client.sendall(bytes(out_data, 'UTF-8'))
            in_data = client.recv(1024)

            print(in_data.decode())
            out_data = input()
            flag = True
            while flag:
                try:
                    Money = Money - int(out_data)
                    client.sendall(bytes(out_data, 'UTF-8'))
                    flag = False
                except:
                    print("Try entering a number")
                    out_data = input()

            loop = False
        elif ("call" in out_data or "fold" in out_data or "check" in out_data):
            client.sendall(bytes(out_data, 'UTF-8'))
            in_data = client.recv(1024)
            print(in_data.decode())
            loop = False
        else:
            print("try entering a check bet call or fold")
            out_data = input()

# SERVER = "127.0.0.1"
# PORT = 8080
# Money = 1000
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect((SERVER, PORT))
# in_data = client.recv(1024)
# print(in_data.decode())
# out_data = input()
# client.sendall(bytes(out_data, 'UTF-8'))
# in_data = client.recv(1024)
# print(in_data.decode())
# out_data = input()
# client.sendall(bytes(out_data, 'UTF-8'))
## if out_data=='bye':
## break
# bet(client, Money)
# client.close()
#
