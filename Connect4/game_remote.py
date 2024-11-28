import uuid
import numpy as np
import requests

class game_remote:
    """
    Talks to a game instance on a remote server through api calls
    Other scripts can interact with this class the same way they can with the game class (after it was initiated)
    """
    def __init__(self) -> None:
        """
        Parameters:
            url (str)       the url of the game server
        """
        pass

    def get_status(self) -> tuple:
        """
        Get the game's status.
            - active player (id or icon)
            - is there a winner? if so who?
            - what turn is it?
        """
        pass
    def register_player(self, player_id:uuid.UUID, name: str):
        """ 
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            player_id (UUID)    Unique ID

        Returns:
            icon:       Player Icon (or None if failed)
        """
        pass

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
            if so, makes the move and returns true

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (str):   Player ID 
        Returns:
            bool    True if the move was valid, false otherwise
        """
        pass