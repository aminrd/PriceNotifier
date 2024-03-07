from .PageBase import PageBase
from ..models import Stock, Other
from ..utility.stock import sync_stocks


class Home(PageBase):
    page_name = "Existing Tracks"
    template_name = "home.html"

    def __init__(self):
        all_stocks = sync_stocks(Stock.objects.all())
        self.params['stocks'] = all_stocks
        self.params['others'] = Other.objects.all()
