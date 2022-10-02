from telegram import ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.market_register.static_text import market_location

def location_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(market_location, request_location=True)]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

