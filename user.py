from letter import Letter
from search import Search

class User:
    chat_id: int
    username: str
    full_name: str
    last_action: str
    current_letter: Letter
    search: Search

    def __init__(self, chat_id='', username='', full_name='', json_data=None):
        self.default()
        if json_data:
            for key, value in dict(json_data).items():
                setattr(self, key, value)
            return
        self.chat_id, self.username, self.full_name = chat_id, username, full_name

    def set_letter(self):
        self.current_letter = Letter()

    def default(self):
        self.last_action = None
        self.current_letter = None
        self.handler = None
        self.clear_search()

    def create_search(self, query):
        self.search = Search(query)

    def clear_search(self):
        self.search = None

    def get_data(self):
        return {
            'chat_id': self.chat_id,
            'username': self.username,
            'full_name': self.full_name
        }