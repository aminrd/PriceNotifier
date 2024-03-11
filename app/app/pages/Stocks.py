import time

from .PageBase import PageBase
from ..models import Stock
from ..utility.common import RequestParse
from django.shortcuts import redirect, get_object_or_404


def get_stock_from_post_request(request):
    parser = RequestParse(request)
    stock = Stock(
        name=parser.get_str("name"),
        base_value=parser.get_float("base_value"),
        last_value=parser.get_float("base_value"),
        low_value=parser.get_float("low_value"),
        high_value=parser.get_float("high_value"),
        code=parser.get_str("code"),
        notify=parser.get_radio("notify")
    )
    return stock


class NewStock(PageBase):
    page_name = "Track a new stock"
    template_name = "new_stock.html"

    def post_hanlder(self):
        stock = get_stock_from_post_request(self.request)
        stock.owner = self.user

        if not stock.is_valid():
            self.params["NOTIFY_ERROR"] = "The form is not valid!"
            return super().default_response()

        stock.save()
        return redirect('home')


class ModifyStock(PageBase):
    page_name = "Modify an existing stock tracking"
    template_name = "new_stock.html"

    def __init__(self, request, id):
        self.stock = get_object_or_404(Stock, pk=id)
        super().__init__(request)

    def get_hanlder(self):
        self.params["existing_stock"] = self.stock
        return super().get_hanlder()

    def post_hanlder(self):
        modified_stock = get_stock_from_post_request(self.request)
        modified_stock.owner = self.user

        if not modified_stock.is_valid():
            self.params["NOTIFY_ERROR"] = "The form is not valid!"
            return super().default_response()

        self.stock.name = modified_stock.name
        self.stock.code = modified_stock.code
        self.stock.low_value = modified_stock.low_value
        self.stock.high_value = modified_stock.high_value
        self.stock.base_value = modified_stock.base_value
        self.stock.notify = modified_stock.notify
        self.stock.last_modified = time.time()
        self.stock.save()

        return redirect('home')

    def delete_handler(self):
        self.stock.delete()
        return redirect('home')
