# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

# 数字範囲や個数の定義
LOTTO7_RANGE = range(1, 38)  # 1～37
LOTTO7_COUNT = 7

import random

def generate_random_lotto7():
    # 1～37の中から重複しない7つの数字をランダムに選ぶ
    return sorted(random.sample(LOTTO7_RANGE, LOTTO7_COUNT))