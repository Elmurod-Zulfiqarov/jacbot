import datetime
import requests
import tempfile

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

def download_image(image_url):
	# Stream the image from the url
	response = requests.get(image_url, stream=True)
	
	# Get the filename from the url, used for saving later
	file_name = image_url.split('/')[-1]
	
	# Create a temporary file
	lf = tempfile.NamedTemporaryFile()

	# Read the streamed image in sections
	for block in response.iter_content(1024 * 8):
		
		# If no more file then stop
		if not block:
			break

		# Write image block to temporary file
		lf.write(block)

	return {"file_name": file_name, "lf": lf}
	

def get_image(update: Update, context: CallbackContext):
	global image
	image = context.bot.getFile(update.message.photo[-1].file_id)
	image = download_image(image['file_path'])
	text = static_text.register_passport
	update.message.reply_text(text)
	return ENTER_PASSPORT


def get_passport(update: Update, context: CallbackContext):
	global passport 
	passport = context.bot.getFile(update.message.photo[-1].file_id)
	passport = download_image(passport['file_path'])
	print(f"{full_name}\n {address}\n {phone}\n {image}\n {passport}", )

	agency = Agency()
	agency.full_name = full_name
	agency.address = address
	agency.phone = phone
	agency.image.save(image["file_name"], image["lf"])
	agency.image_passport.save(passport["file_name"], passport["lf"])

	text = static_text.register_finished
	update.message.reply_text(text, reply_markup=get_markets())
	return MARKET_MENU


def get_market(update: Update, context: CallbackContext):
	update.message.reply_text(text=static_text.redirect_market, reply_markup=market_keyboard_list())
	return ConversationHandler.END
	