#!/usr/bin/env python
import os
import asyncio
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from services.telegram_bot import TelegramBot


def main():
    """Run administrative tasks."""

    # Initialize Telegram Bot
    bot = TelegramBot()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot.start())


if __name__ == '__main__':
    main()
