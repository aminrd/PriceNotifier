from .PageBase import PageBase
from ..models import Stock, Other


class NewStock(PageBase):
    page_name = "Track a new stock"
    template_name = "new_stock.html"

    def __init__(self):
        pass

class ModifyStock(PageBase):
    page_name = "Modify an existing stock tracking"
    template_name = "new_stock.html"

    def __init__(self):
        pass
