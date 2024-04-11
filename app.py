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
        response = requests.post(SAGEMAKER_INFERENCE_ENDPOINT_URL, headers=headers, json=data)
        api_response_data = response.json()
        predicted_label = api_response_data["predicted_label"]
        return (render_template("index.html", result=predicted_label+" sentiment."))
    else:
        return (render_template("index.html", result="Please key in a financial text or tweet."))

@application.route("/financegpt", methods=["GET", "POST"])
def financegpt():
    if request.method == "POST" and request.form.get("tweet"):
        tweet = request.form.get("tweet")
        prompt = "Is this financial text a positive or negative sentiment: " + tweet
        result = palm.chat(**gpt_model, messages=prompt)
        return (render_template("financegpt.html", result=result.last))

    else:
        return (render_template("financegpt.html", result="Please key in a financial text or tweet."))

@application.route("/stockpriceanalyzer", methods=["GET", "POST"])
def stockpriceanalyzer():
    if request.method == "POST" and request.form.get("selected_symbol"):
        selected_symbol = request.form.get("selected_symbol").upper()
        alphavantage_api_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={selected_symbol}&outputsize=compact&apikey={ALPHAVANTAGE_API_KEY}'
        r = requests.get(alphavantage_api_url)
        data = r.json()
        symbol = data['Meta Data']['2. Symbol']
        last_30_days = {k: data['Time Series (Daily)'][k] for k in list(data['Time Series (Daily)'])[:30]}
        main_prompt = f'Given the last 30 traded days for {symbol} stock: [{last_30_days}], DO NOTE THAT the prices are most recent date first analyze the following:'
        prompt = main_prompt + analysis.analysis
        result = palm.chat(**gpt_model, messages=prompt)
        return (render_template("stockpriceanalyzer.html", result=result.last))
    else:
        return (render_template("stockpriceanalyzer.html", result="Please enter a stock symbol."))

@application.route("/end", methods=["GET", "POST"])
def end():
    if request.method == "POST":
        print(request.form)
        return render_template("end.html")
    
if __name__ == "__main__":
    application.run()
