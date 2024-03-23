from typing import List
from app.models.Prices import ChangeLogBase
from app.models.Subscribers import Subscriber, TelegramSubscribe


class Dispatcher:
    def __init__(self, telegram_bot=None, email_server=None, sms_server=None):
        self.telegram_bot = telegram_bot
        self.email_server = email_server
        self.sms_server = sms_server

    async def dispatch_msg_to_user_async(self, changelog: ChangeLogBase, subscribers: List[Subscriber]) -> None:
        for subscriber in subscribers:
            if subscriber.type == TelegramSubscribe.type:
                # self.telegram_bot.notifiy(changelog)
                pass
            else:
                pass
