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

    # 例: ダミーデータ
PAST_DATA = {
    1: 15, 2: 22, 3: 3, 4: 18, 5: 9,
    # ... 全数字分の適当な値 ...
    37: 11
}

def generate_weighted_lotto7(past_data):
    # 1～37をリスト化
    all_nums = list(LOTTO7_RANGE)
    # past_data から対応するweightを作成 (なければ1とか)
    weights = [past_data.get(num, 1) for num in all_nums]
    # 重み付きで7つサンプル
    selected = []
    while len(selected) < LOTTO7_COUNT:
        pick = random.choices(all_nums, weights=weights, k=1)[0]
        if pick not in selected:
            selected.append(pick)
    return sorted(selected)