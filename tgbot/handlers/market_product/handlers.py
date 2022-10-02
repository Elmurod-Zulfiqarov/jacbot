from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, MessageHandler, ConversationHandler
from telegram.replykeyboardremove import ReplyKeyboardRemove

from tgbot.handlers.market_product.keyboards import market_info_btn

from agency.models import Market
from django.conf import settings


def get_market_info(update: Update, context: CallbackContext):
	market_name = update.message.text
	markets = Market.objects.all()
	for market in markets:
		if market.name == market_name:
			text = f"{market_name} do'koni haqida ma'lumot"
			update.message.reply_text(text, reply_markup=market_info_btn())
			break
	else:
		print("Bunday do'kon mavjud emas!")
	print("Tugadi!")
