class ClientGameState(object):
    """
    Information object for clients
    """

    def __init__(self, player, is_my_turn, game_has_ended, flop, winner=None):
        """

        :type player: TODO
        :type is_my_turn: bool
        :type game_has_ended: bool
        :type flop: TODO
        :type winner: str
        """
        self.is_my_turn = is_my_turn
        self.player = player
        self.game_has_ended = game_has_ended
        self.flop = flop
        self.winner = winner

    def __str__(self):
        # TODO improve this
        return '[flop={flop}, ]'.format(flop=self.flop)
