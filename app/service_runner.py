#!/usr/bin/env python
import os
import asyncio
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from services.telegram_bot import TelegramBot


class ServiceRunner:
    def __init__(self):
        self.telegram_bot = TelegramBot()

    async def start(self):
        await self.telegram_bot.start()


def main():
    """Run administrative tasks."""

    # Initialize Telegram Bot
    service_runner = ServiceRunner()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(service_runner.start())


if __name__ == '__main__':
    main()
