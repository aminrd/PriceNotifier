from .PageBase import PageBase
from ..models import Stock, Other


class NewOther(PageBase):
    page_name = "Add new custom price tracker"
    template_name = "new_other.html"


class ModifyOther(PageBase):
    page_name = "Modify an existing custom price tracker"
    template_name = "new_other.html"

    def __init__(self, request, id):
        self.id = id
        super().__init__(request)
