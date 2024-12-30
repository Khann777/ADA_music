from django.core.management.base import BaseCommand
from telegram_bot.bot import start_bot

class Command(BaseCommand):
    help = "Запуск Telegram бота"

    def handle(self, *args, **kwargs):
        start_bot()
