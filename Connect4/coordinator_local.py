

from game import Connect4
from player_local import Player_Local

class Coordinator_Local:
    """ 
    Coordinator for two Local players
    
    This class manages the game flow, player registration, turn management, 
    and game status updates for local players.


    Attributes:
        game (Connect4):    Local Instance of a Connect4 Game
        player1 (Player):   Local Instance of a Player 
        player2 (Player):   Local Instance of a Player
    """

    def __init__(self) -> None:
        """
        Initialize the Coordinator_Local with a Game and 2 Players
        """
        self.game = Connect4()
        self.player1 = Player_Local(self.game)
        self.player2 = Player_Local(self.game)
        #raise NotImplementedError(f"You need to write this code first")
    

    def play(self):
        """ 
        Main function to run the game with two local players.
        
            This method handles player registration, turn management, 
            and checking for a winner until the game concludes.
        """
        # TODO
        #raise NotImplementedError(f"You need to write this code first")



if __name__ == "__main__":
    # Create a coordinator
    # play a game
    Coordinator = Coordinator_Local()
    Coordinator.play()