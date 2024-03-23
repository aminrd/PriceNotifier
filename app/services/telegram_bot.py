import logging
import asyncio
from asgiref.sync import sync_to_async
from typing import Optional
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, Updater

from django.contrib.auth.models import User
from app.utility.Config import get_telegram_api_key
from app.models import Token, TelegramSubscribe
from app.settings import APPLICATION_NAME
from app.common_variables import ONE_TIME_TOKEN_LENGTH


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

        self.updater = Updater(self.api_token)

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
                    await subscribe(update, ContextTypes.DEFAULT_TYPE)
                elif "unsubscribe" in update.message.text:
                    await unsubscribe(update, ContextTypes.DEFAULT_TYPE)
                else:
                    self.logger.log(logging.WARNING, f"Unhandled update message in the telegram bot {0}", update)

                offset = update.update_id + 1

    async def notify_users(self, receivers: Optional["Users"]):
        pass


def is_valid_string(obj: str, expected_length: int = None):
    if obj is None or not isinstance(obj, str):
        return False

    if expected_length is not None:
        return len(obj) == expected_length

    return True


def get_token_from_message(message: str) -> str:
    if not is_valid_string(message):
        return ""

    split_message = message.strip().split()
    if len(split_message) < 2:
        return ""

    return split_message[1]


def get_user_by_token(token_key: str) -> User:
    if not is_valid_string(token_key, ONE_TIME_TOKEN_LENGTH):
        return None

    try:
        token = Token.objects.get(pk=token_key)
        if token.is_expired():
            return None

        return token.user
    except:
        return None


def subscribe_telegram_to_user_profile(telegram_user_id: int, user: User):
    telegram_subscription = TelegramSubscribe.objects.get_or_create(id=telegram_user_id, user=user)
    return telegram_subscription


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user
    if update.message is None:
        return

    token_key = get_token_from_message(update.message.text)
    user = await sync_to_async(get_user_by_token, thread_sensitive=True)(token_key=token_key)
    if user is None:
        await update.message.reply_html(rf"{telegram_user.mention_html()} your token is not valid or expired!")
        return

    telegram_subscription = await sync_to_async(subscribe_telegram_to_user_profile, thread_sensitive=True)(
        telegram_user_id=telegram_user.id, user=user)

    if telegram_subscription is None:
        await update.message.reply_html(rf"Unable to create a telegram subscription for user! User was not found!")
        return

    await update.message.reply_html(
        rf"{telegram_user.mention_html()} you have successfully subscribed to receive notifications in Telegram!")


def unsubscribe_telegram_user(telegram_user_id: int):
    try:
        telegram_subscription = TelegramSubscribe.objects.get(telegram_user_id)
        telegram_subscription.delete()
    except:
        return


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_user = update.effective_user
    await sync_to_async(unsubscribe_telegram_user, thread_sensitive=True)(telegram_user_id=telegram_user.id)

    await update.message.reply_html(
        rf"{telegram_user.mention_html()} you have successfully unsubscribed to receive notifications in Telegram!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = rf""" Hi {update.effective_user.mention_html()}! 
    To use this bot, first generate a token in {APPLICATION_NAME} and then use: 
    
    /subscribe **token**  : to start subscribing all price notifications on your account

    Or just use 
    /unsubscribe          : to stop subscribing through telegram
    """
    await update.message.reply_html(help_message)
