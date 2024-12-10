from enum import Enum
class TerminalColors(Enum):
    """
    A Class that defines the colors for Ansi formatting
    """
    Black = 0
    Red = 196#1
    Green = 35
    #Green = #2
    Yellow = 226#3
    Orange = 221
    Blue = 21#4
    #Magenta = #5
    #Cyan = #6
    #White = #7
    default = 1000

def colorprint(text:str,
               foreground_color:TerminalColors=TerminalColors.default,
               background_color:TerminalColors=TerminalColors.default,
               foreground_bright:bool=False, background_bright:bool=False,
               underline:bool=False,
               blink:bool=False,
               ) -> str:
    """returns the text string formattet to be printed into a terminal"""
    #foreground = (3+foreground_bright*6)*10+foreground_color.value # foreground_bright is a bool. if true, 6 will be added to 3
    #background = (4+background_bright*6)*10+background_color.value # normal colors are from 40 to 47, bright from 100 (=(4+6)*10 - 107
    #return(f"\033[{foreground};{background}{";4"*underline+";5"*blink}m{text}\033[0m")
    #return(f"\033[{background};{foreground}{";4"*underline+";5"*blink}m{text}\033[0m")
    print("\033[=19h")
    foreground = f"38;5;{foreground_color.value}"
    background = f"48;5;{background_color.value}"
    underline_and_blink = ";4"*underline+";5"*blink
    if foreground_color.value == 1000:
        foreground = "39"
    if background_color.value == 1000:
        background = "49"
    #return("\033[38;5;196;48;5;21mANSI RULES!\033[0m")
    return(f"\033[{foreground};{background}{underline_and_blink}m{text}\033[0m")
    #return(f"\033[{foreground};{background}{";4"*underline+";5"*blink}m{text}\033[0m")

def clear_screen() -> None:
    """clear the entire screen in the Terminal"""
    print("\033[2J", end="")

def set_cursorpos(x:int,y:int):
    """moves the terminal cursor to the specified location"""
    print(f"\033[{y};{x}H", end='')

def clear_line():
    """
    Clears the entire line, where the cursor is positioned and moves the cursor to the beginning of that line
    Returns: None
    """

    print(f"\033[2K", end = "") # deletes the whole line
    print(f"\033[0E", end = "") # moves cursor to the beginning of the line
    #print("\033M") # carriage return
    #print("                                                                                                 ", end = "")
    #print("\033M") # carriage return
    #print("\033[\0331B", end = "") # moves cursor down (because carriage return moves it up)


if __name__ == "__main__":
    import time
    #print("\033[\34;44mwell...")
    print("Hallo")
    print(colorprint("⬤", foreground_color=TerminalColors.Yellow, background_color=TerminalColors.Blue, underline=False,blink=False))
    print("wowie")
    while True:
        print("bober    ", end = "", flush= True)
        time.sleep(0.2)
        clear_line()
        print("bober .  ", end = "", flush= True)
        time.sleep(0.2)
        clear_line()
        print("bober .. ", end = "", flush= True)
        time.sleep(0.2)
        clear_line()
        print("bober ...", end = "", flush= True)
        time.sleep(0.2)
        clear_line()
    #print("dulibab")
    #print("dulibab")
