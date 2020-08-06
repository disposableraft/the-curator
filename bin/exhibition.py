from graph import Node
import uuid

class Exhibition(Node):
    def __init__(self, id, title, source):
        super().__init__(str(uuid.uuid4()))
        self.title = title
        self.source = source
        self.source_id = id
