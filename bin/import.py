from exhibition import Exhibition

class Import:
    def __init__(self, size=(2, 30)):
        """
        `size` import exhibitions between sizes (<min>, <max>).
        """
        self.size = size
        self.exhibitions = dict()

    def create_exhibition(self, row):
        # placeholder values, these:
        e = Exhibition(row['id'], row['title'], row['artists'])
        # Exhibition has routine? or tells artist to fetch?
        # e.fetch_artist_movements()
        self.add(e)
    
    def add(self, exhibition):
        minimum, maximum = self.size
        if minimum < exhibition.members and maximum > exhibition.members:
            id = exhibition.id
            self.exhibitions[id] = exhibition
            return self.exhibitions
        return False
    


