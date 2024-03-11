from ..models import Settings
from ..settings import TELEGRAM_BOT_API_key


def get_all_settings():
    return Settings.objects.all()


TELEGRAM_BOT_API_KEY_CONFIG = "notif:telegram::api_key"
RUNTIME_FREQUENCY_MINUTES = "app:logic::frequency_minutes"


def init_configs():
    init_setting_list = (
        Settings(key=TELEGRAM_BOT_API_KEY_CONFIG, value=TELEGRAM_BOT_API_key),
        Settings(key=RUNTIME_FREQUENCY_MINUTES, value="3600"),
    )

    for setting in init_setting_list:
        try:
            existing_setting = Settings.objects.get(pk=setting.key)
        except:
            existing_setting = None

        if existing_setting is None:
            setting.save()


class Config:
    settings = None

    def __init__(self):
        init_configs()
        self.settings = Settings.objects.all()


def get_telegram_api_key() -> str:
    try:
        setting = Settings.objects.get(key=TELEGRAM_BOT_API_KEY_CONFIG)
        return setting.value
    except:
        return TELEGRAM_BOT_API_key
