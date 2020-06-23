import socket

from server import poker_logic, db_manager
from shared import constants, protocol
from shared.protocol import NetworkConnection


def start_server(port=constants.DEFAULT_SERVER_PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', port))
    server_socket.listen(5)
    clients_sockets = []

    for _ in range(constants.NUM_PLAYERS):  # 2 players
        client_sock, _ = server_socket.accept()
        clients_sockets.append(client_sock)

    server_socket.close()
    return clients_sockets


def register_new_user(username, password):
    db_manager.get_connection().cursor().execute(constants.DB_CHECK_IF_USER_EXSIST.format(username=username))
    query_result = db_manager.get_connection().cursor().fetchone()

    if query_result:
        return False

    db_manager.get_connection().cursor().execute(
        constants.DB_INSERT_USER.format(username=username, password=password, money=1000))
    db_manager.get_connection().commit()
    return True


def test_credentials(username, password):
    db_manager.get_connection().cursor().execute(
        constants.DB_TRY_LOGIN.format(username=username, password=password))
    query_result = db_manager.get_connection().cursor().fetchone()
    return query_result


def handle_login(connection):
    while True:
        message = connection.recv_obj()
        if type(message) is not protocol.LoginRegisterMessage:
            raise RuntimeError('login error: ' + str(message))
        if message.is_register:
            user_login_state = register_new_user(message.username, message.password)
            if user_login_state:
                connection.send_string(constants.LOGIN_SUCCESS)
                break
            else:
                connection.send_string(constants.LOGIN_FAIL)
        else:
            if test_credentials(message.username, message.password):
                connection.send_string(constants.LOGIN_SUCCESS)
                break
            else:
                connection.send_string(constants.LOGIN_FAIL)


def start_game(clients_sockets):
    connections = [NetworkConnection(sock) for sock in clients_sockets]

    for conn in connections:
        handle_login(conn)

    for conn in connections:
        conn.send_string(constants.START_MESSAGE)
    game = poker_logic.Poker(connections)
    game.play()
    game.end_game()
    while True:
        poker_logic.test_poker_logic(connections)


def close_server(clients_sockets):
    for sock in clients_sockets:
        # TODO: maybe send "GoodbyeMessage", probably no need
        sock.close()


def server_main():
    # db_manager.clear_db()
    clients_sockets = start_server()
    start_game(clients_sockets)
    close_server(clients_sockets)

    db_manager.get_connection().commit()
    db_manager.get_connection().close()


if __name__ == '__main__':
    server_main()
