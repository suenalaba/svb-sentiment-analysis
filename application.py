import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
import google.generativeai as palm
import requests
import analysis

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
MAKERSUITE_API_KEY = os.getenv('MAKERSUITE_API_KEY')
SAGEMAKER_INFERENCE_ENDPOINT_URL = os.getenv('SAGEMAKER_INFERENCE_ENDPOINT_URL')

gpt_model = {
    "model": "models/chat-bison-001"
}
palm.configure(api_key=MAKERSUITE_API_KEY)

application = Flask(__name__)

@application.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and request.form.get("tweet"):
        tweet = request.form.get("tweet")
        data = {"inputs": tweet}
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(SAGEMAKER_INFERENCE_ENDPOINT_URL, headers=headers, json=data)
            api_response_data = response.json()
            predicted_label = api_response_data["predicted_label"]
            return (render_template("index.html", result={"sentiment": predicted_label+" sentiment.", "tweet": tweet}))
        except:
            return (render_template("index.html", result="Service currently unavailable, please try again later."))
    else:
        return (render_template("index.html", result="Please key in a financial text or tweet."))

@application.route("/financegpt", methods=["GET", "POST"])
def financegpt():
    if request.method == "POST" and request.form.get("tweet"):
        tweet = request.form.get("tweet")
        prompt = analysis.stock_sentiment_analysis + tweet
        result = palm.chat(**gpt_model, messages=prompt)
        return (render_template("financegpt.html", result={"sentiment": result.last, "tweet": tweet}))

    else:
        return (render_template("financegpt.html", result="Please key in a financial text or tweet."))

@application.route("/stockpriceanalyzer", methods=["GET", "POST"])
def stockpriceanalyzer():
    if request.method == "POST" and request.form.get("selected_symbol"):
        try:
            selected_symbol = request.form.get("selected_symbol").upper()
            alphavantage_api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={selected_symbol}&outputsize=compact&apikey={ALPHAVANTAGE_API_KEY}'
            r = requests.get(alphavantage_api_url)
            data = r.json()
            symbol = data['Meta Data']['2. Symbol']
            last_30_days = {k: data['Time Series (Daily)'][k] for k in list(data['Time Series (Daily)'])[:30]}
            last_30_days_tabular = "Date\tOpen\tHigh\tLow\tClose\tVolume\n"  # Header row
            for date, values in last_30_days.items():
                last_30_days_tabular += f"{date}\t{values['1. open']}\t{values['2. high']}\t{values['3. low']}\t{values['4. close']}\t{values['5. volume']}\n"
            main_prompt = f'I have the last 30 trading days of {symbol} stock data including open, high, low, close, and volume. Please provide a detailed technical analysis, covering:'
            sub_prompt = f'The stock data is as follows: \n{last_30_days_tabular}'
            prompt = f'{main_prompt}\n {analysis.stock_price_analysis}\n {sub_prompt}'
            result = palm.chat(**gpt_model, messages=prompt)
            return (render_template("stockpriceanalyzer.html", result={"analysis": result.last, "symbol": symbol}))
        except:
            return (render_template("stockpriceanalyzer.html", result="Please enter a valid stock symbol."))
    else:
        return (render_template("stockpriceanalyzer.html", result="Please enter a stock symbol."))

@application.route("/end", methods=["GET", "POST"])
def end():
    if request.method == "POST":
        print(request.form)
        return render_template("end.html")
    
if __name__ == "__main__":
    application.run()
