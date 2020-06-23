from client.game import Game
from client.game_session import GameSession


def client_main():
    """ connects to server, logs in / register, and starts game """
    print('Connecting to server...')
    game_session = GameSession()
    game_session.connect()

    # Login / Register loop
    while True:
        choice = input('login or register? l / r -> ')
        username, password = input('Enter username and password: ').split()

        if choice == 'l' or choice == 'login':
            if game_session.login(username, password):
                break
            print('Failed to login')
        elif choice == 'r' or choice == 'register':
            if game_session.register(username, password):
                break
            print('Failed to register')
        else:
            print('Please enter l,r,login or register')

    # Wait to start game (blocking call)
    game_session.wait_for_game_start()

    while True:
        print("game started")
        game = Game(game_session)
        game.start()


if __name__ == '__main__':
    client_main()
