from .PageBase import PageBase
from ..utility import Config


class Settings(PageBase):
    page_name = "Settings"
    template_name = "settings.html"

    def __init__(self, request):
        super().__init__(request)
        user_settings = Config.Config()
        setting_list = sorted(user_settings.settings, key=lambda s: s.get_section())
        self.params['user_settings'] = setting_list
