import time
from asgiref.sync import sync_to_async
import yfinance as yf

from ..common_variables import Result
from ..models import Stock

type StockList = list[Stock]


def get_current_stock_price(code: str) -> Result:
    result = Result()

    try:
        stock = yf.Ticker(code)
        history = stock.history(period="1d")
        if history is None or history.shape is None or history.shape[0] < 1:
            result.message = "History show no data"
            result.success = False
            return result

        result.item = round(history.Close.iloc[-1], 2)
        result.success = True

    except Exception as e:
        result.message = str(e)

    return result


@sync_to_async
def get_current_stock_price_async(code: str) -> Result:
    return get_current_stock_price(code)


def get_year_stock_price(code: str, years=1) -> Result:
    result = Result()

    try:
        stock = yf.Ticker(code)
        history = stock.history(period=f"{years}y")
        if history is None or history.shape is None or history.shape[0] < 1:
            result.message = "History show no data"
            result.success = False
            return result

        result.item = history
        result.success = True

    except Exception as e:
        result.message = str(e)

    return result


def update_stock(stock: Stock, result: Result):
    stock.last_value = result.item
    stock.last_check_timestamp = time.time()
    stock.save()


def sync_stocks(stocks: StockList) -> StockList:
    if stocks is None:
        return []

    for stock in stocks:
        update_result = get_current_stock_price(stock.code)
        if update_result.success:
            update_stock(stock, update_result)

    return stocks


async def sync_stock_async(stock: Stock) -> Stock:
    if stock is None:
        return stock

    update_result = await get_current_stock_price_async(stock.code)
    if update_result.success:
        await sync_to_async(update_stock, thread_sensitive=True)(stock=stock, result=update_result)

    return stock
