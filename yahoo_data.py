import yfinance as yf


def get_market_data(symbol):


    ticker = yf.Ticker(symbol)

    history = ticker.history(period="5d")


    if len(history) < 2:
        return None

    latest = history.iloc[-1]
    previous = history.iloc[-2]

    return {
        "price": float(round(latest["Close"], 2)),
        "open": float(round(latest["Open"], 2)),
        "high": float(round(latest["High"], 2)),
        "low": float(round(latest["Low"], 2)),
        "change": float(round(latest["Close"] - previous["Close"], 2)),
        "change_pct": float(
            round(
                ((latest["Close"] - previous["Close"]) / previous["Close"]) * 100,
                2
            )
        ),
    }


    if len(history) < 2:
        return None

    latest = history.iloc[-1]
    previous = history.iloc[-2]

    return {
        "price": float(round(latest["Close"], 2)),
        "open": float(round(latest["Open"], 2)),
        "high": float(round(latest["High"], 2)),
        "low": float(round(latest["Low"], 2)),
        "change": float(round(latest["Close"] - previous["Close"], 2)),
        "change_pct": float(
            round(
                ((latest["Close"] - previous["Close"]) /
                 previous["Close"]) * 100,
                2
            )
        )
    }


def get_dxy_data():
    return get_market_data("DX-Y.NYB")