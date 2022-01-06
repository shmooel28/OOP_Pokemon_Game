import unittest

from src.GraphAlgo import GraphAlgo
from src.Pokemon import Pokemon


class MyTestCase(unittest.TestCase):
    def test_start_end_pos(self):
        pok_dic = {'Pokemon': {'value': 5.0, 'type': -1, 'pos': '35.197656770719604,32.10191878639921,0.0'}}
        pok = Pokemon(pok_dic)
        graph = GraphAlgo()
        graph.load_from_json("A0.json")
        pok.start_end_pos(graph)
        self.assertEqual(pok.src, 9)  # add assertion here

    def test_distance(self):
        pok_dic = {'Pokemon': {'value': 5.0, 'type': -1, 'pos': '35,32,0.0'}}
        pok = Pokemon(pok_dic)
        dis = pok.distanc((0, 0))
        self.assertEqual(dis, 47.423622805517505085772961419857)

    def test_is_on_edge(self):
        pok_dic = {'Pokemon': {'value': 5.0, 'type': -1, 'pos': '35.197656770719604,32.10191878639921,0.0'}}
        pok = Pokemon(pok_dic)
        graph = GraphAlgo()
        graph.load_from_json("A0.json")
        edge = (9, 8)
        print(edge)
        flag = pok.is_on_edge(edge, graph)
        self.assertEqual(flag, True)


if __name__ == '__main__':
    unittest.main()
