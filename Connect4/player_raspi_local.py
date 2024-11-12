import time

from sense_hat import SenseHat #type: ignore

from game import Connect4
from player_local import Player_Local


class Player_Raspi_Local(Player_Local):
    """ 
    Local Raspi Player 
        Same as Local Player -> with some changed methods
            (uses Methods of Game and SenseHat)
    """

    def __init__(self, game:Connect4, **kwargs) -> None:
        """ 
        Initialize a local Raspi player with a shared SenseHat instance.

        Parameters:
            game (Connect4): Game instance.
            sense (SenseHat): Shared SenseHat instance for all players. (if SHARED option is used)
        
        Raises:
            ValueError: If 'sense' is not provided in kwargs.
        """
        # Initialize the parent class (Player_Local)
        # TODO: The player can't input his name, if he plays on the raspi... fix that somehow (probably just not doing the super init)
        super().__init__(game, **kwargs)

        # Extract the SenseHat instance from kwargs  (only if SHARED instance)
        # Remove Otherwise
        try:
            self.sense: SenseHat = kwargs["sense"]
        except KeyError:
            raise ValueError(f"{type(self).__name__} requires a 'sense' (SenseHat instance) attribute")

        # TODO: setup other Raspi stuff here

    
    def register_in_game(self):
        """
        Register in game
            Set Player Icon 
            Set Player Color
        """
        # first do normal register
        #self.icon = super().register_in_game()          # call method of Parent Class (Player_Local)
        return super().register_in_game()

        # TODO: also set color of the player

        #raise NotImplementedError(f"Override register_in_game of Player_Raspi_Locap")

    
    def visualize_choice(self, column:int)->None:
        """ 
        Visualize the SELECTION process of choosing a column
            Toggles the LED on the top row of the currently selected column

        Parameters:
            column (int):       potentially selected Column during Selection Process
        """
        

    def visualize(self) -> None:
        """
        Override Visualization of Local Player
            Also Visualize on the Raspi 
        """

        # TODO: visualize Board on raspi

        # OPTIONAL: also visualize on CLI
        super().visualize()

        #raise NotImplementedError(f" visualize on Raspi not yet implemented")

    def make_move(self) -> int:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.

        Returns:
            col (int):  Selected column (0...7)
        """
        super().make_move()
        
        #raise NotImplementedError(f"make_move not yet implemented on Player_Raspi_Local")
    
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Raspi player
            Override Method of Local Player
        """
        # TODO: Own Celebration Method on SenseHat

        # Optional: also do CLI celebration
        super().celebrate_win()