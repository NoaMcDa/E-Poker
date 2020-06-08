from shared import constants, protocol


class GameSession(object):
    def __init__(self):
        self.connection = None
        self._bet = 0  # TODO noa check this
        self._min_bet = 0  # TODO noa

    def connect(self, ip=constants.DEFAULT_SERVER_IP, port=constants.DEFAULT_SERVER_PORT):
        self.connection = protocol.NetworkConnection(ip, port)

    def login(self, username, password):
        """
        login with username and password
        :type username: str
        :type password: str
        :return: True if connection was successful
        """

        # Send username and password
        self.connection.send_string(username)
        self.connection.send_string(password)

        # Receive login result
        connect_result = self.connection.recv_string()
        if connect_result == constants.LOGIN_SUCCESS:
            return True
        if connect_result == constants.LOGIN_FAIL:
            return False
        raise Exception('Unexpected: ' + connect_result)

    def wait_for_game_start(self):
        """
        Waits for server to send game start message
        """
        start_message = self.connection.recv_string()
        if constants.START_MESSAGE != start_message:
            print('Unexpected string: ' + start_message)
            exit(1)

    def send_move(self, move):
        pass

    def get_opponent_move(self):
        pass

    def raise_bet(self, amount):
        self._bet += amount

    def lower_bet(self, amount):
        if self._bet - amount < self._min_bet:
            raise ValueError("Insufficient bet")
        self._bet -= amount

    def fold_hand(self):
        pass

    def play(self):
        while True:
            game_state = self.connection.recv_obj()
            if game_state.game_has_ended:
                print('game has ended')
                print('winner is: ' + game_state.winner)
                return
            if game_state.is_my_turn:
                self.play_turn(game_state)

    MENU = '1 - check/call\n2 - bet\n3 - fold'

    def play_turn(self, game_state):
        print('game state: ' + str(game_state))

        choice = -1
        while not 1 <= choice <= 3:
            print('Please choose from the following\n' + GameSession.MENU)
            choice = int(input())

        # TODO talk with noa
        if choice == 1:
            pass
        elif choice == 2:
            print('enter bet amount')
            bet_amount = int(input())
            self.connection.send_string(protocol.PlayerMoveMessage(bet_amount).encode())

        elif choice == 3:
            pass


def client_main():
    # game = Game()
    # game.start()
    # For now lets assume I am registered.
    # TODO: add register feature

    # Connect to server
    print('Connecting to server...')
    game_session = GameSession()
    game_session.connect()

    print('Enter username and password')
    username, password = input().split()

    if not game_session.login(username, password):
        print('Failed to login, please register TODO')
        exit(1)

    # Wait to start game (blocking call)
    game_session.wait_for_game_start()

    game_session.play()


if __name__ == '__main__':
    client_main()
