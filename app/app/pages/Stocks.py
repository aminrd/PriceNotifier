import time

from .PageBase import PageBase
from ..models import Stock, Other
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

    def post_hanlder(self, request):
        stock = get_stock_from_post_request(request)

        if not stock.is_valid():
            self.params["NOTIFY_ERROR"] = "The form is not valid!"
            return super().default_response(request)

        stock.save()
        return redirect('home')


class ModifyStock(PageBase):
    page_name = "Modify an existing stock tracking"
    template_name = "new_stock.html"

    def __init__(self, id):
        self.stock = get_object_or_404(Stock, pk=id)

    def get_hanlder(self, request):
        self.params["existing_stock"] = self.stock
        return super().get_hanlder(request)

    def post_hanlder(self, request):
        modified_stock = get_stock_from_post_request(request)
        if not modified_stock.is_valid():
            self.params["NOTIFY_ERROR"] = "The form is not valid!"
            return super().default_response(request)

        self.stock.name = modified_stock.name
        self.stock.code = modified_stock.code
        self.stock.low_value = modified_stock.low_value
        self.stock.high_value = modified_stock.high_value
        self.stock.base_value = modified_stock.base_value
        self.stock.notify = modified_stock.notify
        self.stock.last_modified = time.time()
        self.stock.save()

        return redirect('home')

    def delete_handler(self, request):
        self.stock.delete()
        return redirect('home')
