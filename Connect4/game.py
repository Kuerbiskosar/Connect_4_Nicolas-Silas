import uuid
import random

import numpy as np


class Connect4:
    """
    Connect 4 Game Class

        Defines rules of the Game
            - what is a win
            - where can you set / not set a coin
            - how big is the playing field

        Also keeps track of the current game  
            - what is its state
            - who is the active player?

        Is used by the Coordinator
            -> executes the methods of a Game object
    """
    
    def __init__(self, width:int = 8, height:int = 7) -> None:
        """ 
        Init a Connect 4 Game

        Parameters
        - width (int) default 8       The width of the connect 4 board
        - height (int) defalut 7      The height of the connect 4 board

        Attributes:
        - Board (np array)          height x width numpy array of strings
        - player_info (Dict)        dictionary with uuid's as strings and tuple with player icon and player name as values
        - players (list)            list containing the registered players uuid's
        - activeplayer (int)        the index of the active player in players
        - turn_counter (int)        which turn it is (-1 = game has not yet started)
        - winner (uuid/None)        None, when no winner is present. The winners uuid, when the game ended with a winner
        """
        self.board = np.empty((width, height), dtype=str)    # Board 8x7 with zeros representing empty cells
        self.player_info = {}                       # Dictionary to map player UUID to a tuple with icon and name
        self.players = []                           # a list with the players UUID's
        self.activeplayer = 0                       # index of the active player in the list 
        self.turn_counter = -1                       # To keep track of whose turn it is
        self.winner = None                          # Holds the winner's ID when a win is detected
        self.width = width
        self.height = height


    """
    Methods to be exposed to the API later on
    """
    def get_status(self) -> tuple:
        """
        Get the game's status.
        Returns
        - Dictionary with the following Keys
            - active_player (str)   'X' or 'O' The symbol of the active player in the board
            - active_id (uuid)      the UUID of the active player
            - winner (str)          the uuid of the player that won the game
            - turn_number (int)     the turn Number. -1 if the Game has not jet started
        """
        # TODO: change to follow api specification (currently: icon, winner, turn_counter. should be: icon, uuid, winner, turn_counter)
        # TODO: probably prettier as a dictionary (get values by key)
        return {"active_player":self.player_info[self.players[self.activeplayer]][0],
                "active_id":self.players[self.activeplayer],
                "winner":self.winner,
                "turn_number":self.turn_counter}


    def register_player(self, player_id: uuid.UUID, name: str) -> str:
        """ 
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            -  player_id (UUID)    Unique ID
            -  name (str)          the Name of the player

        Returns:
            icon (str)       Player Icon for the registering player (or None if failed)
        """
        if len(self.player_info) < 2:
            icon = ''
            if len(self.player_info) < 1:
                choice = np.random.rand()
                if choice > 0.5:
                    icon = 'X'
                else: icon = 'O'
            elif self.player_info[self.players[0]][0] == 'X':
                icon = 'O'
            else: icon = 'X'

            self.player_info[player_id] = (icon, name)
            self.players.append(player_id)
            if len(self.player_info) == 2:
                print("two players make a party")
                self.turn_counter = 0
            return icon
        return None


    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state (For Example an Array of all Elements)

        Returns:
            board (numpy array of lists of strings)     The game board. board [1,0] is the second collumn on the bottom
        """
        return self.board


    def check_move(self, column:int, id:str = None, icon:str = None) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move
            if so, makes the move and returns true
            id OR icon are required

        Parameters:
            colmn (int):      Selected Column of Coin Drop
            id (uuid):        Player ID of the move requesting player
            icon (string):    icon of the move requesting player
        Returns:
            bool    True if the move was valid, false otherwise
        """
        if icon == None and id != None:
            icon = self.player_info.get(id)[0]
        # if it is not the turn of the requesting player, mark the move as invalid
        if self.player_info[self.players[self.activeplayer]][0] != icon:
            return False
        for i in range(len(self.board[column])):
            if self.board[column][i] == '':
                self.board[column][i] = icon
                self.__update_status()
                return True
        else:
            return False
        
    """ 
    Internal Method (for Game Logic)
    """
    def __update_status(self):
        """ 
        Update all values for the status (after each successful move)
            - active player
            - winner
            - turn_number
        """
        self.__detect_win()
        self.activeplayer = self.activeplayer*-1 + 1
        self.turn_counter += 1
    

    def __detect_win(self)->bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        
        Returns:
            bool    True if there's a winner, False otherwise
        """    
        # Active player icon for easier comparison
        icon:str = self.player_info[self.players[self.activeplayer]][0]
        # the code checks Horizontal wins, Vertical wins, Diagonal up and Diagonal down wins in this order
        # The code for those checks is almost same, except for the checking pattern and boundary conditions
        # for the diagonal down check a special case is needed, because it is the only case that does not start its check at an offset of 0,0
        patterns = [(1,0), (0,1), (1,1)]
        #boundarys = [(1,0), (0,1), (1,1), (1, -1)] # the for loop index i gets multiplied with these, to change the positions
        # check horizontal, vertical and diagonal
        for pattern in patterns:
            for y in range(self.height - 3 * pattern[1]):
                for x in range(self.width - 3 * pattern[0]):  # Only go as far as possible for 4 in a row
                    if all(self.board[x + i * pattern[0], y + i * pattern[1]] == icon for i in range(4)):
                        self.winner = self.players[self.activeplayer]
                        # set the fields to winner fields
                        for i in range (4):
                            self.board[x+i*pattern[0], y+i*pattern[1]] = icon.lower()
                        return True
        # check diagonal down
        for pattern in patterns:
            for y in range(3, self.height):
                for x in range(self.width - 3):  # Only go as far as possible for 4 in a row
                    if all(self.board[x + i, y - i] == icon for i in range(4)):
                        self.winner = self.players[self.activeplayer]
                        # set the fields to winner fields
                        for i in range (4):
                            self.board[x+i, y-i] = icon.lower()
                        return True
        # No winner detected
        self.winner = None
        return False

if __name__ == "__main__":
    myGame = Connect4(8,7)
    myGame.register_player(4698, "franz")
    myGame.check_move(1, 4698)
    print(myGame.board)