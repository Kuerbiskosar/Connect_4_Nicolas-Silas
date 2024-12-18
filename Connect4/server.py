import uuid
import json # not needed, if names don't need to be generated
import random # dito
import os # dito
import socket                                               # to get own IP
from flask import Flask, request, jsonify, current_app                   # for api
from flask_swagger_ui import get_swaggerui_blueprint        # for swagger documentation


# local includes
from game import Connect4


class Connect4Server:
    """
    Game Server
        Runs on Localhost
    
    Attributes
        game (Connect4):    Local Instance of Connect4 Game (with all game rules)
        app (Flask):        Web Server Instance

    """
    def __init__(self):
        """
        Create a Connect4 Server on localhost (127.0.0.1)
        - Add SWAGGER UI Documentation
        - Expose API Methods
        """

        self.game = Connect4(8,7)  # Connect4 game instance
        self.app = Flask(__name__)  # Flask app instance

        # Swagger UI Configuration
        SWAGGER_URL = '/swagger/connect4/'
        API_URL = '/static/swagger.json'  # This points to the static swagger.json file
        
        swaggerui_blueprint = get_swaggerui_blueprint(
            SWAGGER_URL,
            API_URL,
            config={  # Swagger UI config overrides
                'app_name': "Connect 4 API",
                'layout': "BaseLayout"  # You can choose other layouts
            }
        )

        # Register the Swagger UI blueprint
        self.app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


        # Define API routes within the constructor
        self.setup_routes()

    def setup_routes(self):
        """
        Expose the Methods
            - /connect4/status
            - /connect4/register
            - /connect4/board
            - /connect4/check_move
        """
        # Overall Description
        @self.app.route('/')
        def index():
            return "Welcome to the Connect 4 API!"



        # 1. Expose get_status method
        @self.app.route('/connect4/status', methods=['GET'])
        def get_status():
            try:
                status = self.game.get_status()
                return jsonify(status)
            except Exception as e:
                return jsonify({"description": "Failed to get game status", "details": str(e)}), 500


        # 2. Expose register_player method
        @self.app.route('/connect4/register', methods=['POST'])
        def register_player():
            # TODO Register the player and return the ICON
            # ERROR: game.register_player takes a player UUID and a name
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400
                uuid = data.get("player_id")
                name = data.get("name")
                if not name:
                    # because the API doesn't expose the players name, if none is given a random one will be assigned

                    #with open(os.getcwd()+"/Connect4/girl_boy_names_2023.json") as json_file:
                    with current_app.open_resource('application/girl_boy_names_2023.json') as json_file:
                        dict = json.load(json_file)
                        # choose if boy or girl with the ratio of girls / boys in the python course (0.05)
                        choice = random.randint(1,80)
                        if choice > 4:
                            # boy
                            names = dict.get("boys")
                        else:
                            # girl
                            names = dict.get("girls")
                    name = names[random.randint(0, len(names)-1)]
                    print(name)
                if not uuid:
                    print("No uuid provided")
                    return jsonify({"description": "No uuid provided"}), 400
                icon = self.game.register_player(uuid, name)
                if icon is None:
                    print("Maximum number of players reached")
                    return jsonify({"description": "Maximum number of players reached"}), 400
                return jsonify({"icon":icon})
            except Exception as e:
                return jsonify({"error": "Failed to register player", "details": str(e)}), 500


        # 3. Expose get_board method
        @self.app.route('/connect4/board', methods=['GET'])
        def get_board():
            # TODO correctly return the Board
            # note that game.get_board() also returns x and o (lowercase) after the game was won,
            # but we don't care if the game crashes, when the game is finished
            # ERROR: the format of the board from get_board does not match the specification
            try:
                board = self.game.get_board()
                # rearrange y positions so that 0 is at the top
                board = [
                        [board[collumn][row] for collumn in range(len(board))] # constructs a row of the board
                         for row in range(len(board[0])-1, -1, -1) # collummns get flipped because the zero point of the game is at the bottom, 
                                                                   #but the one that the server should return at the top
                         ]
                return jsonify({"board":board})
            except Exception as e:
                return jsonify({"description": "Failed to retrieve board: {e}", "details": str(e)}), 500

        # 4. Expose move method
        @self.app.route('/connect4/check_move', methods=['POST'])
        def make_move():
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"description": "No data provided"}), 400
                column = data.get("column")
                player_id = data.get("player_id")
                if column is None or player_id is None:
                    return jsonify({"description": "Column and Player ID are required"}), 400
                column = int(column)
                check_move = self.game.check_move(column, id=player_id)
                if not check_move:
                    return jsonify({"description": "Illegal move"}), 400
                return jsonify(check_move)
            except Exception as e:
                return jsonify({"description": f"Failed to make move: {e}", "details": str(e)}), 500
        


    def run(self, debug=True, host='0.0.0.0', port=5000):
        # Get and display the local IP address
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Server is running on {local_ip}:{port}")

        # Start the Flask app
        self.app.run(debug=debug, host=host, port=port)



# If you want to run the server directly:
if __name__ == '__main__':
    server = Connect4Server()  # Initialize the Connect4Server
    server.run()               # Start the Flask app