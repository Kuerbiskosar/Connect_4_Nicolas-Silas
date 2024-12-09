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

        # TODO: setup other Raspi stuff here

    
    def register_in_game(self):
        """
        Register in game
            Set Player Icon 
            Set Player Color
        """
        # first do normal register
        #self.icon = super().register_in_game()          # call method of Parent Class (Player_Local)
        self.name = "Raspberry"
        return self.game.register_player(self.id, name=self.name)

        #raise NotImplementedError(f"Override register_in_game of Player_Raspi_Locap")

    
    def visualize_choice(self, column:int)->None:
        """ 
        TODO: remove this function. it is not used anymore
        Visualize the SELECTION process of choosing a column
            Toggles the LED on the top row of the currently selected column

        Parameters:
            column (int):       potentially selected Column during Selection Process
        """
        raise NotImplementedError("this function should not be called anymore, because it does not work as intended")
        # Define colors
        empty = [55, 55, 55]  # White for empty cells
        if self.icon == BoardIcon.player1.value:
            highlight = [255, 255, 0]  # Yellow for Player 1
        elif self.icon == BoardIcon.player2.value:
            highlight = [255, 0, 0]  # Red for Player 2

        # Prepare the top row only
        top_row = [highlight if col == column else empty for col in range(8)]

        # Get the current board visualization
        board_display = [[empty for _ in range(8)] for _ in range(8)]
        board = self.game.get_board()

        # Map the game board onto the display
        icon1 = [255, 255, 0]  # Yellow for Player 1
        icon2 = [255, 0, 0]  # Red for Player 2
        for x in range(len(board)):
            for y in range(len(board[0])):
                if board[x][y] == BoardIcon.player1.value:
                    board_display[7 - y][x] = icon1
                elif board[x][y] == BoardIcon.player2.value:
                    board_display[7 - y][x] = icon2

        # Replace the top row with the column highlight
        board_display[0] = top_row

        # Flatten the display array and update the Sense HAT
        flattened_display = [pixel for row in board_display for pixel in row]
        print(flattened_display)
        #self.sense.set_pixels(flattened_display)


    def visualize(self, fetch_board = True, write_turn = True) -> None:
        """
        Override Visualization of Local Player
            Also Visualize on the Raspi 
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

        #raise NotImplementedError(f" visualize on Raspi not yet implemented")

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
            #print(f"events: {events}")
        #super().make_move()
        
        #raise NotImplementedError(f"make_move not yet implemented on Player_Raspi_Local")
    
    
    def celebrate_win(self) -> None:
        """
        Celebrate CLI Win of Raspi player
            Override Method of Local Player
        """
        # TODO: Own Celebration Method on SenseHat

        # Optional: also do CLI celebration
        super().celebrate_win()