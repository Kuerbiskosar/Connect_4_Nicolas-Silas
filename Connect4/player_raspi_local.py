import time

from sense_hat import SenseHat #type: ignore

from game import Connect4
from player_local import Player_Local
from player_local import Action
from player_local import BoardIcon


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
    
    def register_in_game(self):
        """
        Register the player in the game.

        Sets the player's name and icon, and registers the player in the game instance.

        Returns:
            str: The icon assigned to the player during registration.
        """
        # first do normal register
        #self.icon = super().register_in_game()          # call method of Parent Class (Player_Local)
        self.name = "Raspberry"
        return self.game.register_player(self.id, name=self.name)

    def visualize(self, fetch_board = True, write_turn = True) -> None:
        """
        Override the visualization of the local player, also visualizing on the Raspberry Pi.

        This function updates the LED matrix on the Raspberry Pi with the current state of the game board.
        It highlights the selected column, updates the board with player icons, and shows winning icons 
        for players if applicable.

        Parameters:
            fetch_board (bool): If True, fetches the board from the game; otherwise, uses the cached board.
            write_turn (bool): If True, writes the current player's turn message to the console.

        Returns:
            None
        """
        # Define colors
        nonboard = [0,0,0] # black for cells above the board
        emptyIcon = [155, 155, 155]  # White for empty cells
        icon1 = [255, 255, 0]  # Yellow for Player 1
        icon2 = [255, 0, 0]  # Red for Player 2

        winner_icon1 = [0, 255, 0] # Green for win Player 1
        winner_icon2 = [255, 128, 0] # Orange for win Player 1

        # Prepare the LED matrix (8x8)
        matrix = [[nonboard for _ in range(8)] for _ in range(8)]
        
        if fetch_board or self.board is None:
            board = self.game.get_board()
        else:
            board = self.board

        # visualize the choice on the top of the board
        if self.drop_position >= 0 and self.is_my_turn():
            if self.icon == BoardIcon.player1.value:
                highlight = [255, 255, 0]  # Yellow for Player 1
            elif self.icon == BoardIcon.player2.value:
                highlight = [255, 0, 0]  # Red for Player 2
            top_row = [highlight if col == self.drop_position else nonboard for col in range(8)]

            matrix[7-len(board[0])] = top_row 

        # Map the Connect4 board onto the LED matrix
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == BoardIcon.player1.value:
                    matrix[7 - y][x] = icon1
                elif board[x][y] == BoardIcon.player2.value:
                    matrix[7 - y][x] = icon2
                elif board[x][y] == BoardIcon.player1_winning.value:
                    matrix[7 - y][x] = winner_icon1
                elif board[x][y] == BoardIcon.player2_winning.value:
                    matrix[7 - y][x] = winner_icon2
                elif board[x][y] == BoardIcon.empty.value:
                    matrix[7-y][x] = emptyIcon

        # Flatten the matrix and send it to the Sense HAT
        flattened_matrix = [pixel for row in matrix for pixel in row]
        self.sense.set_pixels(flattened_matrix)

        # Also update the column selection
        #self.visualize_choice(self.drop_position)

        # OPTIONAL: Visualize on CLI
        super().visualize(fetch_board, write_turn)

    def get_action(self) -> int:
        """
        Override make_move for Raspberry Pi input using the Sense HAT joystick.
        Uses joystick to move left or right and select a column.

        Returns:
            col (int):  Selected column (0...7)
        """
        #super().visualize()
        while True:
            event = self.sense.stick.wait_for_event()
            if event.action == 'pressed':
                if event.direction == 'left':
                    return Action.left
                elif event.direction == 'right':
                    return Action.right
                elif event.direction == 'middle':
                    return Action.drop  
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI win of Raspberry Pi player.
            Winning line gets highlighted.
        """
        super().celebrate_win()