from telebot import TeleBot, types
import environ
from markups import get_markup, get_empty_markup
from users import Users
from user import User
from commands import *
import api
import os

env = environ.Env()
bot = TeleBot(env('token'))
users = Users(api.get_users())

def log(function):
    def some_action(message: types.Message, *args, **kwargs):
        users.get(message).last_action = get_command(message.text)
        return function(message, *args, **kwargs)
    return some_action

def get_current_user(function):
    def some_action(message: types.Message):
        current_user = users.get(message)
        return function(message, current_user)
    return some_action

@bot.message_handler(commands=[START])
@log
def start_action(message: types.Message):
    if message.from_user.username not in users:
        user = users.add(message)
    else:
        user = users.get(message)
    user.default()
    bot.send_message(message.chat.id, 'Хотите признаться в своих чувствах, но стесняетесь?\nОтправьте анонимную валентинку своему возлюбленному или возлюбленной', reply_markup=get_markup(START))

##### Send actions #####
@log
@bot.message_handler(commands=[SEND])
def send_action(message: types.Message):
    bot.send_message(message.chat.id, 'Введите тг', reply_markup=get_markup(SEND))

@log
def error_action(message: types.Message):
    send_action(message)

@log
def text_action(message: types.Message):
    bot.send_message(message.chat.id, 'Напишите письмо ему/ей', reply_markup=get_empty_markup())

@log
def photo_action(message: types.Message):
    bot.send_message(message.chat.id, 'Отправьте фотку или картинку для него/нее', reply_markup=get_markup(PHOTO))

@get_current_user
@log
def mail_action(message: types.Message, sender: User = None):
    sender.current_letter.sender = message.from_user.username
    chat_id = api.mail(sender.current_letter)
    bot.send_message(chat_id, f'Для вас новая валентинка: "{sender.current_letter.text}"', reply_markup=get_markup(START))
    if sender.current_letter.photo:
        bot.send_photo(chat_id, bot.download_file(sender.current_letter.photo))
        os.remove(env('path'))
    sender.current_letter = None
    bot.send_message(message.chat.id, 'Сообщение отправлено', reply_markup=get_markup(START))

@log
def unknown_action(message: types.Message):
    bot.send_message(message.chat.id, 'А что вы знаете?', reply_markup=get_markup(UNKNOWN))

@log
def name_action(message: types.Message):
    bot.send_message(message.chat.id, 'Введите его/ее имя', reply_markup=get_markup(NAME))

@get_current_user
@log
def found_action(message: types.Message, user: User = None):
    user.search.search()
    if len(user.search.users) == 0:
        bot.send_message(message.chat.id, f'Я не смог найти "{user.search.query}"', reply_markup=get_markup(UNFOUND))
    elif len(user.search.users) == 1:
        bot.send_message(message.chat.id, f'Я нашел "{user.search.query}", их ник: {user.search.users[0].username} Это он/она?', reply_markup=get_markup(APPROVE))
    else:
        user.handler = choose_handler
        lst = '\n'.join([str(i + 1) + '. ' + user.search.users[i].username for i in range(len(user.search.users))])
        bot.send_message(message.chat.id, f'Я нашел несколько пользователей с таким именем {user.search.query}' + '\n' + f'{lst}.\nЕсли тут есть тот, кого вы искали, то введите соответствущюю цифру', reply_markup=get_markup(UNFOUND))

@get_current_user
@log
def unfound_action(message: types.Message, user: User = None):
    user.clear_search()
    return name_action(message)

@get_current_user
@log
def approve_action(message: types.Message, user: User = None):
    user.last_action = SEND
    user.handler = send_handler
    user.set_letter()
    user.current_letter.receiver = user.search.users[0].username
    user.clear_search()
    text_action(message)

@get_current_user
@log
def none_action(message: types.Message, user: User = None):
    user.clear_search()
    bot.send_message(message.chat.id, 'Увы, тогда я бессилен!', reply_markup=get_empty_markup())
#####   #####

##### Valentines actions #####
@bot.message_handler(commands=[VALENTINES])
@get_current_user
@log
def valentines_action(message: types.Message, receiver: User = None):
    receiver.default()
    letters = api.get_valentines(message.from_user.username)
    if len(letters) == 0:
        bot.send_message(message.chat.id, 'Вам пока что не присылали валентинок(', reply_markup=get_empty_markup())
    else:
        bot.send_message(message.chat.id, f'У вас {len(letters)} валентинок, ура!')
        i = 1
        for l in letters:
            bot.send_message(message.chat.id, f'{i}. {l.text}')
            if l.photo:
                api.save_image(l.photo)
                bot.send_photo(message.chat.id, open('image.jpg', 'rb'))
            i += 1
        try:
            os.remove(env('path'))
        except:
            pass
        bot.send_message(message.chat.id, 'Пока что все', reply_markup=get_empty_markup())
#####   #####

##### Help actions #####
@bot.message_handler(commands=[HELP])
@get_current_user
@log
def help_action(message: types.Message, user: User = None):
    user.default()
    bot.send_message(message.chat.id, 'Я могу отправить ваше сообщение или картинку в директ человеку.\nЯ запоминаю только ваше имя и ник в тг, чтобы вам могли отправлять валентинки, мой создатель видит лишь всех зарегестрированных пользователей, но не валентинки отправленные ими или им - анонимность же. Сделано @grosu_igor', reply_markup=get_markup(HELP))
#####   #####

callbacks = dict(filter(lambda pair: pair[0].endswith('_action'), globals().items()))
cut_username = lambda username: username.replace('https://t.me/', '').replace('@', '')

@bot.message_handler(content_types=['text', 'photo'])
@get_current_user
def reply_to_button(message: types.Message, user: User = None):
    if user.handler:
        user.handler(message)
        return
    if message.text in COMMANDS.values():
        try:
            callbacks[get_command(message.text) + '_action'](message)
        except:
            bot.send_message(message.chat.id, 'Я вас не понял, выберите что-то из меню', reply_markup=get_markup(START))
    elif user.last_action == SEND or user.last_action == ERROR:
        if api.user_exists(cut_username(message.text)):
            user.handler = send_handler
            user.set_letter()
            user.current_letter.receiver = cut_username(message.text)
            text_action(message)
        else:
            bot.send_message(message.chat.id, 'Такой пользователь не зарегестрирован!', reply_markup=get_markup(ERROR))
    elif user.last_action == NAME:
        user.create_search(message.text)
        found_action(message)
    else:
        bot.send_message(message.chat.id, 'Я вас не понял, выберите что-то из меню', reply_markup=get_markup(START))

@get_current_user
def send_handler(message: types.Message, user: User = None):
    if not user.last_action or user.current_letter == None:
        user.handler = None
        return reply_to_button(message)
    if user.last_action.startswith('@') or user.last_action.startswith('https://t.me/') or user.last_action == user.current_letter.receiver or user.last_action == APPROVE:
        user.current_letter.text = message.text
        photo_action(message)
    elif user.last_action == user.current_letter.text or message.photo:
        if message.photo:
            user.current_letter.photo = bot.get_file(message.photo[-1].file_id).file_path
            with open('image.jpg', 'wb') as new_file:
                new_file.write(bot.download_file(user.current_letter.photo))
        mail_action(message)
    else:
        user.handler = None
        reply_to_button(message)

@get_current_user
def choose_handler(message: types.Message, user: User = None):
    if message.text.isnumeric():
        if int(message.text) - 1 < len(user.search.users):
            user.last_action = SEND
            user.handler = None
            message.text = user.search.users[int(message.text) - 1].username
            return reply_to_button(message)

    user.handler = None
    reply_to_button(message)

if __name__ == '__main__':
    print('reloaded')
    bot.polling(True)

