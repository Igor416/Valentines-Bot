class Search:
    def __init__(self, query):
        self.query = query
        self.users = []

    def search(self):
        from api import find_by_full_name
        self.users = find_by_full_name(self.query)
        return self.users