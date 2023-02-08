from letter import Letter
from user import User
import requests
import environ

env = environ.Env()

API = 'http://127.0.0.1:8000/'

def get_users():
    return requests.get(API + 'user/').json()

def register(user: User):
    requests.post(API + 'user/', user.get_data())

def user_exists(username: str):
    return requests.get(API + f'user/{username}/').ok

def mail(letter: Letter):
    requests.post(API + 'letter/', letter.get_data(), files={'photo': open(env('path'), 'rb')} if letter.photo else None)
    return dict(requests.get(API + f'user/{letter.receiver}/').json())['chat_id']

def get_valentines(receiver: str):
    return [Letter(json_data=letter) for letter in requests.get(API + f'letter/{receiver}/').json()]

def find_by_full_name(full_name: str):
    return [User(json_data=user) for user in requests.get(API + f'user/full_name/{full_name}/').json()]

def save_image(url):
    with open('image.jpg', 'wb') as new_file:
        new_file.write(requests.get(url).content)