

from game import Connect4
from player import Player
import numpy as np
from enum import Enum
import ansi_wrapper
from msvcrt import getch # to detect keyboard input TODO: add as dependency

class BoardIcon(Enum):
    empty = 0
    player1 = 1
    player2 = 2

class Action(Enum):
    """represents the possible input actions in a human readable way"""
    right = 0
    left = 1
    drop = 2
class Special_Keycodes(Enum):
    """abstracting the special keycodes of special keys. keys that send the is_special key first are marked with l_<Key name>"""
    is_special = b'\xe0' # leader for arrow keys and the navigation block
    #the following keys are lead with a leaderKey
    l_up = b'H'
    l_left = b'K'
    l_down = b'P'
    l_right = b'M'

    # these keys don't have a leader
    abort = b'\x03' #ctrl + c
    esc = b'\x1b'
    enter = b'\r'
    

class Player_Local(Player):
    """ 
    Local Player (uses Methods of the Game directly).
    """

    def __init__(self, game:Connect4, **kwargs) -> None:
        """ 
        Initialize a local player.
            Must Implement all Methods from Abstract Player Class

        Parameters:
            game (Connect4): Instance of Connect4 game passed through kwargs.
        
       
        """
        super().__init__()  # Initialize id and icon from the abstract Player class
        self.game = game
        self.name = input("Enter your name: ")
        while True:
            self.icon = input(f'Enter your icon for {self.name}:')
            if len(self.icon) == 1:
                break
            print('Please enter ony one charakter as your icon.')
        self.register_in_game()
        #raise NotImplementedError(f"You need to write this code first")

    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon.
        """
        return self.game.register_player(self.id, self.icon, self.name)
        #raise NotImplementedError(f"You need to write this code first")

    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")

    def get_game_status(self):
        """
        Get the game's current status.
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
      
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")

    def get_action(self) -> Action:
        """reads input from the user, until the keypress corresponds to a action in the game"""
        # gets user input until a key that does something is pressed
        while True:
            user_input = getch()
            match user_input:
                # if the user presses ctrl + c, end the program
                case Special_Keycodes.abort.value:
                    exit()
                case Special_Keycodes.is_special.value:
                    print("special value")
                    # TODO: remove horribly deep nesting
                    # needed, to avoid moving the cursor to the left, when pressing shift + k
                    second_input = getch()
                    match  second_input:
                        case Special_Keycodes.l_left.value:
                            return Action.left
                        case Special_Keycodes.l_right.value:
                            return Action.right
                        case _:
                            pass
                case b'a':
                    return Action.left
                case b'd':
                    return Action.right
                case Special_Keycodes.enter.value:
                    return Action.drop
                case _:
                    pass

    def make_move(self) -> int:
        """ 
        Prompt the physical player to enter a move via the console.

        Returns:
            int: The column chosen by the player for the move.
        """
        while True:
            self.visualize(self.game.board)
            action = self.get_action()
            if action == Action.drop:
                return self.drop_position
            elif action == Action.right and self.drop_position < self.board_width-1:
                self.drop_position += 1
            elif action == Action.left and self.drop_position > 0:
                self.drop_position -=1
    
    def visualize(self, board:np.ndarray, icon1:str="🟡", icon2:str="🔴", useAscii:bool=True) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        # TODO things to condiser:
        # importing the board as a list instead of a numpy array (that way remote players don't need to have it installed)
        # TODO Remove emojis
        emptyIcon = "🔘"
        if useAscii:
            emptyIcon = ansi_wrapper.colorprint(" ⬤ ",background_color=ansi_wrapper.TerminalColors.Blue, background_bright=True, foreground_color=ansi_wrapper.TerminalColors.default)
            icon1 = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Yellow, background_color=ansi_wrapper.TerminalColors.Blue, background_bright = True)
            icon2 = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Red, background_color=ansi_wrapper.TerminalColors.Blue, background_bright=True)
        width = len(board)
        height = len(board[0])
        output = ""
        # range from width (exclusive) to 0 (inclusive) because the board position 0,0 is at the bottom left
        output_header = ["   "]*(width+1)
        output_header[self.drop_position] = ansi_wrapper.colorprint(" ↓ ",blink=True)
        output_header = ''.join(output_header)
        output += output_header + "\n"
        for y in range(height-1,-1,-1):
            for x in range(width):
                if board[x,y] == BoardIcon.empty.value:
                    output += emptyIcon
                elif board[x,y] == BoardIcon.player1.value:
                    output += icon1
                elif board[x,y] == BoardIcon.player2.value:
                    output += icon2
                else:
                    # if we don't know what the number in the array is supposed to represent,
                    # we could raise a exception, but this way funnier,
                    # and such a thing doesn't necessarily need to crash the game
                    output += "💩"
            output += "\n"
        ansi_wrapper.clear_screen()
        ansi_wrapper.set_cursorpos(0,0) # sets the cursor position to the top
        print(output)
        print(f"{self.name}! it is your turn!")
        print("select in which row you want to place your coin, by pressing <a>/<d> or <right arrow> / <Left arrow>")


    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player
        """
        # TODO
        raise NotImplementedError(f"You need to write this code first")

def main():
    print("You are running the file player_local for debug purposes.")
    game = Connect4()
    player1 = Player_Local(game)
    print(player1.make_move())
    board = np.zeros((8,7))
    #player1.visualize(board)
    #board[1,0] = 1
    #board[1][1] = 2
    #player1.visualize(board,useAscii=True)

"""test the class"""
if __name__ == "__main__":
    main()