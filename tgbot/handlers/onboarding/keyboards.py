from telegram import ReplyKeyboardMarkup

from tgbot.handlers.onboarding.manage_data import REGISTER_LEVEL_BUTTON
from tgbot.handlers.onboarding.static_text import register_button_text, redirect_market, add_market


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    buttons = [
            [register_button_text]
        ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_markets() -> ReplyKeyboardMarkup:
    buttons = [
            [redirect_market]
        ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def market_keyboard_list() -> ReplyKeyboardMarkup:
    test_data = ["Market 1", "Market 2", "Market 3", "Market 4", "Market 5","Market 6"]
    buttons = []
    for i in test_data:
            buttons.append([i])

    buttons.append([add_market])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    
