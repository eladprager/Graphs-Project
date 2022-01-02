from unittest import TestCase
from threading import Semaphore
from main import Graph, Node, add_edge, validate_lists

print_semaphore = Semaphore(1)


class TestClass(TestCase):

    def test_empty_graph(self):
        g = Graph()
        self.assertTrue(g.is_dag())

        actual_result = g.topo_sort()
        expected_result = []
        self.assertListEqual(expected_result, actual_result)
        validate_lists(expected_result, actual_result, 'error:')

        actual_result = g.level()
        expected_result = 0
        self.assertEqual(expected_result, actual_result)

        print_semaphore.acquire()
        print(f'################## EMPTY GRAPH ##################\n{g}')
        print_semaphore.release()

    def test_one_node(self):
        g = Graph()
        g.add_node(Node('x'))
        self.assertTrue(g.is_dag())

        actual_result = g.topo_sort()
        expected_result = [Node('x')]
        self.assertListEqual(expected_result, actual_result)
        validate_lists(expected_result, actual_result, 'error:')

        actual_result = g.level(Node('x'))
        expected_result = 0
        self.assertEqual(expected_result, actual_result)

        print_semaphore.acquire()
        print(f'################## ONE NODE ##################\n{g}')
        print_semaphore.release()

    def test_two_nodes_no_edges(self):
        g = Graph()
        g.add_node(Node('x'))
        g.add_node(Node('a'))
        self.assertTrue(g.is_dag())

        actual_result = g.topo_sort()
        expected_result = [Node('a'), Node('x')]
        self.assertListEqual(expected_result, actual_result)
        validate_lists(expected_result, actual_result, 'error:')

        actual_result = {}
        for node in g.get_nodes():
            actual_result[node] = g.level(node)
        expected_result = {Node('a'): 0, Node('x'): 0}
        self.assertDictEqual(expected_result, actual_result)

        print_semaphore.acquire()
        print(f'################## TWO NODES NO EDGES ##################\n{g}')
        print_semaphore.release()

    def test_two_separate_components_cycle(self):
        g = Graph()
        add_edge(g, 'x', 'a')
        add_edge(g, 'a', 'x')

        add_edge(g, 'y', 'b')
        add_edge(g, 'b', 'y')

        self.assertFalse(g.is_dag())

        with self.assertRaises(Exception):
            g.topo_sort()

        with self.assertRaises(Exception):
            for node in g.get_nodes():
                g.level(node)

        print_semaphore.acquire()
        print(f'################## TWO SEPARATE COMPONENTS CYCLE ##################\n'
              f'no support for cyclic graphs\n')
        print_semaphore.release()

    def test_two_separate_components_dag(self):
        g = Graph()
        add_edge(g, 'x', 'a')
        add_edge(g, 'a', 'b')

        add_edge(g, 'y', 'c')
        add_edge(g, 'c', 'd')

        self.assertTrue(g.is_dag())

        actual_result = g.topo_sort()
        expected_result = [Node('y'), Node('c'), Node('d'), Node('x'), Node('a'), Node('b')]
        self.assertListEqual(expected_result, actual_result)
        validate_lists(expected_result, actual_result, 'error:')

        actual_result = {}
        for node in g.get_nodes():
            actual_result[node] = g.level(node)
        expected_result = {Node('x'): 0, Node('a'): 1, Node('b'): 2, Node('y'): 0, Node('c'): 1, Node('d'): 2}
        self.assertDictEqual(expected_result, actual_result)

        print_semaphore.acquire()
        print(f'################## TWO SEPARATE COMPONENTS DAG ##################\n{g}')
        print_semaphore.release()

    def test_two_sources_one_sink(self):
        g = Graph()
        add_edge(g, 'x', 'a')
        add_edge(g, 'y', 'a')

        add_edge(g, 'a', 'b')
        add_edge(g, 'b', 'c')

        self.assertTrue(g.is_dag())

        actual_result = g.topo_sort()
        expected_result = [Node('y'), Node('x'), Node('a'), Node('b'), Node('c')]
        self.assertListEqual(expected_result, actual_result)
        validate_lists(expected_result, actual_result, 'error:')

        actual_result = {}
        for node in g.get_nodes():
            actual_result[node] = g.level(node)
        expected_result = {Node('x'): 0, Node('y'): 0, Node('a'): 1, Node('b'): 2, Node('c'): 3}
        self.assertDictEqual(expected_result, actual_result)

        print_semaphore.acquire()
        print(f'################## TWO SOURCES ONE SINK ##################\n{g}')
        print_semaphore.release()

    def test_small_graph_cycle(self):
        g = Graph()
        add_edge(g, 'x', 'a')
        add_edge(g, 'a', 'x')
        self.assertFalse(g.is_dag())

        with self.assertRaises(Exception):
            g.topo_sort()

        with self.assertRaises(Exception):
            for node in g.get_nodes():
                g.level(node)

        print_semaphore.acquire()
        print(f'################## SMALL GRAPH CYCLE ##################\n'
              f'no support for cyclic graphs\n')
        print_semaphore.release()

    def test_medium_graph_cycle(self):
        g = Graph()
        add_edge(g, 'x', 'a')
        add_edge(g, 'a', 'b')
        add_edge(g, 'b', 'c')
        add_edge(g, 'c', 'a')
        add_edge(g, 'c', 'y')
        add_edge(g, 'y', 'z')
        add_edge(g, 'y', 'c')
        self.assertFalse(g.is_dag())

        with self.assertRaises(Exception):
            g.topo_sort()

        with self.assertRaises(Exception):
            for node in g.get_nodes():
                g.level(node)

        print_semaphore.acquire()
        print(f'################## MEDIUM GRAPH CYCLE ##################\n'
              f'no support for cyclic graphs\n')
        print_semaphore.release()

    def test_large_graph_cycle(self):
        g = Graph()
        add_edge(g, 'x', 'a')
        add_edge(g, 'x', 'b')
        add_edge(g, 'y', 'b')
        add_edge(g, 'y', 'c')
        add_edge(g, 'y', 'd')
        add_edge(g, 'a', 'h')
        add_edge(g, 'b', 'h')
        add_edge(g, 'b', 'f')
        add_edge(g, 'c', 'e')
        add_edge(g, 'd', 'f')
        add_edge(g, 'e', 'f')
        add_edge(g, 'f', 'g')
        add_edge(g, 'g', 'j')
        add_edge(g, 'h', 'i')
        add_edge(g, 'h', 'j')
        add_edge(g, 'i', 'k')
        add_edge(g, 'j', 'k')

        add_edge(g, 'j', 'a')
        self.assertFalse(g.is_dag())

        with self.assertRaises(Exception):
            g.topo_sort()

        with self.assertRaises(Exception):
            for node in g.get_nodes():
                g.level(node)

        print_semaphore.acquire()
        print(f'################## LARGE GRAPH CYCLE ##################\n'
              f'no support for cyclic graphs\n')
        print_semaphore.release()

    def test_small_graph_dag(self):
        g = Graph()
        add_edge(g, 'x', 'a')
        add_edge(g, 'a', 'b')
        self.assertTrue(g.is_dag())

        actual_result = g.topo_sort()
        expected_result = [Node('x'), Node('a'), Node('b')]
        self.assertListEqual(expected_result, actual_result)
        validate_lists(expected_result, actual_result, 'error:')

        actual_result = {}
        for node in g.get_nodes():
            actual_result[node] = g.level(node)
        expected_result = {Node('x'): 0, Node('a'): 1, Node('b'): 2}
        self.assertDictEqual(expected_result, actual_result)

        print_semaphore.acquire()
        print(f'################## SMALL GRAPH DAG ##################\n{g}')
        print_semaphore.release()

    def test_medium_graph_dag(self):
        g = Graph()
        add_edge(g, 'a', 'x')
        add_edge(g, 'a', 'b')
        add_edge(g, 'b', 'c')
        add_edge(g, 'c', 'd')
        self.assertTrue(g.is_dag())

        actual_result = g.topo_sort()
        expected_result = [Node('a'), Node('b'), Node('c'), Node('d'), Node('x')]
        self.assertListEqual(expected_result, actual_result)
        validate_lists(expected_result, actual_result, 'error:')

        actual_result = {}
        for node in g.get_nodes():
            actual_result[node] = g.level(node)
        expected_result = {Node('a'): 0, Node('x'): 1, Node('b'): 1, Node('c'): 2, Node('d'): 3}
        self.assertDictEqual(expected_result, actual_result)

        print_semaphore.acquire()
        print(f'################## MEDIUM GRAPH DAG ##################\n{g}')
        print_semaphore.release()

    def test_large_graph_dag(self):
        g = Graph()
        add_edge(g, 'x', 'a')
        add_edge(g, 'x', 'b')
        add_edge(g, 'y', 'b')
        add_edge(g, 'y', 'c')
        add_edge(g, 'y', 'd')
        add_edge(g, 'a', 'h')
        add_edge(g, 'b', 'h')
        add_edge(g, 'b', 'f')
        add_edge(g, 'c', 'e')
        add_edge(g, 'd', 'f')
        add_edge(g, 'e', 'f')
        add_edge(g, 'f', 'g')
        add_edge(g, 'g', 'j')
        add_edge(g, 'h', 'i')
        add_edge(g, 'h', 'j')
        add_edge(g, 'i', 'k')
        add_edge(g, 'j', 'k')
        self.assertTrue(g.is_dag())

        actual_result = g.topo_sort()
        expected_result = [Node('y'), Node('d'), Node('c'), Node('e'), Node('x'), Node('b'), Node('f'), Node('g'),
                           Node('a'), Node('h'), Node('j'), Node('i'), Node('k')]
        self.assertListEqual(expected_result, actual_result)
        validate_lists(expected_result, actual_result, 'error:')

        actual_result = {}
        for node in g.get_nodes():
            actual_result[node] = g.level(node)
        expected_result = {Node('x'): 0, Node('y'): 0, Node('a'): 1, Node('b'): 1, Node('c'): 1, Node('d'): 1,
                           Node('e'): 2, Node('f'): 3, Node('g'): 4, Node('h'): 2, Node('i'): 3, Node('j'): 5,
                           Node('k'): 6}
        self.assertDictEqual(expected_result, actual_result)

        print_semaphore.acquire()
        print(f'################## LARGE GRAPH DAG ##################\n{g}')
        print_semaphore.release()
