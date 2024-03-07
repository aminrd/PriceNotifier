import time

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


def sync_stocks(stocks: StockList) -> StockList:
    if stocks is None:
        return []

    for stock in stocks:
        update_result = get_current_stock_price(stock.code)
        if update_result.success:
            stock.last_value = update_result.item
            stock.last_check_timestamp = time.time()
            stock.save()

    return stocks
