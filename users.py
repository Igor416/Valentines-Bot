from user import User
from telebot.types import Message
from api import register

class Users:
    def __init__(self, users):
        self.users = {}
        for user in users:
            user = User(json_data=user)
            self.users[user.username] = user

    def get(self, message: Message) -> User:
        return self.users[message.from_user.username]

    def add(self, message: Message) -> User:
        user = User(message.chat.id, message.from_user.username, message.from_user.full_name)
        self.users[message.from_user.username] = user
        register(user)
        return user
    
    def __contains__(self, user) -> bool:
        return user in self.users

    def __str__(self) -> str:
        return str(self.users)

    def __repr__(self) -> str:
        return str(self)