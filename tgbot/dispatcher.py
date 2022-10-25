"""
	Telegram event handlers
"""
import sys
import logging
from typing import Dict

import telegram.error
from telegram import Bot, Update, BotCommand
from telegram.ext import (
	Updater, Dispatcher, Filters,
	CommandHandler, MessageHandler, 
	CallbackQueryHandler, ConversationHandler,
)

from core.celery import app  # event processing in async mode
from core.settings import TELEGRAM_TOKEN, DEBUG

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.onboarding import static_text as onboarding_command
from tgbot.handlers.market_register import handlers as market_register_handlers
from tgbot.handlers.market_register import static_text as market_register_command
from tgbot.handlers.market_product import handlers as market_product_handlers
from tgbot.handlers.market_product import static_text as market_product_command


from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command


ENTER_NAME, ENTER_ADDRESS, ENTER_PHONE, ENTER_IMAGE, ENTER_PASSPORT, MARKET_MENU = range(6)

MARKET_NAME, MARKET_DOCUMENT, MARKET_PHOTO, MARKET_OWNER_NAME, MARKET_OWNER_PHONE, MARKET_ADDRESS, MARKET_LOCATION = range(7)


def setup_dispatcher(dp):
	"""
	Adding handlers for events from Telegram
	"""
	
	register_handler = ConversationHandler(
		entry_points=[
			MessageHandler(Filters.text(onboarding_command.register_button_text),
								onboarding_handlers.register_level),
		],
		states={
			ENTER_NAME: [
				MessageHandler(Filters.text & ~Filters.command, 
								onboarding_handlers.get_full_name),
			],
			ENTER_ADDRESS: [
				MessageHandler(Filters.text & ~Filters.command,
							   onboarding_handlers.get_address)
			],
			ENTER_PHONE: [
				MessageHandler(Filters.text & ~Filters.command,
							   onboarding_handlers.get_phone)                            
			],
			ENTER_IMAGE: [
			   MessageHandler(Filters.photo, onboarding_handlers.get_image)                         
			],
			ENTER_PASSPORT: [
			   MessageHandler(Filters.photo, onboarding_handlers.get_passport)                           
			],
			MARKET_MENU: [
				MessageHandler(Filters.text(onboarding_command.redirect_market),
								onboarding_handlers.get_market)
			]
		},

		fallbacks=[],
		allow_reentry=True
	)

	market_register_handler = ConversationHandler(
		entry_points=[
			MessageHandler(Filters.text(onboarding_command.add_market),
								market_register_handlers.add_new_market)
		],
		states={
			MARKET_NAME: [
				MessageHandler(Filters.text & ~Filters.command, 
								market_register_handlers.get_market_name),
			],
			MARKET_DOCUMENT: [
				MessageHandler(Filters.photo, market_register_handlers.get_market_document)
			],
			MARKET_PHOTO: [
				MessageHandler(Filters.photo, market_register_handlers.get_market_photo)                            
			],
			MARKET_OWNER_NAME: [
			   MessageHandler(Filters.text & ~Filters.command, market_register_handlers.get_owner_name)                         
			],
			MARKET_OWNER_PHONE: [
			   MessageHandler(Filters.text & ~Filters.command, market_register_handlers.get_owner_phone)                           
			],
			MARKET_ADDRESS: [
				MessageHandler(Filters.text & ~Filters.command, market_register_handlers.get_market_address)
			],
			MARKET_LOCATION: [
				MessageHandler(Filters.location, market_register_handlers.get_market_location)
			]
		},

		fallbacks=[],
		allow_reentry=True
	)

	# onboarding
	dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))
	dp.add_handler(CommandHandler("help", onboarding_handlers.command_help))

	# register handler in onboarding
	dp.add_handler(register_handler)

	# market handler in market_register
	dp.add_handler(market_register_handler)

	# product handler in market_product
	dp.add_handler(MessageHandler(Filters.text & ~Filters.command,
								market_product_handlers.get_market_info))




	# admin commands
	# dp.add_handler(CommandHandler("admin", admin_handlers.admin))
	# dp.add_handler(CommandHandler("stats", admin_handlers.stats))
	# dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))

	# # location
	# dp.add_handler(CommandHandler(
	#     "ask_location", location_handlers.ask_for_location))
	# dp.add_handler(MessageHandler(Filters.location,
	# 							  location_handlers.location_handler))

	# broadcast message
	# dp.add_handler(
	#     MessageHandler(Filters.regex(
	#         rf'^{broadcast_command}(/s)?.*'), broadcast_handlers.broadcast_command_with_message)
	# )
	# dp.add_handler(
	#     CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler,
	#                          pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
	# )

	# files
	# dp.add_handler(MessageHandler(
	# 	Filters.animation, files.show_file_id,
	# ))

	# handling errors
	dp.add_error_handler(error.send_stacktrace_to_tg_chat)

	# EXAMPLES FOR HANDLERS
	# dp.add_handler(MessageHandler(Filters.text, <function_handler>))
	# dp.add_handler(MessageHandler(
	# 	Filters.document, <function_handler>,
	# ))
	# dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
	# dp.add_handler(MessageHandler(
	# 	Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
	# 	& Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
	# 	<function_handler>,
	# ))

	return dp


def run_polling():
	""" Run bot in polling mode """
	updater = Updater(TELEGRAM_TOKEN, use_context=True)

	dp = updater.dispatcher
	dp = setup_dispatcher(dp)

	bot_info = Bot(TELEGRAM_TOKEN).get_me()
	bot_link = f"https://t.me/" + bot_info["username"]

	print(f"Polling of '{bot_link}' has started")
	# it is really useful to send '👋' emoji to developer
	# when you run local test
	# bot.send_message(text='👋', chat_id=<YOUR TELEGRAM ID>)

	updater.start_polling()
	updater.idle()


# Global variable - best way I found to init Telegram bot
bot = Bot(TELEGRAM_TOKEN)
try:
	TELEGRAM_BOT_USERNAME = bot.get_me()["username"]
except telegram.error.Unauthorized:
	logging.error(f"Invalid TELEGRAM_TOKEN.")
	sys.exit(1)


@app.task(ignore_result=True)
def process_telegram_event(update_json):
	update = Update.de_json(update_json, bot)
	dispatcher.process_update(update)


def set_up_commands(bot_instance: Bot) -> None:
	langs_with_commands: Dict[str, Dict[str, str]] = {
		'en': {
			'start': 'Start django bot 🚀',
			'stats': 'Statistics of bot 📊',
			'admin': 'Show admin info ℹ️',
			'ask_location': 'Send location 📍',
			'broadcast': 'Broadcast message 📨',
			'export_users': 'Export users.csv 👥',
		},
		'es': {
			'start': 'Iniciar el bot de django 🚀',
			'stats': 'Estadísticas de bot 📊',
			'admin': 'Mostrar información de administrador ℹ️',
			'ask_location': 'Enviar ubicación 📍',
			'broadcast': 'Mensaje de difusión 📨',
			'export_users': 'Exportar users.csv 👥',
		},
		'fr': {
			'start': 'Démarrer le bot Django 🚀',
			'stats': 'Statistiques du bot 📊',
			'admin': "Afficher les informations d'administrateur ℹ️",
			'ask_location': 'Envoyer emplacement 📍',
			'broadcast': 'Message de diffusion 📨',
			"export_users": 'Exporter users.csv 👥',
		},
		'ru': {
			'start': 'Запустить django бота 🚀',
			'stats': 'Статистика бота 📊',
			'admin': 'Показать информацию для админов ℹ️',
			'broadcast': 'Отправить сообщение 📨',
			'ask_location': 'Отправить локацию 📍',
			'export_users': 'Экспорт users.csv 👥',
		}
	}

	bot_instance.delete_my_commands()
	for language_code in langs_with_commands:
		bot_instance.set_my_commands(
			language_code=language_code,
			commands=[
				BotCommand(command, description) for command, description in langs_with_commands[language_code].items()
			]
		)


# WARNING: it's better to comment the line below in DEBUG mode.
# Likely, you'll get a flood limit control error, when restarting bot too often
set_up_commands(bot)

n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(
	bot, update_queue=None, workers=n_workers, use_context=True))
