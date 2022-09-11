from tgbot.dispatcher import run_polling
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()


if __name__ == "__main__":
    run_polling()
