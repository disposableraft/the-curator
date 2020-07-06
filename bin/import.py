from exhibition import Exhibition

class Import:
    def __init__(self, sizes_allowed=(2, 30)):
        """
        `sizes_allowed` import exhibitions between sizes (<min>, <max>).
        """
        self.sizes_allowed = sizes_allowed
        self.exhibitions = dict()

    def create_exhibition(self, row):
        # placeholder values, these:
        e = Exhibition(row['id'], row['title'], row['artists'])
        # Exhibition has routine? or tells artist to fetch?
        # e.fetch_artist_movements()
        self.add(e)
    
    def add(self, exhibition):
        minimum, maximum = self.sizes_allowed
        if minimum < exhibition.members and maximum > exhibition.members:
            id = exhibition.id
            self.exhibitions[id] = exhibition
            return self.exhibitions
        return False
    


