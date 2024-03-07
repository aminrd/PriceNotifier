from .PageBase import PageBase
from ..models import Stock, Other


class Home(PageBase):
    page_name = "Existing Tracks"
    template_name = "home.html"

    def __init__(self):
        self.params['stocks'] = Stock.objects.all()
        self.params['others'] = Other.objects.all()
