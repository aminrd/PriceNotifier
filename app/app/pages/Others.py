from .PageBase import PageBase
from ..models import Stock, Other


class NewOther(PageBase):
    page_name = "Add new custom price tracker"
    template_name = "new_other.html"

    def __init__(self):
        pass

class ModifyOther(PageBase):
    page_name = "Modify an existing custom price tracker"
    template_name = "new_other.html"

    def __init__(self, id):
        self.id = id
