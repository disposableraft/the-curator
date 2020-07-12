import inspect
import unittest
from collections import deque

class Node:
    def __init__(self, id):
        self.id = id
        self.degrees = 0
        self.edges = set()
        self.type = self.__class__.__name__

    def __str__(self):
        return str({
            'id': self.id,
            'degrees': self.degrees,
            'edges': self.edges,
            'type': self.type
        })

    def __iter__(self):
        return iter([x for x in self.edges])

    def increment_degree(self):
        self.degrees += 1

    def add_edge(self, edge):
        # This should be called by graph, so the dictionary can be managed.
        class_name = inspect.stack()[1][0].f_locals['self'].__class__.__name__
        assert class_name == 'Graph'
        self.edges.add(edge)
        self.increment_degree()


class Graph:
    """
    A directed graph
    """
    def __init__(self, nodes=[]):
        self.nodes = dict()
        self.add_nodes(nodes)

    def __iter__(self):
        """
        Returns the nodes in the graph, but not node.edges
        """
        return iter([self.nodes[key] for key in self.nodes])

    def __getitem__(self, key):
        return self.nodes[key]

    def get_nodes(self):
        """
        Returns a dict of nodes grouped by class name.
        """
        groups = dict()
        for key, node in self.nodes.items():
            group = groups.setdefault(node.type, dict())
            group[key] = node
        return groups

    def add(self, node):
        assert isinstance(node, Node)
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            if node.id == 'helenfrankenthal':
                print('adding helen')
        return self.nodes[node.id]

    def add_nodes(self, nodes):
        for v in nodes:
            self.add(v)

    def edges(self, id):
        node = self.nodes[id]
        return [k for k in node]

    def add_edges(self, node, edges=[]):
        for x in edges:
            self.add_edge(node.id, x)

    def add_edge(self, key, node):
        self.nodes[key].add_edge(node.id)
        node.increment_degree()
        return self.nodes[key].edges

    def bfs(self):
        """
        Returns an array of all the graph's nodes and edges.
        """
        # enqueue the nodes
        q = deque(self.nodes)
        visited = list()
        while len(q) > 0:
            key = q.popleft()
            if key not in visited:
                visited.append(key)
                if len(self.nodes[key].edges) > 0:
                    for m in self.nodes[key].edges:
                        if m not in q:
                            q.appendleft(m)
        return visited

    def count_nodes(self):
        return len(self.bfs())

    def count_edges(self):
        count = 0
        for node in self:
            count += node.degrees
        return count

    def density(self):
        m = self.count_edges()
        n = self.count_nodes()
        density = (m * 2) / (n * (n - 1))
        return density


class TestGraph(unittest.TestCase):
    def test_init(self):
        node = Node(23)
        g = Graph([node])
        self.assertEqual(g.nodes, {node.id: node})

    def test_iter(self):
        nodes = [Node(0), Node(1), Node(2)]
        G = Graph(nodes)
        iterated = list(G)
        self.assertListEqual(nodes, iterated)

    def test_get_item(self):
        n0 = Node('xyz')
        g = Graph([n0])
        self.assertEqual(g['xyz'], n0)

    def test_get_nodes(self):
        class A(Node):
            pass
        class B(Node):
            pass
        a = A('a')
        b = B('b')
        b1 = B('b1')
        g = Graph([a, b, b1])
        expected = {
            'A': {'a': a},
            'B': {'b': b, 'b1': b1}
        }
        self.assertDictEqual(g.get_nodes(), expected)

    def test_bfs(self):
        n1 = Node(1)
        n3 = Node(3)
        n6 = Node(6)

        G = Graph()
        G.add_nodes([n1,n3,n6])

        G.add_edges(n1, [Node(2), n3])
        G.add_edges(n3, [Node(4), Node(5)])
        G.add_edge(n3.id, n6)
        G.add_edge(n6.id, n1)

        bfs = G.bfs()

        result = [n for n in bfs]
        expected = [1,2,3,4,5,6]

        self.assertListEqual(sorted(result), sorted(expected))

    def test_count_nodes(self):
        G = Graph()
        n1 = Node(1)
        n2 = Node(2)
        G.add_nodes([n1])
        G.add_edges(n1, [n2, Node(3), Node(4)])
        count = G.count_nodes()
        self.assertEqual(count, 4, f'nodes: {[x for x in G]}')

    def test_count_edges(self):
        n1 = Node(1)
        G = Graph([n1])
        G.add_edges(n1, [Node(2), Node(3), Node(4)])
        count = G.count_edges()
        self.assertEqual(count, 3)

    def test_density_for_complete_graph(self):
        G = Graph()
        n1 = Node(1)
        n2 = Node(2)
        n3 = Node(3)
        n4 = Node(4)

        G.add_nodes([n1])

        G.add_edges(n1, [n2,n3,n4])
        G.add_edges(n2, [n3,n4])
        G.add_edges(n3, [n4])

        density = G.density()
        self.assertEqual(density, 1)

    def test_add_edge(self):
        G = Graph([Node(1)])
        G.add_edge(1, Node(2))
        edges = G.add_edge(1, Node(3))
        # Graph adds any new nodes passed as edges
        # Graph adds edges to node
        self.assertEqual(3, len(G.nodes))
        self.assertEqual(2, len(edges))


class TestNode(unittest.TestCase):
    def test_init(self):
        x = Node(1)
        self.assertEqual(x.id, 1)

    def test_cannot_call_add_edge(self):
        # Test that add edge cannot be called from inside Node
        x = Node(1)
        y = Node(2)
        self.assertRaises(AssertionError, x.add_edge, y)

    def test_str(self):
        x = Node(23)
        self.assertEqual('23', str(x))


if __name__ == '__main__':
    unittest.main()