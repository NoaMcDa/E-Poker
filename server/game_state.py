
class GameState(object):
    """
    sending the client the gamestate, positions of all players and his turn, so we can present it in the graphics
    """
    def __init__(self,player,turn,end_game,flop):
        self.turn = turn
        self.player = player
        self.end_game = end_game
        self.flop = flop