import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from tgbot.dispatcher import run_polling

if __name__ == "__main__":
    run_polling()
