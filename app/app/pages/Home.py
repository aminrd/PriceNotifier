from .PageBase import PageBase
from ..utility.stock import sync_stocks


class Home(PageBase):
    page_name = "Existing Tracks"
    template_name = "home.html"

    def __init__(self, request):
        super().__init__(request)
        self.params['stocks'] = sync_stocks(self.user.user_stocks.all())
        self.params['others'] = self.user.user_others.all()
