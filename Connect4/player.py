from abc import ABC, abstractmethod
import uuid

class Player(ABC):
    """
    Abstract Base Player class to define common methods for both Local and Remote players.

    Attributes:
        id (UUID): Unique identifier for the player.
        icon: The player's icon used in the game. (set during registration)
        board_width (int):  Number of Horizontal Elements 
        board_height (int): Number of Vertical Elements
    """

    def __init__(self) -> None:
        self.id = uuid.uuid4()          # Assign a unique ID to the player
        self.icon = None                # Set during registration
        self.name = ""                  # Player's name

        self.board_width:int = 8        # Set the width of the board
        self.board_height:int = 7       # Set the height of the board
        
    @abstractmethod
    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon.

        """
        
        raise NotImplementedError("Subclasses must implement 'register_in_game'")

    @abstractmethod
    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        raise NotImplementedError("Subclasses must implement 'is_my_turn'")

    @abstractmethod
    def get_game_status(self) -> tuple[str,str,bool,int]:
        """
        Get the game's current status.
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
      
        """
        raise NotImplementedError("Subclasses must implement 'get_game_status'")

    @abstractmethod
    def make_move(self) -> int:
        """
        Prompt the player to make a move. 
        
        Returns:
            int: The column chosen by the player for the move.
        
        """
        raise NotImplementedError("Subclasses must implement 'make_move'")

    @abstractmethod
    def visualize(self)->None:
        """
        Visualize the current board state
        """
        raise NotImplementedError("Subclasses must implement 'visualize'")
    
    @abstractmethod
    def celebrate_win(self)->None:
        """
        Players personal "celebration" on how to visualize a Win
        """
        raise NotImplementedError("Subclasses must implement 'celebrate_win'")