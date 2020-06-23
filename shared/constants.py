DEFAULT_SERVER_IP = '127.0.0.1'
DEFAULT_SERVER_PORT = 9999
NUM_PLAYERS = 3

# Poker protocol
LOGIN_SUCCESS = 'SUCCESS'  # TODO: replace with the relevant protocol messages
LOGIN_FAIL = 'FAIL'
START_MESSAGE = 'START'

TURN_SUCCESS = "1"
TURN_FAIL = "0"

# Game constants
SCREEN_SIZE = (1000, 700)
FPS = 60

LOG_BORDER_RECT = (0, 0, 0.5 * SCREEN_SIZE[0], 0.70 * SCREEN_SIZE[1])  # x,y, width, height
HAND_BORDER_RECT = (0.5 * SCREEN_SIZE[0], 0, 0.5 * SCREEN_SIZE[0], 0.70 * SCREEN_SIZE[1])  # x,y, width, height
SHARED_HAND_BORDER_RECT = (0, 0.70 * SCREEN_SIZE[1], SCREEN_SIZE[0], 0.30 * SCREEN_SIZE[1])
# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 230)
LIGHT_BLUE = (0, 50, 190)
LOG_BACK_COLOR = BLACK

# File constants
BACKGROUND_IMAGE_PATH = 'resources/background.jpg'
CARD_DECK_IMAGE_PATH = 'resources/carddeck.jpg'

# Client moves
MOVE_CALL = "CALL"
MOVE_CHECK = "CHECK"
MOVE_FOLD = "FOLD"
MOVE_BET = "BET"

# DB Stuff
DB_NAME = 'poker.db'
DB_CREATE_TABLE = \
    """
    CREATE TABLE Clients (
        user_name text,
        password text,
        money int,
        PRIMARY KEY (user_name)
    );
    """
DB_INSERT_USER = \
    """
    INSERT INTO Clients (user_name , password, money)
    VALUES ('{username}','{password}',{money});
    """
DB_CHECK_IF_USER_EXSIST = \
    """
    SELECT * FROM Clients WHERE user_name='{username}';
    """
DB_TRY_LOGIN = \
    """
    SELECT * FROM Clients WHERE user_name='{username}' AND password='{password}';
    """
# ("Noa","123123",3000);
