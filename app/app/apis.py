from django.http import JsonResponse
from .utility import stock


def get_current_price(request, code: str):
    result = stock.get_current_stock_price(code)
    if result.success:
        return JsonResponse({"price": result.item})
    else:
        return api404(request, result.message)


def get_year_price(request, code: str, years: int = 1):
    result = stock.get_year_stock_price(code, years)
    if result.success:
        return JsonResponse({"price": result.item.to_json()})
    else:
        return api404(request, result.message)


def api404(request, error='The resource was not found'):
    return JsonResponse({
        'status_code': 404,
        'error': error
    })
