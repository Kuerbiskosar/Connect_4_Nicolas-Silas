from time import sleep
from game_remote import Connect4_remote
from os import path # to check if we are wearing a senseHat

class Coordinator_Remote:
    """ 
    Coordinator for two Remote players
        - either playing over CLI or
        - playing over SenseHat

    This class manages the game flow, player registration, turn management, 
    and game status updates for Remote players using the Server.


    Attributes:
        api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        player (Player):    Local Instance of ONE remote Player (Raspi or Normal)
        sense (SenseHat):   Optional Local Instance of a SenseHat (if on Raspi)
    """

    def __init__(self, api_url: str) -> None:
        """
        Initialize the Coordinator_Remote.

        Parameters:
            api_url (str):      Address of Server, including Port Bsp: http://10.147.17.27:5000
        """
        self.api_url = api_url
        self.game = Connect4_remote(api_url)
        # check if a SenseHat is connected. If not, the game will run in the Terminal, where this script was started.
        # https://raspberrypi.stackexchange.com/questions/39153/how-to-detect-what-kind-of-hat-or-gpio-board-is-plugged-in-if-any
        if path.isfile(r"/proc/device-tree/hat/product"): # the r before the string indicates a raw string.
            # a Hat is attached, most likely a senseHat
            # create a sense hat shared between both players
            from sense_hat import SenseHat #type: ignore # this commend makes pylance accept, that sense_hat does not need to be installed on windows
            from player_raspi_local import Player_Raspi_Local

            sense = SenseHat()
            self.player = Player_Raspi_Local(self.game, sense=sense)
            print("initiated sense-hat players")
            #self.player1 = Player_Local(self.game)
            #self.player2 = Player_Local(self.game)
        else:
            from player_local import Player_Local
            self.player = Player_Local(self.game)
        # wait until the other player is connected 
        self.wait_for_second_player()
    


    def wait_for_second_player(self):
        """
        Waits for the second player to connect.

        This method checks the game status until the second player is detected,
        indicating that the game can start.
        """
        turn_number = self.game.get_status()[-1]
        while turn_number < 0:
            turn_number = self.game.get_status()[-1]
            print("waiting for opponent to connect")
            sleep(1) 

    def play(self):
        """ 
        Main function to play the game with two remote players.

        This method manages the game loop, where players take turns making moves,
        checks for a winner, and visualizes the game board.
        """
        status = self.game.get_status()
        winner = status[-2] # the UUID of the winner
        turn_counter = status[-1]
        while not self.game.winner and self.game.turn_counter < self.game.width * self.game.height:
            currentPlayer = self.player1 if self.player1.is_my_turn() else self.player2
            currentPlayer.make_move()
            if winner == self.player.id:
                currentPlayer.celebrate_win()
                exit()
            if winner != None:
                self.player.visualize()
                print("Your opponent wins! sad times.")
        print('The game is a draw.')

# To start a game
if __name__ == "__main__":
    server_location = input("""
 Where is the server?
 [1] - localhost:5000
 [2] - enter url
""")
    if server_location == "1":
        #api_url = "http://localhost:5000"  # Connect 4 API server URL
        api_url = "http://127.0.0.1:5000"
    else:
        api_url = input("url: http://<your input> \n example input: 127.0.1.1:500 \n")
    
    # Uncomment the following lines to specify different URLs
    # pc_url = "http://172.19.176.1:5000"
    # pc_url = "http://10.147.97.97:5000"
    # pc_url = "http://127.0.1.1:5000"

    # Initialize the Coordinator
    c_remote = Coordinator_Remote(api_url=api_url)
    c_remote.play()