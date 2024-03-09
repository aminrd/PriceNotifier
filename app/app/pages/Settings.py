from .PageBase import PageBase
from ..utility import Config


class Settings(PageBase):
    page_name = "Settings"
    template_name = "settings.html"

    def __init__(self):
        user_settings = UserSettings.Config()
        setting_list = sorted(user_settings.settings, key=lambda s: s.get_section())
        self.params['user_settings'] = setting_list
