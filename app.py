from flask import Flask, render_template, request, jsonify
import os
from core.upload import upload_to_cloudflare

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/convert-github", methods=["POST"])
def convert_github():
    url = request.json["url"]

    if url is None or not url.startswith("https://github.com"):
        return jsonify({"error": "Invalid GitHub URL"}), 400

    # 解析 GitHub URL
    parts = url.split("/")
    if len(parts) < 7:
        return jsonify({"error": "Invalid GitHub URL"}), 400

    user = parts[3]
    repo = parts[4]
    branch = parts[6]
    file_path = "/".join(parts[7:])

    # 转换为 jsDelivr URL
    jsdelivr_url = f"https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{file_path}"

    return jsonify({"convertedUrl": jsdelivr_url})


@app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    vip = request.form["vipCode"]
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    file_path = f"/tmp/{file.filename}"
    file.save(file_path)
    try:
        file_url = upload_to_cloudflare(file_path=file_path, vipcode=vip)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    try:
        # clear everything
        os.remove(file_path)
    except Exception as e:
        print(f"Failed to remove file: {str(e)}")
    return jsonify({"fileUrl": file_url})


if __name__ == "__main__":
    app.run(debug=True)
