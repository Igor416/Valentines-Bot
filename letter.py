from telebot import types

class Letter:
    text: str
    photo: types.ChatPhoto
    sender: str
    receiver: str

    def __init__(self, json_data=None):
        if json_data:
            for key, value in dict(json_data).items():
                setattr(self, key, value)
            return
        self.text = ''
        self.photo = None
        self.sender = ''
        self.receiver = ''

    def get_data(self):
        return {
            'text': self.text,
            'photo': self.photo,
            'sender': self.sender,
            'receiver': self.receiver
        }