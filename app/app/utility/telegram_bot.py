import logging
import asyncio
import telegram
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from ..utility.Config import get_telegram_api_key
from ..models import Token, User


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
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def sync_updates(self):
        offset = None
        bot = telegram.Bot(self.api_token)
        iteration, max_iter = 0, 1000

        while iteration < max_iter:
            iteration += 1
            updates = await bot.getUpdates(limit=1000, offset=offset)
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

def consume_token(token) -> User:
    try:
        user = User.objects.get(id=None)
    except:
        return None

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    token = get_token_by_message(update.message.text)
    if token is None:
        return

    token.delete()

    user = update.effective_user
    await update.message.reply_html(
        rf"{user.mention_html()} you have successfully subscribed to receive notifications in Telegram!",
        reply_markup=ForceReply(selective=True),
    )
    print(f"{user} has subscribed with messsage {update.message}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help!")


async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Why did you unsubscribe?!!!!")


if __name__ == '__main__':
    bot = TelegramBot()
