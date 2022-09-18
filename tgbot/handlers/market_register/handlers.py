import datetime
from turtle import update

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, MessageHandler, ConversationHandler
from telegram.replykeyboardremove import ReplyKeyboardRemove

from tgbot.handlers.market_register import static_text
from tgbot.models import User

from agency.models import Market
from django.conf import settings

MARKET_NAME, MARKET_DOCUMENT, MARKET_PHOTO, MARKET_OWNER_NAME, MARKET_OWNER_PHONE, MARKET_ADDRESS, MARKET_LOCATION = range(7)


def add_new_market(update: Update, context: CallbackContext):
	text = static_text.market_name
	update.message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())
	return MARKET_NAME

name = None
document = None
photo = None
owner_full_name = None
phone = None
address = None
location = None


def get_market_name(update: Update, context: CallbackContext):
	global name
	text = static_text.market_document
	if 3 <= len(update.message.text) <= 128:
		name = update.message.text
		update.message.reply_text(text)
		return MARKET_DOCUMENT
	else: 
		update.message.reply_text(text="Ism uzunligi 3-128 belgidan iborat bo'lishi kerak. Qaytdan kiriting!")
		return MARKET_NAME

# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404


# def download_image(path):
# 	file_path = os.path.join(settings.MEDIA_ROOT, path)
# 	if os.path.exists(file_path):
# 		with open(file_path, 'rb') as fh:
# 			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
# 			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
# 			return response
# 	raise Http404


def get_market_document(update: Update, context: CallbackContext):
	global document
	text = static_text.market_image
	document = context.bot.getFile(update.message.photo[-1].file_id)
	# print(image)
	# image = download_image(image['file_path'])
	# print(image)	
	update.message.reply_text(text)
	return MARKET_PHOTO


def get_market_photo(update: Update, context: CallbackContext):
	global photo
	photo = context.bot.getFile(update.message.photo[-1].file_id)
	# print(image)
	# image = download_image(image['file_path'])
	# print(image)	
	text = static_text.market_owner_name
	update.message.reply_text(text)
	return MARKET_OWNER_NAME


def get_owner_name(update: Update, context: CallbackContext):
	global owner_full_name
	text = static_text.market_owner_phone
	if 10 <= len(update.message.text) <= 128:
		owner_full_name = update.message.text
		update.message.reply_text(text)
		return MARKET_OWNER_PHONE
	else: 
		update.message.reply_text(text="Ism uzunligi 10-128 belgidan iborat bo'lishi kerak. Qaytdan kiriting!")
		return MARKET_OWNER_NAME


def get_owner_phone(update: Update, context: CallbackContext):
	global phone
	text = static_text.market_address
	num_prefixes = ['99', '98', '97', '95', '94', '93', '91', '90', '88', '77', '33']
	if len(update.message.text)==17:
		phone = update.message.text
		if phone[:4] == "+998" and phone[5:7] in num_prefixes:
			update.message.reply_text(text)
			return MARKET_ADDRESS
		else:
			update.message.reply_text(text="Iltimos, telefon raqamingizni na'munadagidek(+998 XX XXX XX XX) kiriting")
			return MARKET_OWNER_PHONE
	else: 
		update.message.reply_text(text="Iltimos, telefon raqamingizni na'munadagidek(+998 XX XXX XX XX) kiriting")
		return MARKET_OWNER_PHONE


def get_market_address(update: Update, context: CallbackContext):
	global address
	text = static_text.market_location
	if 10 <= len(update.message.text) <= 256:
		address = update.message.text
		update.message.reply_text(text)
		return MARKET_LOCATION
	else: 
		update.message.reply_text(text="Manzil uzunligi 10-256 belgidan iborat bo'lishi kerak. Qaytdan kiriting!")
		return MARKET_ADDRESS
	

def get_market_location(update: Update, context: CallbackContext):
	text = static_text.market_register_finished
	update.message.reply_text(text=text)

	return ConversationHandler.END
