import datetime
import requests
import tempfile

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, MessageHandler, ConversationHandler
from telegram.replykeyboardremove import ReplyKeyboardRemove

from tgbot.handlers.market_register import static_text
from tgbot.models import Location, User
from tgbot.handlers.market_register.keyboards import location_keyboard

from agency.models import Market
from django.conf import settings

MARKET_NAME, MARKET_DOCUMENT, MARKET_PHOTO, MARKET_OWNER_NAME, MARKET_OWNER_PHONE, MARKET_ADDRESS, MARKET_LOCATION = range(7)

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
		update.message.reply_text(text=static_text.check_name)
		return MARKET_NAME


def get_market_document(update: Update, context: CallbackContext):
	global document
	text = static_text.market_image
	document = context.bot.getFile(update.message.photo[-1].file_id)
	document = download_image(document['file_path'])
	update.message.reply_text(text)
	return MARKET_PHOTO


def get_market_photo(update: Update, context: CallbackContext):
	global photo
	photo = context.bot.getFile(update.message.photo[-1].file_id)
	photo = download_image(photo['file_path'])
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
		update.message.reply_text(text=static_text.check_name)
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
			update.message.reply_text(text=static_text.check_phone)
			return MARKET_OWNER_PHONE
	else: 
		update.message.reply_text(text=static_text.check_phone)
		return MARKET_OWNER_PHONE


def get_market_address(update: Update, context: CallbackContext):
	global address
	text = static_text.market_location
	if 10 <= len(update.message.text) <= 256:
		address = update.message.text
		update.message.reply_text(text, reply_markup=location_keyboard())
		return MARKET_LOCATION
	else: 
		update.message.reply_text(text=static_text.check_address)
		return MARKET_ADDRESS
	

def get_market_location(update: Update, context: CallbackContext):
	location = update.message.location.to_dict()
	text = static_text.market_register_finished
	
	market = Market()
	market.name = name
	market.owner_full_name = owner_full_name
	market.phone = phone
	market.address = address
	market.location = location
	market.document.save(document["file_name"], document["lf"])
	market.photo.save(photo["file_name"], photo["lf"])

	update.message.reply_text(text=text, reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END
