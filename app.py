# flask --app app run
# http://127.0.0.1:5000

from flask import Flask, render_template, request

from nltk.metrics.distance import edit_distance # Levenshtein
from nltk.translate import bleu # BLEU

# before loading BERTScore (and necessary Huggingface libraries), 
# need to set up environment variables to access locally saved model & don't attempt to download
import os
os.environ["HUGGINGFACE_HUB_CACHE"] = os.path.join(os.getcwd(), "static")
os.environ["TRANSFORMERS_OFFLINE"] = "1"

# required for BERTScore (https://help.pythonanywhere.com/pages/MachineLearningInWebsiteCode/)
import torch
torch.set_num_threads(1)

from bert_score import BERTScorer
scorer = BERTScorer(model_type="t5-small") 
# use a smaller model than BERT that fits in limited online storage and increases speed


app = Flask(__name__)

def calc_metrics(text1=None, text2=None):
    # calls all the separate metric functions
    # returns a dict with results
    metrics = {}

    # Levenshtein
    metrics["Levenshtein"] = edit_distance(text1, text2)
    
    # BLEU
    metrics["BLEU"] = bleu([text1.split()], text2.split())

    # BERTScore
    P, R, F1 = scorer.score([text1], [text2])
    metrics["BERTScore"] = F1.item()
    
    # - other metrics
    # - make metrics.html receive a dictionary in JSON & loop through it
    # - apply optional text preprocessing to text1/2 (lower case, remove punctuation)

    return metrics


@app.route("/calc", methods=['POST'])
def calc():
    text1 = request.form["text1"]
    text2 = request.form["text2"]

    # calculate the metrics here, change later
    metrics = calc_metrics(text1, text2) # escape(text1) ? # from markupsafe import escape

    return render_template('metrics.html', metrics=metrics)


@app.route("/") # http://127.0.0.1:5000
def hello():
    return render_template('index.html')

