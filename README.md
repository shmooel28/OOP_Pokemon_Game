# OOP_Pokemon_Game
![open_page](https://user-images.githubusercontent.com/93682110/148511971-7fdcd6a4-ebac-4c58-8005-9c0b7107a7b8.gif)
![open_page_pokemon](https://user-images.githubusercontent.com/93682110/148511974-5d51401e-9e19-4148-a739-435877eecf6e.jpg)


Description
--
I have developed a game where a group of agents have to catch many Pokemons as possible.
I planned for each agent a path for him so he can catch as many Pokemons as possible in the shortest amount of time in order to achieve the highest score possible.

There are 0-15 stages, each with a different amount of agents, Pokemons and a given time.
Every Pokemon that an Agent caught creates a new Pokemon in a random location on the graph.

In this project we received data from a server (jar file) and according to that the game is played.
The information of the game is represented as a JSON file.

Classes
--
to learn about the classes visit in wiki page https://github.com/shmooel28/OOP_Pokemon_Game/wiki/Classes

Algorithm
--
My Algorithm is a greedy algo, for every agent check for every pokemon that not allocat an agent, the sum of the pokemon value less the distance from the agent*10
then take the max sum and allocat the pokemon for the agent.
for saving in "move" acction, and yet not missing a pokemon, i check if their is an agent close to pokemon, if you have agent like this call move, else only call move 8.4 time in a seconde.

Requirements
--
java machine (JDK 11 or above)

python

install pygame

import json


Example
--
in the GUI you can see that have a stop button, and print the time left, grade and moves.
you can see you have to type of pokemon, one for pokemon type negative and one for type positive
The type is determined by the start and the end of the Pokemon sit on, if the start point lower than the end point, than the type is positive, else is negative

![game_photo](https://user-images.githubusercontent.com/93682110/148512029-1aebef39-c755-401f-a75e-e1a6e79d49b3.jpg)

How to run
--
Open the folder in the CMD and run the command line: java -jar Ex4_Server_v0.0.jar 0 <level_number>

run the Pokemon_game class

for the program work you must have a data folder that contain the graph: A0,A1,A2,A3 -https://github.com/shmooel28/OOP_Pokemon_Game/tree/master/data

![cmd_photo](https://user-images.githubusercontent.com/93682110/148512017-c8547702-2270-440c-b3ef-0d0f6fdfbf0b.jpg)


Results
--
see the results in the wiki page https://github.com/shmooel28/OOP_Pokemon_Game/wiki/Results

Download
--

$git clone  https://github.com/shmooel28/OOP_Pokemon_Game.git
