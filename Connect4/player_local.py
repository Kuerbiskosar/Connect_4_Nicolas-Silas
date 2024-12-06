

from game import Connect4
from player import Player
import numpy as np
from enum import Enum
import ansi_wrapper
import sys

#because msvcrt only runs on windows, getch needs to be imported, when running on linux
#TODO: Find the recommended way to do this
if sys.platform.startswith('win'): #type: ignore #to suppress the pylance warning on linux
    from msvcrt import getch # to detect keyboard input TODO: add as dependency
    isLinux = False
elif sys.platform.startswith('linux'):
    from getch import getch #type: ignore #to ignore the pylance warning on windows
    isLinux = True
else:
    raise NotImplementedError("You are not running on a linux or windows machine. Please note, that gaming on a mac is not supported. \
                              for more Information see: https://www.youtube.com/watch?v=IYv3-HfRNcA \
                              and https://www.youtube.com/watch?v=GCrfWmaBy6k")

class BoardIcon(Enum):
    empty = ''
    player1 = 'X'
    player2 = 'O'
    # winning symbols are the symbols of the players as lowercase letters
    # winning symbols are the symbols of the players as lowercase letters
    player1_winning = 'x'
    player2_winning = 'o'

class Action(Enum):
    """represents the possible input actions in a human readable way"""
    right = 0
    left = 1
    drop = 2

# used to decode Windows keycodes
# should contain the same keys as Windows_Keycodes
class Linux_Keycodes(Enum):
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
    """abstracting the special keycodes of special keys. keys that send the is_special key first are marked with l_<Key name>"""
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
            Must Implement all Methods from Abstract Player Class

        Parameters:
            game (Connect4): Instance of Connect4 game passed through kwargs.
        
       
        """
        super().__init__()  # Initialize id and icon from the abstract Player class
        self.game = game
        self.icon = self.register_in_game()


    def register_in_game(self) -> str:
        """
        Register the player in the game and assign the player an icon.

        Returns:
            str: The player's icon.
        """
        self.name = input("Enter your name: ")
        return self.game.register_player(self.id, self.name)


    def is_my_turn(self) -> bool:
        """ 
        Check if it is the player's turn.

        Returns:
            bool: True if it's the player's turn, False otherwise.
        """
        if self.game.get_status()["active_id"] == self.id:
            return True
        else: return False


    def get_game_status(self):
        """
        Get the game's current status.
            - who is the active player?
            - is there a winner? if so who?
            - what turn is it?
      
        """
        return self.game.get_status()


    def get_action(self) -> Action:
        #TODO: unify linux and windows commands (and make arrow keys work on linux)
        """reads input from the user, until the keypress corresponds to a action in the game"""
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
        width = len(board)
        while True:
            self.visualize()
            action = self.get_action()
            if action == Action.drop:
                if self.game.check_move(self.drop_position, self.icon):
                    return self.drop_position
            elif action == Action.right and self.drop_position < width-1:
                self.drop_position += 1
            elif action == Action.left and self.drop_position > 0:
                self.drop_position -=1
    
    def visualize(self) -> None:
        """
        Visualize the current state of the Connect 4 board by printing it to the console.
        """
        board = self.game.get_board()
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
        # only print the header, when the game is not yet over
        if self.drop_position >= 0:
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
        print(f"{self.name}! it is your turn!")
        print("select in which row you want to place your coin, by pressing <a>/<d> or <right arrow> / <Left arrow>")
        #print(myIcon)

    def celebrate_win(self) -> None:
        """
        Celebration of Local CLI Player
        """
        self.drop_position = -1
        self.visualize()
        print(f'Congratulations, {self.name} wins!')


def main():
    input("You are running the file player_local for debug purposes.")
    game = Connect4(7,6)
    player1 = Player_Local(game)
    #print(player1.make_move())
    #board = np.zeros((8,7))
    #player1.visualize(board)
    #board[1,0] = 1
    #board[1][1] = 2
    #player1.visualize(board,useAscii=True)

"""test the class"""
if __name__ == "__main__":
    main()