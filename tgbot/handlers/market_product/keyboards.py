from telegram import ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.market_product.static_text import product_given, money_received_debt, photo_report

def market_info_btn() -> ReplyKeyboardMarkup:
    buttons = [
        [product_given],
        [money_received_debt],
        [photo_report]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

