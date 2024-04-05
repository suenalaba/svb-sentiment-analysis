import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
import google.generativeai as palm
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

load_dotenv()

MAKERSUITE_API_KEY = os.getenv('MAKERSUITE_API_KEY')

gpt_model = {
    "model": "models/chat-bison-001"
}
palm.configure(api_key=MAKERSUITE_API_KEY)

app = Flask(__name__)

def get_custom_prediction(model, tokenizer, text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # Move the inputs to the same device as the model
    inputs = {k: v.to(model.device) for k, v in inputs.items()}

    # Make the prediction
    with torch.no_grad():
        outputs = model(**inputs)
        prediction = outputs.logits.argmax(dim=-1).item()

    predicted_label = model.config.id2label[prediction]

    return predicted_label

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST" and request.form.get("tweet"):
        tweet = request.form.get("tweet")
        model_dir = "model_config"
        loaded_model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        loaded_tokenizer = AutoTokenizer.from_pretrained(model_dir)
        sentiment_output = get_custom_prediction(loaded_model, loaded_tokenizer, tweet)
        # tokenizer = AutoTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
        # finbert_model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
        # inputs = tokenizer(tweet, return_tensors="pt")
        # outputs = finbert_model(**inputs)
        # logits = outputs.logits
        # predicted_class_id = logits.argmax(-1).item()
        # predicted_class_label = finbert_model.config.id2label[predicted_class_id] 
        # return (render_template("index.html", result=predicted_class_label.upper()))
        return (render_template("index.html", result=sentiment_output.upper()))
    else:
        return (render_template("index.html", result="Please key in a financial text or tweet."))

@app.route("/financegpt", methods=["GET", "POST"])
def financegpt():
    if request.method == "POST" and request.form.get("tweet"):
        tweet = request.form.get("tweet")
        prompt = "Is this financial text a positive or negative sentiment: " + tweet
        result = palm.chat(**gpt_model, messages=prompt)
        return (render_template("financegpt.html", result=result.last))

    else:
        return (render_template("financegpt.html", result="Please key in a financial text or tweet."))

@app.route("/end", methods=["GET", "POST"])
def end():
    if request.method == "POST":
        print(request.form)
        return render_template("end.html")
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)