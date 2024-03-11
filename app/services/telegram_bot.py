import os
import sys
from pathlib import Path
import logging
import asyncio
import django
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Connecting to Django ORM
app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from app.utility.Config import get_telegram_api_key
from app.models import Token, TelegramSubscribe
from app.settings import APPLICATION_NAME

class TelegramBot:
    api_token = ""

    def __init__(self):
        self.api_token = get_telegram_api_key()
        if len(self.api_token) < 1:
            raise Exception("Telegram Bot API Token was not found!")

        # setup the logger
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        logging.getLogger("httpx").setLevel(logging.WARNING)
        self.logger = logging.getLogger(__name__)

        asyncio.run(self.sync_updates())

        application = Application.builder().token(self.api_token).build()
        application.add_handler(CommandHandler("subscribe", subscribe))
        application.add_handler(CommandHandler("unsubscribe", unsubscribe))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help_command))
        self.application = application

    def start(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def sync_updates(self):
        offset = None
        bot = telegram.Bot(self.api_token)
        iteration, max_iter = 0, 1000

        while iteration < max_iter:
            iteration += 1
            updates = await bot.getUpdates(limit=100, offset=offset)
            if len(updates) < 1:
                return

            for update in updates:
                if "subscribe" in update.message.text:
                    await subscribe(update)
                elif "unsubscribe" in update.message.text:
                    await unsubscribe(update)
                else:
                    self.logger.log(logging.WARNING, f"Unhandled update message in the telegram bot {0}", update)

                offset = update.update_id + 1


def get_token_by_message(message: str) -> Token:
    try:
        _, token_key = message.strip().split()
        token = Token.objects.get(id=token_key)
        return token
    except:
        return None


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    token = get_token_by_message(update.message.text)
    if token is None or (user := token.user) is None:
        return

    token.delete()
    telegram_user = update.effective_user
    TelegramSubscribe.objects.get_or_create(id=telegram_user.id, user=user)
    await update.message.reply_html(
        rf"{telegram_user.mention_html()} you have successfully subscribed to receive notifications in Telegram!")


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user

    try:
        telegram_subscription = TelegramSubscribe.objects.get(telegram_user.id)
    except:
        return

    telegram_subscription.delete()
    await update.message.reply_html(
        rf"{telegram_user.mention_html()} you have successfully unsubscribed to receive notifications in Telegram!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = rf""" Hi {update.effective_user.mention_html()}! 
    To use this bot, first generate a token in {APPLICATION_NAME} and then use: 
    
    /subscribe **token**  : to start subscribing all price notifications on your account

    Or just use 
    /unsubscribe          : to stop subscribing through telegram
    """
    print(help_message)
    await update.message.reply_html(help_message)


if __name__ == '__main__':
    bot = TelegramBot()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start())

