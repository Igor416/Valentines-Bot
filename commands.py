START = 'start'

SEND = 'send'
ERROR = 'error'
TEXT = 'text'
PHOTO = 'photo'
MAIL = 'mail'
UNKNOWN = 'unknown'
NAME = 'name'
UNFOUND = 'unfound'
APPROVE = 'approve'
NONE = 'none'

VALENTINES = 'valentines'

HELP = 'help'

COMMANDS = {
    START: 'Главное меню',
    SEND: 'Отправить',
    ERROR: 'Попробовать снова',
    TEXT: 'Написать письмо',
    PHOTO: 'Пропустить',
    MAIL: 'Отослать',
    UNKNOWN: 'Я не знаю их тг',
    NAME: 'Я знаю их имя',
    UNFOUND: 'Заново',
    APPROVE: 'Да, это он/она',
    NONE: 'Я ничего не знаю(',
    VALENTINES: 'Мои валентинки',
    HELP: 'Как это работает?',
}

def get_command(text: str) -> str:
    try:
        return list(COMMANDS.keys())[list(COMMANDS.values()).index(text)]
    except:
        return text