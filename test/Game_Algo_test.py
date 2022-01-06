import unittest

from src.Agent import Agent
from src.Game_Algo import Game_Algo
from src.GraphAlgo import GraphAlgo
from src.Pokemon import Pokemon


class MyTestCase(unittest.TestCase):

    def test_dis(self):
        graph = GraphAlgo()
        print(graph.load_from_json("A0.json"))
        pok_dic = {'Pokemon': {'value': 5.0, 'type': -1, 'pos': '35.197656770719604,32.10191878639921,0.0'}}
        pok = Pokemon(pok_dic)
        pok.start_end_pos(graph)
        egent_dic ={'Agent': {'id': 0, 'value': 0.0, 'src': 9, 'dest': -1, 'speed': 1.0, 'pos': '35.19597880064568,32.10154696638656,0.0'}}
        agent = Agent(egent_dic)
        game = Game_Algo(graph)
        dis = game.dist(pok,agent)
        print(dis)
        self.assertEqual(dis, 0)  # add assertion here


if __name__ == '__main__':
    unittest.main()
