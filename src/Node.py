class Node:
    def __init__(self, id: int, pos: tuple = None):
        self.id = id
        self.pos = pos
        self.edge_in = {}
        self.edge_out = {}
        self.dijkstra_flag = False
        self.D = []
        self.D_Max = None

    def add_edge_in(self, src, w):
        self.edge_in[src] = w

    def add_edge_out(self, dest, w):
        self.edge_out[dest] = w

    def remove_edge_in(self, src):
        try:
            del self.edge_in[src]
        except KeyError:
            pass

    def remove_edge_out(self, dest):
        try:
            del self.edge_out[dest]
        except KeyError:
            pass

    def __str__(self):
        return "ID =" + str(self.id) + "|edges out| " + str(len(self.edge_out)) + " |edges in| " + str(
            len(self.edge_in))

    def __repr__(self):
        return "ID =" + str(self.id) + "|edges out| " + str(len(self.edge_out)) + " |edges in| " + str(
            len(self.edge_in))
