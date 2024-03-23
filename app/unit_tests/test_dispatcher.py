from unittest import TestCase
from collections import defaultdict

from test_setup import setup
setup()

from services.dispatcher import Dispatcher
from app.models.Subscribers import *
from app.models.Prices import ChangeLogBase


class MockNotificationService:
    notifications = defaultdict(list)

    def notify(self, subscriber, changelog):
        self.notifications[subscriber].append(changelog)


class TestDispatcher(TestCase):
    def setUp(self):
        self.telegram_bot = MockNotificationService()
        self.email_server = MockNotificationService()
        self.sms_server = MockNotificationService()

        self.dispatcher = Dispatcher(self.telegram_bot, self.email_server, self.sms_server)


class TestDispatchMsgToUserAsync(TestDispatcher):

    async def test_telegram_notification(self):
        subscribers = [TelegramSubscribe() for _ in range(5)]
        changelog = ChangeLogBase()
        await self.dispatcher.dispatch_msg_to_user_async(subscribers, changelog)

        for subscriber in subscribers:
            sent_notifications = self.telegram_bot.notifications[subscriber]
            self.assertIn(changelog, sent_notifications)
