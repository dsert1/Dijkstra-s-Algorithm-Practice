 #!/usr/bin/env python

from graph import Node, DirectedRoad, RoadMap
from ps2 import load_map, get_neighbors, get_best_path, best_path_ideal_traffic, best_path_to_neighbor_restricted, best_path_restricted
import unittest

unittest.TestLoader.sortTestMethodsUsing = None


class InternalPs2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = RoadMap()
        cls.na = Node('NA')
        cls.nb = Node('NB')
        cls.nc = Node('NC')

        # for best path tests
        cls.n0 = Node('N0')
        cls.n1 = Node('N1')
        cls.n2 = Node('N2')
        cls.n3 = Node('N3')
        cls.n4 = Node('N4')
        cls.n5 = Node('N5')
        cls.n6 = Node('N6')
        cls.n7 = Node('N7')
        cls.n8 = Node('N8')
        cls.n9 = Node('N9')
        cls.n10 = Node('N10')

        cls.m.add_node(cls.na)
        cls.m.add_node(cls.nb)
        cls.m.add_node(cls.nc)
        cls.r1 = DirectedRoad(cls.na, cls.nb, 5, 'local')
        cls.r2 = DirectedRoad(cls.na, cls.nc, 10, 'arterial')
        cls.r3 = DirectedRoad(cls.nb, cls.nc, 18, 'interstate')
        cls.m.add_road(cls.r1)
        cls.m.add_road(cls.r2)
        cls.m.add_road(cls.r3)
        cls.road_map = load_map("maps/road_map.txt")

    # ------------------------------------------------ testing graph.py

    def test_1_graph1_weighted_edge_src(self):
        self.assertEqual(str(self.r1.get_source()), str(self.na))
        self.assertEqual(str(self.r2.get_source()), str(self.na))
        self.assertEqual(str(self.r3.get_source()), str(self.nb))

    def test_2_graph2_weighted_edge_dest(self):
        self.assertEqual(str(self.r1.get_destination()), str(self.nb))
        self.assertEqual(str(self.r2.get_destination()), str(self.nc))
        self.assertEqual(str(self.r3.get_destination()), str(self.nc))

    def test_3_graph3_weighted_edge_str(self):
        self.assertEqual(str(self.r1), "NA -> NB takes 5 hours via local road")
        self.assertEqual(str(self.r2), "NA -> NC takes 10 hours via arterial road")
        self.assertEqual(str(self.r3), "NB -> NC takes 18 hours via interstate road")

    def test_4_graph4_weighted_edge_total_time(self):
        self.assertEqual(self.r1.get_total_time(), 5)
        self.assertEqual(self.r2.get_total_time(), 10)
        self.assertEqual(self.r3.get_total_time(), 18)

    def test_5_graph5_add_edge_to_nonexistent_node_raises(self):
        node_not_in_graph = Node('SC')
        no_src = DirectedRoad(self.nb, node_not_in_graph, 9, 'bridge')
        no_dest = DirectedRoad(node_not_in_graph, self.na, 9, 'bridge')

        with self.assertRaises(ValueError):
            self.m.add_road(no_src)
        with self.assertRaises(ValueError):
            self.m.add_road(no_dest)

    def test_6_graph6_add_existing_node_raises(self):
        with self.assertRaises(ValueError):
            self.m.add_node(self.na)

    def test_7_graph7_str(self):
        lines = ["NA -> NB takes 5 hours via local road", 
                 "NA -> NC takes 10 hours via arterial road",
                 "NB -> NC takes 18 hours via interstate road"]
        actual = str(self.m).split("\n")
        self.assertIn(
            lines[0], actual, "Your printed graph does not match the correct string")
        self.assertIn(
            lines[1], actual, "Your printed graph does not match the correct string")
        self.assertIn(
            lines[2], actual, "Your printed graph does not match the correct string")

    # ------------------------------------------------ testing ps2.py

    def test_8_ps2_load_map(self):
        self.assertTrue(isinstance(self.road_map, RoadMap))
        self.assertEqual(len(self.road_map.nodes), 10)
        all_roads = []
        for _, roads in self.road_map.roads.items():
            all_roads += roads  # edges must be dict of node -> list of edges
            for road in roads:
                self.assertFalse('\n' in road.get_type(),
                                 "Your road type contains a new line character. Check the reading/parsing in load_map")
        all_roads = set(all_roads)
        self.assertEqual(len(all_roads), 26)

    def _print_path_description(self, start, end, restricted_roads):
        constraint = ""
        if restricted_roads != []:
            constraint += " and without using the {} line(s)".format(
                restricted_roads)
        print("------------------------")
        print("Shortest path from Node {} to {} {}".format(
            start, end, constraint))

    def _test_path(self, graph, expectedPath, expectedTime, message="", restricted_roads=[]):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, restricted_roads)
        student_path = get_best_path(graph, start, end, restricted_roads)
        print("(Expected Path, Expected Time): ", (expectedPath, expectedTime))
        print("(Your Path, Your Time): ", student_path)
        self.assertEqual(student_path[0], expectedPath, message)
        self.assertEqual(student_path[1], expectedTime,
                         "Time incorrect: " + message)

    def _test_impossible_path(self, graph,
                              start,
                              end,
                              restricted_roads=[], message=""):

        self._print_path_description(start, end, restricted_roads)
        student_path = get_best_path(graph, start, end, restricted_roads)
        self.assertEqual(student_path, None, message)

    def test_9_ps2_map1_path_one_step(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n1], expectedTime=15,
                        message="The path goes one step. Make sure you are looking at all of the neighboring nodes.")

    def test_10_ps2_map2_path_limited_time(self):
        self._test_path(self.road_map,
                        expectedPath=[self.n0, self.n2, self.n4, self.n5], expectedTime=18, message="Make sure your algorithm is finding the shortest path.")

    def test_11_ps2_map3_path_restricted_path(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n2, self.n3], expectedTime=25, restricted_roads=[
                        'interstate'], message="The path tests having a restricted list of road types. Make sure your algorithm is finding the shortest correct path.")

    def test_12_ps2_map_path_start_end_same(self):
        student_path = get_best_path(self.road_map, self.n1, self.n1, [])
        self.assertEqual(student_path[0], [
        ], "If the start and end are the same, the path should be an empty path")
        self.assertEqual(
            student_path[1], 0, "If the start and end are the same, the time traveled should be zero")

    def test_13_ps2_map_path_same_length_different_time(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n1, self.n3], expectedTime=21,
                        message="Should find path that has the shortest length of all edges combined")

    def test_14_ps2_path_multiple_roads_not_allowed(self):
        self._test_path(self.road_map, expectedPath=[self.n0, self.n1, self.n3, self.n8, self.n9], expectedTime=46, restricted_roads=[
                        'arterial', 'local'], message="Make sure your search works with multiple restricted roads")

    def test_15_impossible_path_no_interstate(self):
        self._test_impossible_path(self.road_map, start=self.n0, end=self.n10, restricted_roads=[
                                   'interstate'], message="Should be impossible")

    def test_16_impossible_path_no_interstate_no_local(self):
        self._test_impossible_path(self.road_map, start=self.n1, end=self.n9, restricted_roads=[
                                   'interstate', 'local'], message="Should be impossible")
    def test_17_get_neighbors_1(self):
        found_neighbors = get_neighbors(self.road_map, self.n3, [])
        expected_neighbors = [self.n1, self.n2, self.n6, self.n8]
        self.assertEqual(found_neighbors, expected_neighbors)
        
        found_neighbors = get_neighbors(self.road_map, self.n8, [])
        expected_neighbors = [self.n3, self.n6, self.n7, self.n9]
        self.assertEqual(found_neighbors, expected_neighbors)
        
        
    def test_18_get_neighbors_2(self):
        # get neighbors with restrictions
        found_neighbors = get_neighbors(self.road_map, self.n3, ['local'])
        expected_neighbors = [self.n1, self.n2, self.n8]
        self.assertEqual(found_neighbors, expected_neighbors)  
        
        found_neighbors = get_neighbors(self.road_map, self.n3, ['interstate'])
        expected_neighbors = [self.n2, self.n6]
        self.assertEqual(found_neighbors, expected_neighbors)
        
        found_neighbors = get_neighbors(self.road_map, self.n8, ['interstate', 'bridge'])
        expected_neighbors = [self.n6]
        self.assertEqual(found_neighbors, expected_neighbors)

if __name__ == "__main__":
    # unittest.main(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(InternalPs2Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
