import csv
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# ロト7の定義
LOTTO7_RANGE = range(1, 38)  # 1～37
LOTTO7_COUNT = 7

# 例: ダミーデータ
PAST_DATA = {
    1: 15, 2: 22, 3: 3, 4: 18, 5: 9,
    # ... 全数字分の適当な値 ...
    37: 11
}

def load_past_data_from_csv(file_path):
    """
    CSVから過去データを読み込む関数（例）。
    1行目に「数字,出現回数」の形式で書かれている想定。
    """
    past_data = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            num, freq = int(row[0]), int(row[1])
            past_data[num] = freq
    return past_data

def generate_random_lotto7():
    """
    完全ランダムに重複なしで7つ選ぶ
    """
    return sorted(random.sample(LOTTO7_RANGE, LOTTO7_COUNT))

def generate_weighted_lotto7(past_data):
    """
    過去データ(PAST_DATAなど)を重みとして7つ選ぶ
    """
    all_nums = list(LOTTO7_RANGE)
    weights = [past_data.get(num, 1) for num in all_nums]
    selected = []
    while len(selected) < LOTTO7_COUNT:
        pick = random.choices(all_nums, weights=weights, k=1)[0]
        if pick not in selected:
            selected.append(pick)
    return sorted(selected)

@app.route("/")
def index():
    """
    トップページ: 予測前の画面を表示
    """
    return render_template("index.html", predicted_numbers=None)

@app.route("/predict", methods=["POST"])
def predict():
    """
    予測ボタンが押されたときに呼ばれる
    """
    # ここでは「完全ランダム生成」を例に使用
    # 必要に応じて generate_weighted_lotto7(PAST_DATA) に切り替える
    numbers = generate_random_lotto7()
    
    return render_template("index.html", predicted_numbers=numbers)

@app.errorhandler(404)
def not_found(e):
    """
    404 エラー時のハンドラ
    """
    return render_template("404.html"), 404

if __name__ == "__main__":
    # Flaskアプリをデバッグモードで起動
    app.run(debug=True)