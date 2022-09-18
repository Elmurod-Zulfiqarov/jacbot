import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, MessageHandler, ConversationHandler
from telegram.replykeyboardremove import ReplyKeyboardRemove

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command, \
							 market_keyboard_list, get_markets

from agency.models import Agency
from django.conf import settings

ENTER_NAME, ENTER_ADDRESS, ENTER_PHONE, ENTER_IMAGE, ENTER_PASSPORT, MARKET_MENU = range(6)

def command_start(update: Update, context: CallbackContext) -> None:
	u, created = User.get_user_and_created(update, context)
	if created:
		text = static_text.start_created.format(first_name=u.first_name)
	else:
		text = static_text.start_not_created.format(first_name=u.first_name)
	update.message.reply_text(text=text, reply_markup=make_keyboard_for_start_command())

def register_level(update: Update, context: CallbackContext) -> None:
	text = static_text.register_name
	update.message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())
	return ENTER_NAME

full_name = None
address = None
phone = None
image = None
image_passport = None


def get_full_name(update: Update, context: CallbackContext):
	global full_name
	text = static_text.register_address
	if 10 <= len(update.message.text) <= 128:
		full_name = update.message.text
		update.message.reply_text(text)
		return ENTER_ADDRESS
	else: 
		update.message.reply_text(text="Ism uzunligi 10-128 belgidan iborat bo'lishi kerak. Qaytdan kiriting!")
		return ENTER_NAME


def get_address(update: Update, context: CallbackContext):
	global address
	text = static_text.register_phone
	if 10 <= len(update.message.text) <= 256:
		address = update.message.text
		update.message.reply_text(text)
		return ENTER_PHONE
	else: 
		update.message.reply_text(text="Manzil uzunligi 10-256 belgidan iborat bo'lishi kerak. Qaytdan kiriting!")
		return ENTER_ADDRESS


def get_phone(update: Update, context: CallbackContext):
	global phone
	text = static_text.register_image
	num_prefixes = ['99', '98', '97', '95', '94', '93', '91', '90', '88', '77', '33']
	if len(update.message.text)==17:
		phone = update.message.text
		if phone[:4] == "+998" and phone[5:7] in num_prefixes:
			update.message.reply_text(text)
			return ENTER_IMAGE
		else:
			update.message.reply_text(text="Iltimos, telefon raqamingizni na'munadagidek(+998 XX XXX XX XX) kiriting")
			return ENTER_PHONE
	else: 
		update.message.reply_text(text="Iltimos, telefon raqamingizni na'munadagidek(+998 XX XXX XX XX) kiriting")
		return ENTER_PHONE


# import os
# from django.conf import settings
# from django.http import HttpResponse, Http404


# def download_image(path):
# 	file_path = os.path.join(settings.MEDIA_ROOT, path)
# 	print(file_path)
# 	print(os.path.exists(file_path))

# 	if os.path.exists(file_path):
# 		print(os.path.exists(file_path))
# 		with open(file_path, 'rb') as fh:
# 			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
# 			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
# 			return response
# 	raise Http404


def get_image(update: Update, context: CallbackContext):
	global image
	image = context.bot.getFile(update.message.photo[-1].file_id)
	# print(image)
	# image = download_image(image['file_path'])
	# print(image)	
	text = static_text.register_passport
	update.message.reply_text(text)
	return ENTER_PASSPORT


def get_passport(update: Update, context: CallbackContext):
	global passport 
	passport = context.bot.getFile(update.message.photo[-1].file_id)
	# print(passport)
	# passport = download_image(passport['file_path'])
	# print(passport)
	# print(f"{full_name}\n {address}\n {phone}\n {image}\n {passport}", )
	# Agency.objects.create(full_name=full_name, address=address, phone=phone, 
	# 					image=image, image_passport=passport)
	
	text = static_text.register_finished
	update.message.reply_text(text, reply_markup=get_markets())
	return MARKET_MENU


def get_market(update: Update, context: CallbackContext):
	update.message.reply_text(text=static_text.redirect_market, reply_markup=market_keyboard_list())
	return ConversationHandler.END
	