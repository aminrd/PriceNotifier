import yfinance as yf
from common_variables import *

def get_current_stock_price(code:str) -> Result:
    result = Result()

    try:
        stock = yf.Ticker(code)
        history = stock.history(period="1h")
        if history is None or history.shape is None or history.shape[0] < 1:
            return result

        result.value = history.Close.iloc[-1]
        result.success = True

    except Exception as e:
        result.message = str(e)

    return result