import datetime
from fileinput import filename
from os import curdir
from tkinter import Entry

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, MessageHandler, ConversationHandler

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command, \
							 market_keyboard_list, get_markets

from agency.models import Agency

ENTER_NAME, ENTER_ADDRESS, ENTER_PHONE, ENTER_IMAGE, ENTER_PASSPORT, MARKET_MENU = range(6)

def command_start(update: Update, context: CallbackContext) -> None:
	u, created = User.get_user_and_created(update, context)

	if created:
		text = static_text.start_created.format(first_name=u.first_name)
	else:
		text = static_text.start_not_created.format(first_name=u.first_name)
	update.message.reply_text(text=text, reply_markup=make_keyboard_for_start_command())

def register_level(update: Update, context: CallbackContext) -> None:
	user_id = extract_user_data_from_update(update)['user_id']
	text = static_text.register_name
	update.message.reply_text(text=text)
	return ENTER_NAME

full_name = None
address = None
phone = None
image = None
image_passport = None


def get_full_name(update: Update, context: CallbackContext):
	global full_name
	full_name = update.message.text
	text = static_text.register_address
	update.message.reply_text(text)
	return ENTER_ADDRESS


def get_address(update: Update, context: CallbackContext):
	global address
	address = update.message.text
	text = static_text.register_phone
	update.message.reply_text(text)
	return ENTER_PHONE


def get_phone(update: Update, context: CallbackContext):
	global phone
	phone = update.message.text
	text = static_text.register_image
	update.message.reply_text(text)
	return ENTER_IMAGE


def get_image(update: Update, context: CallbackContext):
	global image
	image = context.bot.getFile(update.message.photo[-1].file_id)
	image = image.download()
	text = static_text.register_passport
	update.message.reply_text(text)
	return ENTER_PASSPORT


def get_passport(update: Update, context: CallbackContext):
	global passport 
	passport = context.bot.getFile(update.message.photo[-1].file_id)
	passport = passport.download()
	print(f"{full_name}\n {address}\n {phone}\n {image}\n {passport}", )
	Agency.objects.create(full_name=full_name, address=address, phone=phone, 
						image=image, image_passport=passport)
	
	text = static_text.register_finished
	update.message.reply_text(text, reply_markup=get_markets())
	return MARKET_MENU


def get_market(update: Update, context: CallbackContext):
	update.message.reply_text(text="Bizning do'konlar", reply_markup=market_keyboard_list())
	return ConversationHandler.END
	