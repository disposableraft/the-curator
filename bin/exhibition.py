from nodes import Node

class Exhibition(Node):
    def __init__(self, id, title):
        super().__init__(id)
        self.title = title
