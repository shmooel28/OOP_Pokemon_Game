class Agent:
    # class represent Agent
    def __init__(self, agent_dic):
        self.id = agent_dic["Agent"]["id"]
        self.value = agent_dic["Agent"]["value"]
        self.src = agent_dic["Agent"]["src"]
        self.dest = agent_dic["Agent"]["dest"]
        self.speed = agent_dic["Agent"]["speed"]
        x, y, z = agent_dic["Agent"]["pos"].split(',')
        self.pos = (float(x), float(y), float(z))
        self.path = []
        self.time_to_dest = 0
