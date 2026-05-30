from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)


def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    name = info.get("shortName") or info.get("longName") or "查無股票名稱"
    price = None

    try:
        price = stock.fast_info.get("last_price")
    except Exception:
        price = None

    if price is None:
        price = info.get("regularMarketPrice") or info.get("currentPrice")

    return {
        "symbol": symbol,
        "name": name,
        "price": price if price is not None else "查無最新股價",
    }


@app.route("/", methods=["GET", "POST"])
def index():
    stock_data = None
    error = None

    if request.method == "POST":
        symbol = request.form.get("symbol", "").strip().upper()

        if symbol:
            try:
                stock_data = get_stock_data(symbol)
            except Exception:
                error = "查詢失敗，請確認股票代號是否正確。"
        else:
            error = "請輸入股票代號。"

    return render_template("index.html", stock_data=stock_data, error=error)


if __name__ == "__main__":
    app.run(debug=True)
