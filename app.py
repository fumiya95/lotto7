# app.py
from flask import Flask, render_template, request
import random

app = Flask(__name__)

LOTTO7_RANGE = range(1, 38)
LOTTO7_COUNT = 7

def generate_random_lotto7():
    return sorted(random.sample(LOTTO7_RANGE, LOTTO7_COUNT))

@app.route("/")
def index():
    return render_template("index.html", predicted_numbers=None)

@app.route("/predict", methods=["POST"])
def predict():
    numbers = generate_random_lotto7()
    return render_template("index.html", predicted_numbers=numbers)

if __name__ == "__main__":
    app.run(debug=True)