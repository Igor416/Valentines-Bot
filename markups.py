from telebot import types
from commands import *

def to_main(function):
    def markup_getter() -> types.ReplyKeyboardMarkup:
        markup = function()
        markup.add(Button(COMMANDS[START]))
        return markup
    return markup_getter

def Markup(*args: str, row_width: int = 1) -> types.ReplyKeyboardMarkup:
    buttons = map(lambda arg: Button(COMMANDS[arg]), args)
    return types.ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons, row_width=row_width)

def Button(name) -> types.KeyboardButton:
    return types.KeyboardButton(name)

def get_markup(stage: str) -> types.ReplyKeyboardMarkup:
    try:
        return MARKUPS[f'get_{stage}_markup']()
    except:
        return get_empty_markup()

def get_start_markup():
    return Markup(SEND, VALENTINES, HELP, row_width=2)

@to_main
def get_send_markup() -> types.ReplyKeyboardMarkup:
    return Markup(UNKNOWN)

@to_main
def get_error_markup():
    return Markup(ERROR)

@to_main
def get_photo_markup() -> types.ReplyKeyboardMarkup:
    return Markup(PHOTO)

@to_main
def get_unfound_markup() -> types.ReplyKeyboardMarkup:
    return Markup(UNFOUND)

@to_main
def get_approve_markup() -> types.ReplyKeyboardMarkup:
    return Markup(APPROVE)

@to_main
def get_unknown_markup() -> types.ReplyKeyboardMarkup:
    return Markup(NAME, NONE, row_width=2)

@to_main
def get_empty_markup() -> types.ReplyKeyboardMarkup:
    return Markup()

MARKUPS = dict(filter(lambda pair: pair[0].endswith('_markup'), globals().items()))