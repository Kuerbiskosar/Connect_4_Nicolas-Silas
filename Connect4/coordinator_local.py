

from game import Connect4
from os import path # to check if we are wearing a senseHat

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
        self.game = Connect4(8,7)
        # check if a SenseHat is connected. If not, the game will run in the Terminal, where this script was started.
        # https://raspberrypi.stackexchange.com/questions/39153/how-to-detect-what-kind-of-hat-or-gpio-board-is-plugged-in-if-any
        if path.isfile(r"/proc/device-tree/hat/product"): # the r before the string indicates a raw string.
            # a Hat is attached, most likely a senseHat
            # create a sense hat shared between both players
            from sense_hat import SenseHat #type: ignore # this commend makes pylance accept, that sense_hat does not need to be installed on windows
            from player_raspi_local import Player_Raspi_Local

            sense = SenseHat()
            self.player1 = Player_Raspi_Local(self.game, sense=sense)
            self.player2 = Player_Raspi_Local(self.game, sense=sense)
            print("initiated sense-hat players")
            #self.player1 = Player_Local(self.game)
            #self.player2 = Player_Local(self.game)
        else:
            from player_local import Player_Local
            self.player1 = Player_Local(self.game)
            self.player2 = Player_Local(self.game)
        #raise NotImplementedError(f"You need to write this code first")
    

    def play(self):
        """ 
        Main function to run the game with two local players.
        
            This method handles player registration, turn management, 
            and checking for a winner until the game concludes.
        """
        while not self.game.winner and self.game.turn_counter < self.game.width * self.game.height:
            currentPlayer = self.player1 if self.player1.is_my_turn() else self.player2
            currentPlayer.make_move()
            if self.game.winner:
                currentPlayer.celebrate_win()
                break
        print('The game is a draw.')



if __name__ == "__main__":
    # Create a coordinator
    # play a game
    Coordinator = Coordinator_Local()
    Coordinator.play()