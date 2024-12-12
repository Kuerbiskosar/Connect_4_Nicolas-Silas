

from game import Connect4
from player import Player
import numpy as np
from enum import Enum
import ansi_wrapper
import sys

#because msvcrt only runs on windows, getch needs to be imported, when running on linux
if sys.platform.startswith('win'): #type: ignore #to suppress the pylance warning on linux
    from msvcrt import getch # to detect keyboard input
    isLinux = False
elif sys.platform.startswith('linux'):
    from getch import getch #type: ignore #to ignore the pylance warning on windows
    isLinux = True
else:
    raise NotImplementedError("You are not running on a linux or windows machine. Please note, that gaming on a mac is not supported. \
                              for more Information see: https://www.youtube.com/watch?v=IYv3-HfRNcA \
                              and https://www.youtube.com/watch?v=GCrfWmaBy6k")

class BoardIcon(Enum):
    """
    Represents the icons used on the game board.

    Attributes:
        empty (str):            Represents an empty cell on the board.
        player1 (str):          Symbol for Player 1.
        player2 (str):          Symbol for Player 2.
        player1_winning (str):  Symbol for Player 1's winning cells, denoted by a lowercase 'x'.
        player2_winning (str):  Symbol for Player 2's winning cells, denoted by a lowercase 'o'.
    """
    empty = ''
    player1 = 'X'
    player2 = 'O'
    # winning symbols are the symbols of the players as lowercase letters
    # winning symbols are the symbols of the players as lowercase letters
    player1_winning = 'x'
    player2_winning = 'o'

class Action(Enum):
    """
    Represents possible input actions in a human-readable way.

    Attributes:
        right (int):    Move to the right (value: 0).
        left (int):     Move to the left (value: 1).
        drop (int):     Drop a piece into the current column (value: 2).
    """
    right = 0
    left = 1
    drop = 2

# used to decode Windows keycodes
# should contain the same keys as Windows_Keycodes
class Linux_Keycodes(Enum):
    """
    Represents keycodes for Linux terminal input.

    Attributes:
        is_special (int):   Leader key (value: 27), which precedes special key sequences.
        
        Special Keys (with leader sequence):
            l_up (int):     Keycode for the up arrow key (value: 65).
            l_left (int):   Keycode for the left arrow key (value: 68).
            l_down (int):   Keycode for the down arrow key (value: 66).
            l_right (int):  Keycode for the right arrow key (value: 67).

        Keys without a leader:
            abort (int):    Keycode for the abort key, using Tab (value: 9) instead of Ctrl+C.
            esc (int):      Keycode for Esc, replaced by Tab (value: 9) due to conflict with leader key.
            enter (int):    Keycode for the Enter key (value: 10).

        Alpha Keys:
            w (int): Keycode for 'W' (value: 119).
            a (int): Keycode for 'A' (value: 97).
            s (int): Keycode for 'S' (value: 115).
            d (int): Keycode for 'D' (value: 100).
    """
    is_special = 27 #leader NOTE: after this another byte is send, that is part of the leader, that's why esc can't be used
    #the following keys are lead with a leaderKey
    l_up = 65 #up arrow
    l_left = 68 #left arrow
    l_down = 66 #down arrow
    l_right = 67 #right arrow

    # these keys don't have a leader
    abort = 9 # tab instad of ctrl+c, because ctrl + c already terminates the programm
    esc = 9 # tab instead of esc, because esc (27) is also the first byte of the leader key...
    enter = 10

    # alpha keys
    w = 119
    a = 97
    s = 115
    d = 100
 
# used to decode Windows keycodes
# should contain the same keys as Linux_Keycodes
class Windows_Keycodes(Enum):
    """
    Represents keycodes for Windows terminal input.

    Attributes:
        is_special (int):   Leader key (value: 224) used for arrow keys and navigation block keys.
        
        Special Keys (with leader sequence):
            l_up (int):     Keycode for the up arrow key (value: 72).
            l_left (int):   Keycode for the left arrow key (value: 75).
            l_down (int):   Keycode for the down arrow key (value: 80).
            l_right (int):  Keycode for the right arrow key (value: 77).

        Keys without a leader:
            abort (int):    Keycode for the abort command (Ctrl+C, value: 3).
            esc (int):      Keycode for the Esc key (value: 27).
            enter (int):    Keycode for the Enter key (value: 13).

        Alpha Keys:
            w (int): Keycode for 'W' (value: 119).
            a (int): Keycode for 'A' (value: 97).
            s (int): Keycode for 'S' (value: 115).
            d (int): Keycode for 'D' (value: 100).
    """
    is_special = 224 # leader for arrow keys and the navigation block
    #the following keys are lead with a leaderKey
    l_up = 72
    l_left = 75
    l_down = 80
    l_right = 77

    # these keys don't have a leader
    abort = 3 #ctrl + c
    esc = 27
    enter = 13

    # alpha keys
    w = 119
    a = 97
    s = 115
    d = 100
 
 

class Player_Local(Player):
    """ 
    Local Player (uses Methods of the Game directly).
    """

    def __init__(self, game:Connect4, **kwargs) -> None:
        """ 
        Initialize a local player.
            Implements all methods required by the Abstract Player class.

        Parameters:
            game (Connect4): Instance of the Connect4 game to which the player is linked.

        Attributes:
            game (Connect4): Stores the provided Connect4 game instance.
            icon (str): The player's icon, assigned during registration in the game.
            board (list or None): Variable to store the game board locally, reducing server calls.
        """
        super().__init__()  # Initialize id and icon from the abstract Player class
        self.game = game
        self.icon = self.register_in_game()
        self.board = None # variable to hold the board, to reduce server calls


    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The icon assigned to the player during registration.
        """
        self.name = input("Enter your name: ")
        return self.game.register_player(self.id, self.name)


    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        if str(self.game.get_status()["active_id"]) == str(self.id): # we need to cast the uuid to a str, because the remote game returns a string
            return True
        else: return False


    def get_game_status(self):
        """
        Get the current status of the game.

        Returns:
            dict: A dictionary containing the following keys:
                - "active_player" (str): Name of the active player.
                - "active_id" (str): ID of the active player.
                - "winner" (str or None): The winner of the game, or None if there is no winner yet.
                - "turn_number" (int): The current turn number.
        """
        return self.game.get_status()


    def get_action(self) -> Action:
        """
        Reads input from the user until a valid action for the game is detected.

        Continuously monitors user input for specific key presses that correspond to
        actions within the game (such as moving left, right, or dropping a piece).
        The function differentiates between Linux and Windows keycodes and handles
        special keys, including combinations like the arrow keys and other control inputs.

        Returns:
            Action: The action corresponding to the user's input, such as `Action.left`, 
                    `Action.right`, or `Action.drop`.

        Exits the program if Ctrl+C (abort) is pressed.
        """
        # gets user input until a key that does something is pressed
        while True:
            user_input = getch()
            #check if the linux or windows getch got executed
            if isinstance(user_input, str):
                keycodes = Linux_Keycodes
                isLinux = True
            else:
                keycodes = Windows_Keycodes
                isLinux = False
            user_input = ord(user_input) #converts to int, to make the special leader of linux readable

            # if the user presses ctrl + c, end the program
            if user_input == keycodes.abort.value:
                exit()
            elif user_input == keycodes.is_special.value:
                if isLinux:
                    _ = getch() # the linux leader key returns two characters. skip the second with this line
                # special values return two keycodes, which is why we need to call getch() again
                # needed, to avoid moving the cursor to the left, when pressing shift + k
                second_input = ord(getch())
                if second_input == keycodes.l_left.value:
                    return Action.left
                if second_input == keycodes.l_right.value:
                    return Action.right
            elif user_input == keycodes.a.value:
                return Action.left
            elif user_input == keycodes.d.value:
                return Action.right
            elif user_input == keycodes.enter.value:
                return Action.drop

    def make_move(self) -> int:
        """ 
        Prompt the physical player to enter a move via the console.

        Returns:
            int: The column chosen by the player for the move.
        """
        board = self.game.get_board()
        self.board = board
        width = len(board)
        while True:
            self.visualize(fetch_board=False)
            action = self.get_action()
            if action == Action.drop:
                if self.game.check_move(self.drop_position, self.id):
                    return self.drop_position
            elif action == Action.right and self.drop_position < width-1:
                self.drop_position += 1
            elif action == Action.left and self.drop_position > 0:
                self.drop_position -=1
    
    def visualize(self, fetch_board = True, write_turn = True) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.

        Parameters:
            fetch_board (bool): If True (or if no board was fetched before), the function calls `game.get_board()` to retrieve the latest board state.
                                Defaults to True. Used to reduce server calls.
            write_turn (bool):  If True, displays a message indicating whose turn it is.
                                Defaults to True. Should not be shown after the game ends.

        Returns:
            None
        """
        if fetch_board or self.board is None:
            board = self.game.get_board()
        else:
            board = self.board
        width = len(board)
        emptyIcon = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Black, background_color=ansi_wrapper.TerminalColors.Blue, background_bright=True)
        icon1 = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Yellow, background_color=ansi_wrapper.TerminalColors.Blue, background_bright = True)
        icon2 = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Red, background_color=ansi_wrapper.TerminalColors.Blue, background_bright=True)

        winner_icon1 = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Green, background_color=ansi_wrapper.TerminalColors.Blue, background_bright = True)
        winner_icon2 = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Orange, background_color=ansi_wrapper.TerminalColors.Blue, background_bright = True)

        width = len(board)
        height = len(board[0])
        output = ""
        myIcon = ""
        if self.icon == "X":
            myIcon = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Yellow, background_bright = True)
        else:
            myIcon = ansi_wrapper.colorprint(" ⬤ ",ansi_wrapper.TerminalColors.Red, background_bright=True)
        # range from width (exclusive) to 0 (inclusive) because the board position 0,0 is at the bottom left
        # only print the header, when the game is not yet over or it is my turn
        if self.drop_position >= 0 and self.is_my_turn():
            output_header = ["   "]*(width+1)
            output_header[self.drop_position] = myIcon
            output_header = ''.join(output_header)
            output += output_header + "\n"
        else:
            output += "\n"
        for y in range(height-1,-1,-1):
            for x in range(width):
                if board[x,y] == BoardIcon.empty.value:
                    output += emptyIcon
                elif board[x,y] == BoardIcon.player1.value:
                    output += icon1
                elif board[x,y] == BoardIcon.player2.value:
                    output += icon2
                elif board[x,y] == BoardIcon.player1_winning.value:
                    output += winner_icon1
                elif board[x,y] == BoardIcon.player2_winning.value:
                    output += winner_icon2
                else:
                    # if we don't know what the number in the array is supposed to represent,
                    # we could raise a exception, but this way funnier,
                    # and such a thing doesn't necessarily need to crash the game
                    output += "💩"
            output += "\n"
        ansi_wrapper.clear_screen()
        ansi_wrapper.set_cursorpos(0,0) # sets the cursor position to the top
        print(output)
        if not write_turn:
            return
        if self.is_my_turn():
            print(f"{self.name}! it is your turn!")
            print("select in which row you want to place your coin, by pressing <a>/<d> or <right arrow> / <Left arrow>")
        else:
            print("waiting for the opponent to play")

    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player

        Returns:
            None
        """
        self.drop_position = -1
        self.visualize(write_turn=False)
        print(f'Congratulations, {self.name} wins!')


def main():
    input("You are running the file player_local for debug purposes.")
    game = Connect4(7,6)
    player1 = Player_Local(game)

"""test the class"""
if __name__ == "__main__":
    main()