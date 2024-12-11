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
    
    def __init__(self, width = 8, height = 7) -> None:
        """ 
        Init a Connect 4 Game
            - Create an empty Board
            - Create two (non - registered and empty) players.
            - Set the Turn Counter to 0
            - Set the Winner to False
            - etc.
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
            - active player (id or icon)
            - is there a winner? if so who?
            - what turn is it?
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
            player_id (UUID)    Unique ID
            name (str)          the Name of the player

        Returns:
            icon:       Player Icon (or None if failed)
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
            board
        """
        return self.board


    def check_move(self, column:int, id:str = None, icon:str = None) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move
            if so, makes the move and returns true

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
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
            - active ID
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
            True if there's a winner, False otherwise
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



#        # Horizontal Check
#        for y in range(self.height):
#            for x in range(self.width - 3):  # Only go as far as possible for 4 in a row
#                if all(self.board[x + i, y] == icon for i in range(4)):
#                    self.winner = self.players[self.activeplayer]
#                    # set the fields to winner fields
#                    for i in range (4):
#                        self.board[x+i, y] = icon.lower()
#                    print(icon.lower)
#                    return True
#
#        # Vertical Check
#        for x in range(self.width):
#            for y in range(self.height - 3):  # Only go as far as possible for 4 in a column
#                if all(self.board[x, y + i] == icon for i in range(4)):
#                    self.winner = self.players[self.activeplayer]
#                    return True
#
#        # Diagonal Down Check (Top-left to Bottom-right)
#        for x in range(self.width - 3):
#            for y in range(self.height - 3):
#                if all(self.board[x + i, y + i] == icon for i in range(4)):
#                    self.winner = self.players[self.activeplayer]
#                    return True
#
#        # Diagonal Up Check (Bottom-left to Top-right)
#        for x in range(self.width - 3):
#            for y in range(3, self.height):  # Start from y = 3 for upward diagonal
#                if all(self.board[x + i, y - i] == icon for i in range(4)):
#                    self.winner = self.players[self.activeplayer]
#                    return True

        # No winner detected
        self.winner = None
        return False

        
        #raise NotImplementedError(f"You need to write this code first")


if __name__ == "__main__":
    myGame = Connect4(8,7)
    myGame.register_player(4698, "franz")
    myGame.check_move(1, 4698)
    print(myGame.board)