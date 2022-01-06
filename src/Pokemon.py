import math

from src.GraphAlgo import GraphAlgo


class Pokemon:
    def __init__(self, pok_dic):
        self.value = pok_dic["Pokemon"]["value"]
        self.type = pok_dic["Pokemon"]["type"]
        x, y, z = pok_dic["Pokemon"]["pos"].split(',')
        self.pos = (float(x), float(y), float(z))
        self.src = -1
        self.dest = -1
        self.agent = -1

    def start_end_pos(self, graph: GraphAlgo):
        """
        update the src and the dest of the pokemon
        the src and the dest represent the edge that the pokemon sit on.
        the src and the dest dependent on the type of the pokemon, if the type is negetive the src is
        the max id beteewn the src and dest
        :param graph:
        :return:
        """
        for edge in graph.graph.edge_dic:
            if self.is_on_edge(edge, graph):
                if self.type > 0:
                    self.src = min(edge[0], edge[1])
                    self.dest = max(edge[1], edge[0])
                else:
                    self.src = max(edge[1], edge[0])
                    self.dest = min(edge[0], edge[1])
                return

    def is_on_edge(self, edge, graph: GraphAlgo) -> bool:
        """
        cheak if the pokemon sit on edge.
        the formula is check the distance beteewn the pokemon and the dest and src,
        if that distance less the distance between the src and the dest smaller than epsilon return True
        :param edge:
        :param graph:
        :return: boolean
        """
        loc1 = graph.graph.get_node(edge[0]).pos
        loc2 = graph.graph.get_node(edge[1]).pos
        dis_from_src = self.distanc(loc1)
        dis_from_dest = self.distanc(loc2)
        dis_node = math.sqrt(math.pow(loc1[0] - loc2[0], 2) + math.pow(loc1[1] - loc2[1], 2))
        if abs(dis_node - (dis_from_dest + dis_from_src)) < 0.00001:
            return True
        else:
            return False

    def distanc(self, pos):
        """
        Formula to calculation distance beteen node and pokemon
        :param pos: location of node
        :return: float
        """
        return math.sqrt(math.pow(self.pos[0] - pos[0], 2) + math.pow(self.pos[1] - pos[1], 2))
