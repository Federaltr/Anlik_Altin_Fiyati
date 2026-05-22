from flask import Flask, render_template_string
import yfinance as yf
from datetime import datetime

app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <title>Federal Kuyumculuk Altın Fiyatları</title>

    <meta http-equiv="refresh" content="60">

    <style>
        body{
            font-family: Arial, sans-serif;
            background:#f2f2f2;
            margin:0;
            padding:40px;
        }

        .container{
            max-width:550px;
            margin:auto;
            background:white;
            border-radius:16px;
            padding:30px;
            box-shadow:0 5px 20px rgba(0,0,0,0.1);
        }

        h1{
            text-align:center;
            color:#222;
            margin-bottom:30px;
        }

        .box{
            background:#fafafa;
            border-radius:10px;
            padding:18px;
            margin-bottom:15px;
        }

        .title{
            color:#666;
            font-size:15px;
        }

        .value{
            font-size:28px;
            font-weight:bold;
            color:#111;
            margin-top:8px;
        }

        .gold{
            color:#b8860b;
        }

        .footer{
            margin-top:20px;
            font-size:13px;
            color:#666;
            text-align:center;
        }

        .refresh{
            text-align:center;
            margin-top:15px;
        }

        button{
            padding:10px 20px;
            border:none;
            border-radius:8px;
            background:#222;
            color:white;
            cursor:pointer;
            font-size:15px;
        }

        button:hover{
            background:#444;
        }
    </style>
</head>
<body>

<div class="container">

     <h1>Federal Kuyumculuk Altın Fiyatları</h1>

    <div class="box">
        <div class="title">Gram Altın</div>
        <div class="value gold">{{ gram }} TL</div>
    </div>

    <div class="box">
        <div class="title">Çeyrek Altın</div>
        <div class="value gold">{{ ceyrek }} TL</div>
    </div>

    <div class="box">
        <div class="title">Ons Altın</div>
        <div class="value">{{ ons }} USD</div>
    </div>

    <div class="box">
        <div class="title">USD / TRY</div>
        <div class="value">{{ usdtry }}</div>
    </div>

 

    <div class="refresh">
        <button onclick="window.location.reload();">
            Yenile
        </button>
    </div>

    <div class="footer">
        Son Güncelleme: {{ time }}
        <br><br>
        Hesaplama:
        <br>
        Gram = Ons × USDTRY / 31.1035
        <br>
        Çeyrek = Gram × 1.608

        Federal Kuyumculuk® All Rights Reserved. 2026
    </div>


</div>

</body>
</html>
"""

def get_price(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d", interval="1m")

    if data.empty:
        raise Exception(f"{symbol} verisi alınamadı")

    return float(data["Close"].dropna().iloc[-1])

@app.route("/")
def home():

    try:
        # Ons Altın
        ons = get_price("GC=F")

        # USDTRY
        usdtry = get_price("TRY=X")

        # Has gram altın
        gram = (ons * usdtry) / 31.1035

        # Çeyrek altın (has altın bazlı)
        ceyrek = gram * 1.608

        return render_template_string(
            HTML,
            ons=round(ons, 2),
            usdtry=round(usdtry, 4),
            gram=round(gram, 2),
            ceyrek=round(ceyrek, 2),
            time=datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        )

    except Exception as e:
        return f"Hata oluştu: {e}"

if __name__ == "__main__":
    app.run()
