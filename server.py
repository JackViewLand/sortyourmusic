import os
from flask import Flask, request, send_from_directory, jsonify, redirect, url_for
import json
import csv

# 啟動一個 Flask app，static_folder 指向 ./static
app = Flask(
    __name__,
    static_folder="static",
    static_url_path=""  # 讓 "/" 直接對應到 static
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FEATURE_DIR = os.path.join(BASE_DIR, "static", "database", "feature")
os.makedirs(FEATURE_DIR, exist_ok=True)


# 1) 首頁：直接回傳 static/index.html
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# 2) 上傳 CSV → 產生 feature.json
@app.route("/upload_feature", methods=["POST"])
def upload_feature():
    """
    接收一個 CSV 檔 (欄位格式是 Exportify 那種)，
    用檔名當 base name，產生同名 .json 並存到 static/database/feature
    """
    if "csv_file" not in request.files:
        return "缺少欄位 csv_file", 400

    csv_file = request.files["csv_file"]

    # 例如 "My_Social_2025.csv" → base_name = "My_Social_2025"
    original_name = csv_file.filename
    base_name = os.path.splitext(original_name)[0]
    json_name = base_name + ".json"
    json_path = os.path.join(FEATURE_DIR, json_name)

    raw = csv_file.read()
    try:
        # ✅ 用 utf-8-sig，自動吃掉開頭的 BOM (\ufeff)
        text = raw.decode("utf-8-sig")
    except Exception:
        text = raw.decode("utf-8", "ignore")

    reader = csv.DictReader(text.splitlines())
    features = {}

    def fnum(v):
        try:
            return float(v)
        except Exception:
            return 0.0

    def inum(v):
        try:
            return int(float(v))
        except Exception:
            return 0

    for row in reader:
        track_uri = row.get("Track URI")
        if not track_uri:
            continue

        # spotify:track:XXXXXXX → 取最後一段
        tid = track_uri.split(":")[-1]

        features[tid] = {
            "tempo":            fnum(row.get("Tempo", 0)),
            "energy":           fnum(row.get("Energy", 0)),
            "danceability":     fnum(row.get("Danceability", 0)),
            "valence":          fnum(row.get("Valence", 0)),
            "acousticness":     fnum(row.get("Acousticness", 0)),
            "instrumentalness": fnum(row.get("Instrumentalness", 0)),
            "liveness":         fnum(row.get("Liveness", 0)),
            "loudness":         fnum(row.get("Loudness", 0)),
            "duration_ms":      inum(row.get("Duration (ms)", 0)),
        }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(features, f, indent=2, ensure_ascii=False)

    return jsonify({
        "status": "success",
        "json_file": json_name,
        "stored_at": json_path,
        "tracks": len(features),
    })


if __name__ == "__main__":
    # 直接用 9000 port（你剛剛說想用 9000）
    print("🚀 Server running on http://localhost:9000")
    app.run(host="0.0.0.0", port=9000, debug=True)
