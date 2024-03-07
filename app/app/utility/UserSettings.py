from ..models import Settings


def get_all_settings():
    return Settings.objects.all()


TELEGRAM_BOT_API_KEY_CONFIG = "notif:telegram::api_key"
RUNTIME_FREQUENCY_MINUTES = "app:logic::frequency_minutes"


def init_settings():
    init_setting_list = (
        Settings(key=TELEGRAM_BOT_API_KEY_CONFIG, value=""),
        Settings(key=RUNTIME_FREQUENCY_MINUTES, value="3600"),
    )

    for setting in init_setting_list:
        try:
            existing_setting = Settings.objects.get(pk=setting.key)
        except:
            existing_setting = None

        if existing_setting is None:
            setting.save()


class UserSettings:
    settings = None

    def __init__(self):
        init_settings()
        self.settings = Settings.objects.all()

