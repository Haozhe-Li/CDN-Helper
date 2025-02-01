from flask import Flask, render_template, request, jsonify
import os
from core.upload import upload_to_cloudflare
from core.img_convert import convert_to_webp
# Initialize the Flask application
app = Flask(__name__)

# Define the home route
@app.route("/")
def home():
    """
    Render the home page.
    """
    return render_template("index.html")

# Define the route for converting GitHub URLs to jsDelivr URLs
@app.route("/api/convert-github", methods=["POST"])
def convert_github():
    """
    Convert a GitHub URL to a jsDelivr URL.
    Expects a JSON payload with a 'url' key.
    """
    url = request.json.get("url")

    # Validate the URL
    if url is None or not url.startswith("https://github.com"):
        return jsonify({"error": "Invalid GitHub URL"}), 400

    parts = url.split("/")
    if len(parts) < 7:
        return jsonify({"error": "Invalid GitHub URL"}), 400

    user = parts[3]
    repo = parts[4]
    branch = parts[6]
    file_path = "/".join(parts[7:])

    # Construct the jsDelivr URL
    jsdelivr_url = f"https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{file_path}"

    return jsonify({"convertedUrl": jsdelivr_url})

# Define the route for uploading files
@app.route("/api/upload", methods=["POST"])
def upload():
    """
    Upload a file to Cloudflare.
    Expects a file and a 'vipCode' in the form data.
    """
    file = request.files.get("file")
    vip = request.form.get("vipCode")
    autoConvert = request.form.get("autoConvert")

    if file is None or vip is None:
        return jsonify({"error": "File and VIP code are required"}), 400
    

    file_path = f"/tmp/{file.filename}" # no need for cleanup, as /tmp is cleared automatically on vercel
    file.save(file_path)

    if autoConvert is not None and autoConvert == "true":
        file_path = convert_to_webp(file_path)
        print("converted file to webp" + file_path)

    try:
        # Upload the file to Cloudflare
        file_url = upload_to_cloudflare(file_path=file_path, vipcode=vip)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"fileUrl": file_url})

# Run the application
if __name__ == "__main__":
    app.run(debug=True)