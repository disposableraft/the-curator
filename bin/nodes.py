import unittest
from collections import deque

class Node:
    def __init__(self, id):
        self.id = id
        self.edges = set()
    
    def __str__(self):
        return str(self.id)
        
    def __iter__(self):
        return iter([x for x in self.edges])
        
    def add_edge(self, edge):
        assert isinstance(edge, Node)
        self.edges.add(edge)
    
    def add_edges(self, edges):
        for x in edges:
            self.add_edge(x)
        

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
    
    def add(self, node):
        assert isinstance(node, Node)
        self.nodes[node.id] = node

    def add_nodes(self, nodes):
        for v in nodes:
            self.add(v)
    
    def edges(self, id):
        node = self.nodes[id]
        return [k for k in node]
    
    def bfs(self):
        """
        Returns an array of all the graph's nodes and edges.
        """
        # enqueue the nodes
        q = deque(self)
        visited = list()
        while len(q) > 0:
            node = q.popleft()
            if node not in visited:
                visited.append(node)
                # print('node', node)
                if len(node.edges) > 0:
                    for k in node.edges:
                        if k not in q:
                            q.appendleft(k)
        return visited
    

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
    
    def test_bfs(self):
        n1 = Node(1)
        n3 = Node(3)
        n1.add_edges([Node(2), n3])
        n3.add_edges([Node(4), Node(5)])
        n6 = Node(6)
        n3.add_edge(n6)
        n6.add_edge(n1)        
        
        G = Graph([n1, n3, n6])
        bfs = G.bfs()

        result = [n.id for n in bfs]
        expected = [1,2,3,4,5,6]

        self.assertListEqual(sorted(result), sorted(expected))


class TestNode(unittest.TestCase):
    def test_init(self):
        x = Node(1)
        self.assertEqual(x.id, 1)
    
    def test_add_edge(self):
        x = Node(1)
        y = Node(2)

        x.add_edge(y)
        
        self.assertEqual(len(x.edges), 1)
        self.assertEqual(len(y.edges), 0)
    
    def test_iter_edges(self):
        root = Node(0)
        expected = []
        for x in range(1,3):
            edge = Node(x)
            root.add_edge(edge)
            expected.append(edge.id)
        
        result = [x.id for x in root]

        self.assertListEqual(sorted(result), sorted(expected))
    
    def test_str(self):
        x = Node(23)
        self.assertEqual('23', str(x))
        

if __name__ == '__main__':
    unittest.main()