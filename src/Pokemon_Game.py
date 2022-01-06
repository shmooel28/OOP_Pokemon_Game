"""
OOP - Ex4
main code and GUI for python client to communicates with the server and "play the game!"
"""

import json

from src.GUI import GUI
from src.Game_Algo import Game_Algo
from src.GraphAlgo import GraphAlgo
from src.client import *

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

client = Client()
client.start_connection(HOST, PORT)

num_of_agent = json.loads(client.get_info())["GameServer"]["agents"]
num_of_pokemon = json.loads(client.get_info())["GameServer"]["pokemons"]

graph_algo = GraphAlgo()
graph_algo.load_json_file(client.get_graph())

# before the game, set all the preparations
game = Game_Algo(graph_algo)
game.update_Pokemon(client.get_pokemons(), num_of_pokemon)
game.start_game_loc(num_of_agent, client)
game.update_Agent(client.get_agents())
game.start_game_Agent(client)

ui = GUI(game, client)

# this command starts the server - the game is running now
client.start()
client.move()

flag = 1

while client.is_running() == 'true':
    game.update_Pokemon(client.get_pokemons(), num_of_pokemon)
    game.update_Agent_speed(client.get_agents())
    ui.run()
    game.choose_next_edge(client)
    if flag == 2:
        client.move()
        flag = 0
    else:
        game.check_close(client)
        flag += 1
