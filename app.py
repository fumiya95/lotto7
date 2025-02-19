import csv
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# ロト7の設定
LOTTO7_RANGE = range(1, 38)  # 1～37
LOTTO7_COUNT = 7

def load_past_data_from_csv(file_path):
    """
    CSVファイル (Loto 7 Results.csv) から
    '抽せん数字１'～'抽せん数字７' の出現回数をカウントして返す。
    戻り値: {数字: 出現回数, ...} の辞書
    """
    # 1～37 の数字をキーに、出現回数を0で初期化
    past_data = {i: 0 for i in range(1, 38)}
    
    # ※ CSVの文字コードに注意: "cp932", "utf-8", "utf-8-sig" など
    with open(file_path, 'r', encoding='cp932') as f:
        reader = csv.DictReader(f)
        
        # デバッグ: まずは取得したフィールド名を表示して確認
        print("==== CSV fieldnames ====")
        print(reader.fieldnames)
        print("========================")
        
        for row in reader:
            # 例: "抽せん数字１", "抽せん数字２" ... "抽せん数字７"
            for i in range(1, 8):
                column_name = f"抽せん数字{i}"  # CSVの列見出しに合わせる
                if column_name in row:
                    val = row[column_name]
                    try:
                        num = int(val)
                        if 1 <= num <= 37:
                            past_data[num] += 1
                    except ValueError:
                        # 数値に変換できなかったら無視
                        pass
    
    # デバッグ: カウント結果を一部表示
    print("==== Past Data (出現回数) ====")
    for k in sorted(past_data.keys()):
        print(f"数字 {k}: {past_data[k]} 回")
    print("================================")
    
    return past_data


def generate_random_lotto7():
    """
    完全ランダムに、重複なしで7つ選ぶ
    """
    return sorted(random.sample(LOTTO7_RANGE, LOTTO7_COUNT))


def generate_weighted_lotto7(past_data):
    """
    過去データを重みとして7つ選ぶ。
    多く出現している数字ほど選ばれやすいようにする。
    
    合計ウェイトが0 (=一度もカウントされなかった) の場合は
    ランダムにフォールバックする。
    """
    all_nums = list(LOTTO7_RANGE)
    weights = [past_data.get(num, 0) for num in all_nums]
    total_weights = sum(weights)
    
    if total_weights == 0:
        # すべて0なら ValueError が出るので、ランダムにフォールバック
        print("【警告】weightsの合計が0です。列名不一致orデータが空かもしれません。ランダム予想に切り替えます。")
        return generate_random_lotto7()
    
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
    予想ボタン押下時に呼ばれるエンドポイント
    """
    # フォームから mode を受け取り、ランダムか重み付きかを選択
    mode = request.form.get("mode", "random")

    # CSVファイルから過去出現回数をロード
    past_data = load_past_data_from_csv("Loto 7 Results.csv")

    # モードに応じて予想数字を生成
    if mode == "weighted":
        numbers = generate_weighted_lotto7(past_data)
    else:
        numbers = generate_random_lotto7()

    return render_template("index.html", predicted_numbers=numbers)


@app.errorhandler(404)
def not_found(e):
    """
    404 エラー時のハンドラ
    """
    return render_template("404.html"), 404


if __name__ == "__main__":
    # Flaskアプリを起動 (debug=True)
    app.run(debug=True)