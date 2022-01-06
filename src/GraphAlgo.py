import json
import random
from math import sqrt
from queue import PriorityQueue
from typing import List

import pygame

from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface


def draw_arrow(x1, x2, y1, y2):
    dx = x2 - x1
    dy = y2 - y1
    distance = sqrt(dx * dx + dy * dy)
    start_x = distance - 15
    end_x = start_x
    start_y = 5
    end_y = -5
    sin = dy / distance
    cos = dx / distance
    temp = start_x * cos - start_y * sin + x1
    start_y = start_x * sin + start_y * cos + y1
    start_x = temp
    temp = end_x * cos - end_y * sin + x1
    end_y = end_x * sin + end_y * cos + y1
    end_x = temp
    _x = [x2, int(start_x), int(end_x)]
    _y = [y2, int(start_y), int(end_y)]
    return _x, _y


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, g: DiGraph = DiGraph()):
        self.graph = g
        # self.edges = [[]]
        self.path = [[]]
        self.change_flag = True
        self._mc = int(self.graph.get_mc())

    def update(self):
        self.path = [[[] for _ in range(self.graph.v_size())] for _ in range(self.graph.v_size())]
        for i in self.graph.edge_dic:
            self.path[i[0]][i[1]] = [i[1]]
        self.change_flag = False
        self._mc = int(self.graph.get_mc())
        for i in self.graph.get_all_v():
            self.graph.get_node(i).dijkstra_flag = False

    def get_graph(self):
        """:return the graph that you use for the algo"""
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """load graph from json file, return true if succeed"""
        try:
            with open(file_name, "r") as f:
                self.graph = DiGraph()
                j = json.load(f)
                for n in j["Nodes"]:
                    Id = int(n["id"])
                    self.graph.add_node(Id)
                    try:
                        s = n["pos"]
                        str_split = s.split(",")
                        self.graph.get_node(n["id"]).pos = (
                            float(str_split[0]), float(str_split[1]), float(str_split[2]))
                    except:
                        pass
                for e in j["Edges"]:
                    self.graph.add_edge(int(e["src"]), int(e["dest"]), float(e["w"]))
            self.change_flag = True
            self.dist = [[0 for _ in range(self.graph.v_size())] for _ in range(self.graph.v_size())]
            return True
        except:
            return False

        pass

    def load_json_file(self, json_str_g):
        #print(json_str[0])
        json_str = json.loads(json_str_g)
        self.graph = DiGraph()
        #j = json.load(json_str, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
        for n in json_str["Nodes"]:
            Id = int(n["id"])
            self.graph.add_node(Id)
            try:
                s = n["pos"]
                str_split = s.split(",")
                self.graph.get_node(n["id"]).pos = (
                    float(str_split[0]), float(str_split[1]), float(str_split[2]))
            except:
                pass
        for e in json_str["Edges"]:
            self.graph.add_edge(int(e["src"]), int(e["dest"]), float(e["w"]))

        self.change_flag = True
        self.dist = [[0 for _ in range(self.graph.v_size())] for _ in range(self.graph.v_size())]
    def save_to_json(self, file_name: str) -> bool:
        """save the graph in json format, return true if succeed"""
        try:
            dict_json = {}
            for e in self.graph.edge_dic:
                temp = self.graph.edge_dic[e]
                if "Edges" in dict_json:
                    dict_json["Edges"].append({"src": e[0], "w": temp, "dest": e[1]})
                else:
                    dict_json["Edges"] = [{"src": e[0], "w": temp, "dest": e[1]}]

            for n in self.graph.node_dic:
                temp = self.graph.node_dic[n]
                if "Nodes" in dict_json:
                    if temp.pos is not None:
                        dict_json["Nodes"].append({"pos": "" + str(temp.pos).strip('()'), "id": temp.id})
                    else:
                        dict_json["Nodes"].append({"id": temp.id})
                else:
                    if temp.pos is not None:
                        dict_json["Nodes"] = [{"pos": "" + str(temp.pos).strip('()'), "id": temp.id}]
                    else:
                        dict_json["Nodes"] = [{"id": temp.id}]
            with open(file_name, "w") as out:
                json.dump(dict_json, out, indent=4)
            return True
        except:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """return the sortest path between point a to point b using the dijkstra algo
            :return the time(float) and the path(list)
        """
        if self.change_flag or self._mc != self.graph.get_mc():
            self.update()
        if not self.graph.get_node(id1).dijkstra_flag:
            self.dijkstra(id1)
        if len(self.path[id1][id2]) == 0 and self.graph.get_node(id1).D[id2] != float:
            return -1,[]
        if self.graph.get_node(id1).D[id2] != float('inf') and self.path[id1][id2][0] != id1:
            self.path[id1][id2][:0] = [id1]
        return self.graph.get_node(id1).D[id2], self.path[id1][id2]

    def plot_graph(self) -> None:
        """represent the graph, if you dont have pos for the node, give them in random"""
        RED = (255, 0, 0)
        WHITE = (255, 255, 255)
        BLUE = (0, 0, 128)
        pygame.init()
        screen = pygame.display.set_mode([600, 600])
        running = True
        min_x = min_y = float('inf')
        max_x = max_y = float('-inf')
        for n in self.graph.node_dic:
            if self.graph.get_node(self.graph.node_dic[0].id).pos is not None:
                x, y, z = self.graph.node_dic[n].pos
                if x > max_x:
                    max_x = x
                if x < min_x:
                    min_x = x
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y
            else:
                location = [(i, i) for i in range(self.graph.v_size())]
                for n in self.graph.node_dic:
                    x = random.randint(0, self.graph.v_size() * 100)
                    y = random.randint(0, self.graph.v_size() * 100)
                    while (x, y) in location:
                        x = random.randint(0, self.graph.v_size() * 100)
                        y = random.randint(0, self.graph.v_size() * 100)
                    location[n] = (x, y)
                    if x > max_x:
                        max_x = x
                    if x < min_x:
                        min_x = x
                    if y > max_y:
                        max_y = y
                    if y < min_y:
                        min_y = y
        min_x -= 0.001
        max_x += 0.001
        min_y -= 0.001
        max_y += 0.001
        scaleX = (screen.get_width() / abs(max_x - min_x))
        scaleY = (screen.get_height() / abs(max_y - min_y))
        while running:
            screen.fill(WHITE)
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(10, 10, 580, 580), 2)
            if self.graph.get_node(self.graph.node_dic[0].id).pos is not None:
                for n in self.graph.node_dic:
                    x, y, z = self.graph.node_dic[n].pos
                    x = int((x - min_x) * scaleX)
                    y = int((y - min_y) * scaleY)
                    pygame.draw.circle(screen, RED, (x, y), 6)
                    font = pygame.font.Font('freesansbold.ttf', 10)
                    text = font.render(str(self.graph.node_dic[n].id), True, (0, 0, 0,))
                    textRect = text.get_rect()
                    textRect.center = (x + 5, y + 2)
                    screen.blit(text, textRect)
                for e in self.graph.edge_dic:
                    x1, y1, z1 = self.graph.get_node(e[0]).pos
                    x2, y2, z2 = self.graph.get_node(e[1]).pos
                    x1 = int((x1 - min_x) * scaleX)
                    y1 = int((y1 - min_y) * scaleY)
                    x2 = int((x2 - min_x) * scaleX)
                    y2 = int((y2 - min_y) * scaleY)
                    pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2))
                    _x, _y = draw_arrow(x1, x2, y1, y2)
                    points = [i for i in range(len(_x))]
                    for i in range(len(_x)):
                        points[i] = (_x[i], _y[i])
                    pygame.draw.polygon(screen, BLUE, points)
            else:
                for n in self.graph.node_dic:
                    pygame.draw.circle(screen, RED, location[n], 6)
                for e in self.graph.edge_dic:
                    x1, y1 = location[e[0]]
                    x2, y2 = location[e[1]]
                    pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2))
                    _x, _y = draw_arrow(x1, x2, y1, y2)
                    points = [i for i in range(len(_x))]
                    for i in range(len(_x)):
                        points[i] = (_x[i], _y[i])
                    pygame.draw.polygon(screen, BLUE, points)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
        pygame.quit()
        pass

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """:return the fastest way to path in list of nodes and the time to path them the algorithm is greedy,
        every time check the min way between two point in your list and add that way for your list
        """
        cities = []
        for i in node_lst:
            cities.append(i)
        ans = []
        temp = []
        count = 0.0
        mini = float('inf')
        index = -1
        for i in node_lst:
            for j in node_lst:
                d, path = self.shortest_path(i, j)
                if d < mini and d != 0:
                    mini = d
                    temp = path
        count += mini
        for i in temp:
            ans.append(i)
            index += 1
        for i in ans:
            if i in node_lst:
                node_lst.remove(i)
        while len(node_lst) != 0:
            mini = float('inf')
            temp = []
            for i in node_lst:
                d, path = self.shortest_path(ans[index], i)
                if d < mini and d != 0:
                    mini = d
                    temp = path
            if mini == float('inf'):
                node_lst = []
                for j in cities:
                    node_lst.append(j)
                ans = []
                ans.append(i)
                node_lst.remove(i)
                count = 0
                index = 0
            if mini != float('inf'):
                count += mini
            for i in temp:
                if i != temp[0]:
                    ans.append(i)
                    index += 1
            for i in ans:
                if i in node_lst:
                    node_lst.remove(i)

        return ans, count

    def centerPoint(self) -> (int, float):
        """Finds the node that has the shortest distance to it's farthest node.
            the idea of the algorithm its for evrey nodes find the max distance,and from all the max's find the min
            :return: The nodes id, min-maximum distance
        """
        mini = float('inf')
        ans = 0
        for n in self.graph.node_dic.values():
            maxi = float('-inf')
            if not n.dijkstra_flag:
                self.dijkstra_center(n.id)
            for n1 in self.graph.node_dic:
                if n.D[n1] > maxi and n.D[n1] != float('inf'):
                    maxi = n.D[n1]
            if mini > maxi:
                mini = maxi
                ans = n.id

        return ans, mini

    def dijkstra(self, src):
        """ the dijksra algo will return list with all the distance between src and all other nodes, and the path to
        get to them https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        :param src
        """
        visited = []
        self.path[src][src] = [src]
        D = {v: float('inf') for v in range(self.graph.v_size())}
        D[src] = 0
        Q = PriorityQueue()
        Q.put((0, src))
        while not Q.empty():
            (dist, current) = Q.get()
            visited.append(current)

            for i in range(len(self.graph.node_dic)):
                if (current, i) in self.graph.edge_dic:
                    distance = self.graph.edge_dic[(current, i)]
                    if i not in visited:
                        old = D[i]
                        new = D[current] + distance
                        if new < old:
                            Q.put((new, i))
                            D[i] = new
                            if src != i and src != current and i != current:
                                try:
                                    if len(self.path[src][i]) > 0:
                                        self.path[src][i].clear()

                                except KeyError:
                                    pass
                                try:
                                    for j in self.path[src][current]:
                                        self.path[src][i].append(j)

                                    for j in self.path[current][i]:
                                        self.path[src][i].append(j)
                                except KeyError:
                                    pass
        '''for i in range(len(self.path)):
            for j in range(len(self.path)):
                if self.path[i][j]:
                    self.path[i][j][:0] = [src]'''

        self.graph.get_node(src).dijkstra_flag = True
        self.graph.get_node(src).D = D
        return

    def relax(self, D, Q, current, i):
        new = D[current] + self.graph.edge_dic[(current, i)]
        if new < D[i]:
            Q.put((new, i))
            D[i] = new

    def dijkstra_center(self, src):
        visited = []
        D = {v: float('inf') for v in range(self.graph.v_size())}
        D[src] = 0
        Q = PriorityQueue()
        Q.put((0, src))
        while not Q.empty():
            (dist, current) = Q.get()
            visited.append(current)
            for i in self.graph.all_out_edges_of_node(current):
                self.relax(D, Q, current, i)
        self.graph.get_node(src).D = D
        return
