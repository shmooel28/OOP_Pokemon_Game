import json
import time

import src.client
from src.Agent import Agent
from src.Pokemon import Pokemon


class Game_Algo:
    # class for the main Algorithm of the game
    def __init__(self, graph):
        self.Agent = {}
        self.Pokemon = []
        self.graph = graph

    def start_game_loc(self, num_of_agent, client):
        self.Pokemon.sort(key=lambda x: -x.value)
        for pok in self.Pokemon:
            pok.start_end_pos(self.graph)
            if num_of_agent != 0:
                str_js = "{\"id\":" + str(pok.src) + "}"
                client.add_agent(str_js)
                num_of_agent -= 1
            else:
                return
        center = self.graph.centerPoint
        for agent in range(num_of_agent):
            str_js = "{\"id\":" + str(center[0]) + "}"
            client.add_agent(str_js)

    def start_game_Agent(self, client: src.client):
        for e in self.Agent.values():
            for p in self.Pokemon:
                if e.src == p.src:
                    e.path.append(p.dest)
                    p.agent = e.id
                    break

    def update_Pokemon(self, json_str, num_of_pok):
        """
        update the list of pokemon and for each Pokemon update the src and dest
        :param json_str:
        :param num_of_pok:
        :return:
        """
        pokemons = json.loads(json_str)
        for pok in pokemons["Pokemons"]:
            temp_pok = Pokemon(pok)
            flag = True
            for p in self.Pokemon:
                if temp_pok.pos == p.pos:
                    flag = False
                    break
            if flag:
                self.Pokemon.append(temp_pok)
        if len(self.Pokemon) > num_of_pok:
            length = len(self.Pokemon)
            for i in range(length - num_of_pok):
                self.Pokemon.pop(0)
        for p in self.Pokemon:
            p.start_end_pos(self.graph)

    def update_Agent(self, json_str):
        """
        before the game, enter all the Agents to list of Agents
        :param json_str:
        :return:
        """
        agents = json.loads(json_str)
        for a in agents["Agents"]:
            if a not in self.Agent.values():
                temp_ag = Agent(a)
                self.Agent[temp_ag.id] = temp_ag

    def update_Agent_speed(self, json_str):
        """
        update the speed,src,and dest of the Agents
        :param json_str:
        :return:
        """
        agents = json.loads(json_str)
        for a in agents["Agents"]:
            id = a["Agent"]["id"]
            speed = a["Agent"]["speed"]
            self.Agent[id].speed = speed
            self.Agent[id].dest = a["Agent"]["dest"]
            self.Agent[id].src = a["Agent"]["src"]
            x, y, z = a["Agent"]["pos"].split(',')
            self.Agent[id].pos = (float(x), float(y), float(z))

    def choose_next_edge(self, client: src.client):
        """
        for every agent choose the next dest
        :param client:
        :return:
        """
        for agent in self.Agent.values():
            if agent.dest == -1:
                next_node = self.next_node(agent, client)
                client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')

    def next_node(self, agent: Agent, client: src.client):
        """
        This is the main algorithm of the game.
        check if the Agent path is not empty, and retrun the next dest
        if the path is empty, check the next Pokemon that the agent going to catch
        for every pokemon check the value less the distance*10 between the Agent, take the max resulte between all
        the Pokemons, and build a path to that Pokemon, return the first location of the path
        :param agent:
        :param client:
        :return: the next dest for the agent
        """
        max = float('-inf')
        index = -1
        count = -1
        if len(agent.path) > 0:
            return agent.path.pop(0)
        else:
            for pok in self.Pokemon:
                count += 1
                if pok.agent == -1:
                    score = pok.value - (self.dist(pok, agent) * 10)
                    if score > max:
                        max = score
                        index = count
            p = self.Pokemon[index]
            self.add_path(agent, agent.src, p.src, p.dest, client)
            self.Pokemon[index].agent = agent.id
            return agent.path.pop(0)

    def add_path(self, agent, src, dest1, dest2, client):
        """
        update the path of Agent to the src of Pokemon, and than to the Pokemon dest, using by Dijkstra algorithm
        :param src: start of Agent
        :param dest1: the start of the edge of the Pokemon sit on
        :param dest2: the end of the edge of the Pokemon sit on
        :param client: to check if it been change on the graph
        :return:
        """
        if src == dest1:
            agent.path.append(dest2)
            agent.src = dest2
            return
        agent.time_to_dest, agent.path = self.graph.shortest_path(src, dest1)
        if agent.time_to_dest == -1:
            self.graph.load_json_file(client.get_graph())
        agent.time_to_dest, agent.path = self.graph.shortest_path(src, dest1)
        agent.path.append(dest2)
        agent.src = dest2

    def dist(self, pok: Pokemon, agent: Agent):
        """
        calculation the value of the distane between Agent and Pokemon, use in Dijkstra algorithm
        :param pok:
        :param agent:
        :return: float
        """
        ans, _ = self.graph.shortest_path(agent.src, pok.src)
        return ans

    def check_close(self, client):
        """
        for not missing a Pokemon, if thier is agent next to the pokemon call the client
        :param client:
        :return:
        """
        for pok in self.Pokemon:
            if pok.agent != -1:
                if pok.src == self.Agent[pok.agent].src:
                    time.sleep(0.07)
                    client.move()
