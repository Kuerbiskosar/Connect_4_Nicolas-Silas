import uuid
import numpy as np
import requests
import json # used to read ip's from file
import os # used to read ip's from file

class Connect4_remote:
    """
    Talks to a game instance on a remote server through api calls
    Other scripts can interact with this class the same way they can with the game class (after it was initiated)
    """
    def __init__(self, url:str) -> None:
        """
        Parameters:
            url (str)       the url of the game server
        """
        self.url = url

    def get_status(self) -> tuple:
        """
        Get the game's status.
            - active player (id or icon)
            - is there a winner? if so who?
            - what turn is it?
                <-1> means the game hasn't started yet
        """
        response = requests.get(self.url+"/connect4/status")
        self.__check_response(response)
        active_player = response.json().get("active_player")
        active_id = response.json().get("active_id")
        winner = response.json().get("winner")
        turn_number = response.json().get("turn_number")
        return {"active_player":active_player,
                "active_id":active_id,
                "winner":winner,
                "turn_number":turn_number}

    def register_player(self, player_id:uuid.UUID, name: str = None):
        """ 
        Register a player with a unique ID
            Save his ID as one of the local players
        
        Parameters:
            player_id (UUID)    Unique ID
            name (str)          String

        Returns:
            icon:       Player Icon (or None if failed)
        """
        Player = {"player_id" : str(player_id), "name" : name}

        response = requests.post(self.url+"/connect4/register", json=Player)
        self.__check_response(response)
        return response.json().get("icon")


    def get_board(self)-> np.ndarray:
        """ 
        Return the current board state

        Returns:
            board (Array)
        """
        response = requests.get(self.url+"/connect4/board")
        self.__check_response(response)
        returned_board = response.json().get("board")
        # in the specification, the y axis 0 position is at the top. ours is at the bottom. that's why they have to be flipped.
        # x and y get switched too
        board = np.array(
            [
                [returned_board[row][collumn] for row in range(len(returned_board)-1, -1, -1)] # construct a collumn (flipping the entries, to make zero at the bottom of the board)
                for collumn in range(len(returned_board[0]))
            ]
        )
        return board

    def check_move(self, column:int, player_id:uuid) -> bool:
        """ 
        Check move of a certain player is legal
            If a certain player can make the requested move
            if so, makes the move and returns true

        Parameters:
            col (int):      Selected Column of Coin Drop
            player (uuid):   Player ID 
            
        Returns:
            bool    True if the move was valid, false otherwise
        """
        move = {"column":column, "player_id":str(player_id)}
        response = requests.post(self.url+"/connect4/check_move", json=move)
        if response.status_code == 400:
            return False
        if response.status_code == 200:
            return True
        self.__check_response(response)
        # if the code reaches this point, the response was between 201 and 299
        # this is undefined behaviour, thus we raise an error
        raise RuntimeError(f"Server response not as specified by the api: {response.status_code}")

    def __check_response(self, response):
        """
        Validate the HTTP response from the server.
            Checks if the response status code is within the 2xx range.
            If not, it raises a RuntimeError with a relevant error message.

        Parameters:
            response (object): HTTP response object, containing attributes 
                            `status_code` and `json()`.

        Returns:
            None

        Raises:
            RuntimeError: Raised if the status code is not in the 2xx range, 
                        with an appropriate error message.
        """
        if response.status_code < 200 or response.status_code > 299:
            print(r"a error occurred during server lookup -.- check https://developer.mozilla.org/en-US/docs/Web/HTTP/Status for more information (#notsponsored)")
            try:
                description = response.json().get("description")
            except:
                description = "the server did not return an error description"
            raise RuntimeError(f"Server response {response.status_code, description}")

if __name__ == "__main__":
    adresspath = "ip_address.json"
    if os.path.isfile(adresspath):
        with open(adresspath) as json_file:
            adresses = json.load(json_file)
            print(adresses)
            local_url = 'http://'+adresses.get("offshore")
    else:
        local_url = 'http://'+input("please input the desired adress (if given an ip, follow it with :<portnumber>)")
    game = Connect4_remote(local_url)
    game.register_player(4856345)
    game.check_move(2, player_id=4856345)
    game.get_board()
    game.check_move(2, player_id=4856345)