import os

os.environ['SDL_VIDEO_CENTERED'] = '1'


def main():
    print('Please choose \'client\' / \'c\' or \'server\' / \'s\': ', end='')
    choice = input().lower()

    if choice == 'client' or choice == 'c':
        import client.client as client
        client.client_main()
    elif choice == 'server' or choice == 's':
        pass
        import server.server as serv
        serv.server_main()

    else:
        print('Bad choice. Bye.')


if __name__ == '__main__':
    main()
