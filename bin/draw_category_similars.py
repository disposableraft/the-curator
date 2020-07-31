import constants
from pygraphviz import AGraph
import utils

class DrawCategorySimilars:
    def __init__(self, graph, category_name, image_path):
        self.graph = graph
        self.category_name = category_name
        self.image_path = image_path

    def get_category(self):
        return self.graph[self.category_name]

    def get_connected(self, N :list, data :dict):
        """
        Return a set of connected artists for all nodes in N.

        N, a list of nodes.
        data, the class Graph
        """
        connected = set()
        for n in N:
            for token, _score in n.similar:
                if data[token] in N:
                    connected.add(n)
                    connected.add(data[token])
        return connected

    def run(self):
        G4 = AGraph(directed=True, concentrate=True)
        G4.graph_attr['bgcolor']='aliceblue'
        G4.graph_attr['overlap']='scale'
        G4.graph_attr['K']=0.75

        category = self.get_category()

        G4.add_node(
            category.id,
            shape='circle',
            color='#FFFFFF',
            label=self.category_name,
            fontname="courier",
            fontsize=12,
            style='filled',
            bgcolor="#FFFFFF",
            )
        artist_nodes = set([self.graph[m] for m in category.edges])
        connected = self.get_connected(artist_nodes, self.graph)

        for ca in connected:
            G4.add_node(
                ca.id,
                shape='circle',
                fixedsize=True,
                style='filled',
                bgcolor='#FFFFFF',
                width=0.25,
                color='#f08080',
                xlabel=ca.id,
                label='',
                fontsize=8,
                fontname="courier",
                )

        for ca in connected:
            for token, _score in ca.similar:
                if self.graph[token] in connected:
                    G4.add_edge(
                        ca.id,
                        self.graph[token].id,
                        color="pink",
                        arrowsize=0.5,
                        )

        G4.layout(prog='fdp')
        G4.draw(str(self.image_path))
