from src.GraphInterface import GraphInterface
from src.Node import Node


class DiGraph(GraphInterface):
    def __init__(self, v_size: int = 0, mc=0, e_size: int = 0):
        self._v_size = v_size
        self._mc = mc
        self._e_size = e_size
        self.node_dic = {}
        self.edge_dic = {}

    def get_mc(self) -> int:
        ''' return the count for every change in the graph'''
        return self._mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        ''' add edge for the graph between point a to point b, return true if succeed'''
        try:
            self.edge_dic[(id1, id2)] = weight
            self.get_node(id1).add_edge_out(id2, weight)
            self.get_node(id2).add_edge_in(id1, weight)
            self._e_size += 1
            self._mc += 1
            return True
        except:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        '''
        add node to graph
        :param node_id:
        :param pos:
        :return: true if succeed
        '''
        try:
            temp = Node(node_id, pos)
            self.node_dic[node_id] = temp
            self._v_size += 1
            self._mc += 1
            return True
        except:
            return False

    def remove_node(self, node_id: int) -> bool:
        '''
        remove node from the graph, and all the edges connected from and to this node
        :param node_id:
        :return: true if succeed
        '''
        self._e_size -= len(self.all_in_edges_of_node(node_id))
        for edge in self.all_in_edges_of_node(node_id):
            self.node_dic[edge.src].remove_edge(edge)
        self._e_size -= len(self.all_out_edges_of_node(node_id))
        for edge in self.all_out_edges_of_node(node_id):
            self.node_dic[edge.dest].remove_edge(edge)
        try:
            del self.node_dic[node_id]
            self._v_size -= 1
            self._mc += 1
            return True
        except KeyError:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        remove edge from the graph
        :param node_id1:
        :param node_id2:
        :return: true if succeed
        """
        self.get_node(node_id1).remove_edge_out(node_id2)
        self.get_node(node_id2).remove_edge_in(node_id1)
        try:
            del self.edge_dic[(node_id1, node_id2)]
            self._e_size -= 1
            self._mc += 1
            return True
        except KeyError:
            return False

    def e_size(self) -> int:
        """
        :return: the number of edges
        """
        return self._e_size

    def v_size(self) -> int:
        """
        :return: the number of nodes
        """
        return self._v_size

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        :param id1:
        :return: all the edges that there dest is node: id1
        """
        return self.node_dic[id1].edge_in

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        :param id1:
        :return:  all the edges that there src is node: id1
        """
        return self.node_dic[id1].edge_out

    def get_all_v(self) -> dict:
        """
        :return: a dict for all the nodes
        """
        return self.node_dic

    def get_node(self, node_id) -> Node:
        """
        :param node_id:
        :return: return node -key = node_id
        """
        try:
            return self.node_dic[node_id]
        except KeyError:
            return

    def get_node_dict(self):
        return self.node_dic
    def __str__(self):
        return "|V|=" + str(self.v_size()) + " |E|=" + str(self.e_size())
