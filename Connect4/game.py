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
    
    def __init__(self, width, height) -> None:
        """ 
        Init a Connect 4 Game
            - Create an empty Board
            - Create two (non - registered and empty) players.
            - Set the Turn Counter to 0
            - Set the Winner to False
            - etc.
        """
        self.board = np.empty((width, height), dtype=str)    # Board 8x7 with zeros representing empty cells
        self.player_info = {}                       # Dictionary to map player UUID to icon
        self.players = []                           # a list with the players UUID's
        self.activeplayer = 0                       # index of the active player in the list 
        self.turn_counter = 0                       # To keep track of whose turn it is
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
        return (self.player_info[self.players[self.activeplayer]][0], self.winner, self.turn_counter)


    def register_player(self, player_id: uuid.UUID, name: str) -> str:
        """ 
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            player_id (UUID)    Unique ID

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
            print(self.player_info)
            return icon
        return None


    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state (For Example an Array of all Elements)

        Returns:
            board
        """
        return self.board


    def check_move(self, column:int, icon:str) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        """
        for i in range(len(self.board[column])):
            if self.board[column][i] == '':
                self.board[column][i] = icon
                self.__update_status()
                print(self.activeplayer)
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
        self.activeplayer = self.activeplayer*-1 + 1
        self.turn_counter += 1
        self.__detect_win()
    

    def __detect_win(self)->bool:
        """ 
        Detect if someone has won the game (4 consecutive same pieces).
        
        Returns:
            True if there's a winner, False otherwise
        """    
        horizontal_check = [(0,0), (0,1), (0,2), (0,3)]
        for y in range(self.height):
            for x in range(self.width - 3):
                for i in horizontal_check:
                    if self.board[x + i[0], y + i[1]] == self.player_info[self.players[self.activeplayer]][0]:
                        self.winner = self.players[self.activeplayer]
                    else: 
                        self.winner = None
                        break
        
        diagonal_down_check = [(0,3), (1,2), (2,1), (3,0)]
        for y in range(self.height - 3):
            for x in range(self.width - 3):
                for i in diagonal_down_check:
                    print(y)
                    print(i)
                    if self.board[x + i[0], y + i[1]] == self.player_info[self.players[self.activeplayer]][0]:
                        self.winner = self.players[self.activeplayer]
                    else: 
                        self.winner = None
                        break
        
        #raise NotImplementedError(f"You need to write this code first")


if __name__ == "__main__":
    myGame = Connect4()