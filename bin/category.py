from graph import Node

class Category(Node):
    def __init__(self, title):
        self.title = title
        self.id = title
        super().__init__(self.id)