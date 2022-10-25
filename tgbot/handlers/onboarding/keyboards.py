from telegram import ReplyKeyboardMarkup

from tgbot.handlers.onboarding.static_text import register_button_text, redirect_market, add_market

from agency.models import Market


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
    # test_data = ["Market 1(fake)", "Market 2(fake)", "Market 3(fake)"]
    markets = Market.objects.all()
    buttons = []
    
    for market in markets:
            buttons.append([market.name])

    # for fake in test_data:
    #         buttons.append([fake])

    buttons.append([add_market])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    
