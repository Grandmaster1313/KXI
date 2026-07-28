import yfinance as yf

print("Downloading DXY...\n")

dxy = yf.Ticker("DX-Y.NYB")

history = dxy.history(period="5d")

print("===== DATA RECEIVED =====")
print(history)

print("\nNumber of rows:", len(history))

if len(history) > 0:
    latest = history.iloc[-1]

    print("\nLatest Data")
    print("Open :", latest["Open"])
    print("High :", latest["High"])
    print("Low  :", latest["Low"])
    print("Close:", latest["Close"])