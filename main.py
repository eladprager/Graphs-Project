from dataclasses import dataclass
from typing import List, Set, Any
import textwrap

# our Graph is a dag
# a->b; b->c; a->c


@dataclass(frozen=True, eq=True)
class Node:
    value: Any

    def __repr__(self):
        return str(f'{self.value}')


@dataclass(frozen=True, eq=True)
class Edge:
    src: Node
    dst: Node

    def __repr__(self):
        return str(f'{self.src}->{self.dst}')


class Graph:
    def __init__(self):
        self.nodes = []
        self.edges = []

    # node may be added once!
    def add_node(self, node) -> Node:
        if node in self.nodes:
            raise Exception(f'Node already exist in graph: {node}')
        else:
            return self.add_node_if_missing(node)

    # you may have two edges that are identical
    def add_edge(self, edge) -> Edge:
        self.edges.append(edge)
        return edge

    def add_node_if_missing(self, node) -> Node:
        if node not in self.nodes:
            self.nodes.append(node)
        return node

    def add_edge_from_nodes(self, src, dst) -> Edge:
        edge = Edge(self.add_node_if_missing(src), self.add_node_if_missing(dst))
        return self.add_edge(edge)

    def get_nodes(self) -> List[Node]:
        return self.nodes

    def get_edges(self) -> List[Edge]:
        return self.edges

    def in_edges(self, node) -> List[Edge]:
        return [edge for edge in self.edges if edge.dst == node]

    def parents(self, node) -> List[Node]:
        return [edge.src for edge in self.edges if edge.dst == node]

    def out_edges(self, node) -> List[Edge]:
        return [edge for edge in self.edges if edge.src == node]

    def children(self, node) -> List[Node]:
        return [edge.dst for edge in self.edges if edge.src == node]

    def in_degree(self, node) -> int:
        return len(self.in_edges(node))

    def out_degree(self, node) -> int:
        return len(self.out_edges(node))

    def get_sources(self) -> List[Node]:
        return [node for node in self.nodes if self.in_degree(node) == 0]

    def get_sinks(self) -> List[Node]:
        return [node for node in self.nodes if self.out_degree(node) == 0]

    @staticmethod
    def flatten(t) -> Set:
        return set([item for sublist in t for item in sublist])

    def all_children(self, ns) -> Set:
        return {*Graph.flatten([self.children(n) for n in ns])}

    # tell if this graph contains a loop
    # dag = Directed Acyclic Graph
    def is_dag(self) -> bool:
        nodes = self.get_nodes()
        status = {u: "unvisited" for u in nodes}
        found_cycle = False

        for node in nodes:
            if status[node] == "unvisited":
                found_cycle = self._dag_dfs(node, status)
                if found_cycle:
                    break

        result = not found_cycle
        return result

    # visit nodes with the dfs algorithm, if a node is visited more than once, we have a cycle
    def _dag_dfs(self, node: Node, status: dict) -> bool:
        result = False
        status[node] = "visiting"

        for neighbor in self.children(node):
            if status[neighbor] == "visiting":
                result = True
                break

            if status[neighbor] == "unvisited":
                result = self._dag_dfs(neighbor, status)
                if result:
                    break

        status[node] = "visited"
        return result

    # deterministic solution - doesn't change over time
    # c->d, b->c, a->b, a->x
    # topo: a->b->c->d->x OK
    # topo: a->x->b->c->d OK
    # topo: a->b->x->c->d OK
    # topo: x->a->b->c->d BAD
    def topo_sort(self) -> List[Node]:
        if self.is_dag():
            nodes = self.get_nodes()
            status = {u: "unvisited" for u in nodes}
            result = []

            for node in nodes:
                if status[node] == 'unvisited':
                    self._topo_dfs(node, status, result)
            return result
        else:
            raise Exception("no support for cyclic graphs")

    # visit nodes with the dfs algorithm, insert nodes to result by postorder
    def _topo_dfs(self, node: Node, status: dict, result: list) -> None:
        status[node] = 'visited'

        for neighbor in self.children(node):
            if status[neighbor] == 'unvisited':
                self._topo_dfs(neighbor, status, result)

        result.insert(0, node)

    # integer level of node
    # deterministic solution - doesn't change over time
    # if a->b level(a) < level(b)
    # if exist a path from a to b level(a) < level(b)
    # if a->b, a->c level(b) XX level(c) - can be > OR < or ==, depends on the rest of the connectivity
    def level(self, node=None) -> int:
        result = 0
        if self.is_dag():
            # get the maximal longest path between all sources to the given node
            for source in self.get_sources():
                distance = self._bellman_ford(source)
                if abs(distance[node]) > result and distance[node] != float("Inf"):
                    result = abs(distance[node])
            return result
        else:
            raise Exception("no support for cyclic graphs (NP)")

    # finding the longest path from source to the given node using the bellman-Ford algorithm
    def _bellman_ford(self, source: Node) -> dict:
        nodes = self.get_nodes()
        distance = {}

        for node in nodes:
            distance[node] = float("Inf")
        distance[source] = 0

        for _ in range(len(nodes) - 1):
            for node in nodes:
                for neighbour in self.children(node):
                    if distance[neighbour] > distance[node] - 1:
                        distance[neighbour] = distance[node] - 1

        return distance

    def __str__(self):
        res = textwrap.dedent(f'''
        nodes     {self.get_nodes()}
        edges     {self.get_edges()}
        sources   {self.get_sources()}
        sinks     {self.get_sinks()}
        is_dag    {self.is_dag()}
        topo_sort {self.topo_sort()}
        ''')
        # for n in g.get_nodes():
        for n in self.get_nodes():
            res += textwrap.dedent(f'''
            in_edges  '{n}': {self.in_edges(n)}
            out_edges '{n}': {self.out_edges(n)}
            parents   '{n}': {self.parents(n)}
            children  '{n}': {self.children(n)}
            ''')
        return str(res)


def add_edge(g, a, b):
    return g.add_edge_from_nodes(Node(a), Node(b))


# validates that the lists lo and l1 are of the same length and contain the same values
def validate_lists(l0, l1, msg):
    if len(l0) != len(l1):
        print(f'{msg} lists length not equal: {l0}, {l1}')
    elif l0 != l1:
        print(f'{msg} lists not equal: {l0}, {l1}')
    else:
        pass


def test_out_in_edges():
    g = Graph()
    x_a = add_edge(g, 'x', 'a')
    a_b = add_edge(g, 'a', 'b')
    validate_lists(g.out_edges(Node('x')), [x_a], "out_edges")
    validate_lists(g.out_edges(Node('a')), [a_b], "out_edges")
    validate_lists(g.in_edges(Node('x')), [], "in_edges")


if __name__ == '__main__':
    g = Graph()
    x_a = add_edge(g, 'x', 'a')
    a_b = add_edge(g, 'a', 'b')
    add_edge(g, 'b', 'c')
    add_edge(g, 'c', 'a')
    add_edge(g, 'c', 'y')
    add_edge(g, 'y', 'z')
    add_edge(g, 'y', 'c')
    print(g)

# how to write successful code - for this exercise?
# A
# 1. testing, testing, testing!
# 2. style, readable names - use proposed naming convention, write short elegant functions wherever possible
# 7. efficiency (but not over readability) can we use a dict, can we lazy initialize something?
