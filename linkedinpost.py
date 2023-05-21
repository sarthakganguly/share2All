from flask import Flask, request, jsonify
from linkedin import linkedin

app = Flask(__name__)

@app.route("/linkedinpost", methods=["POST"])
def post_on_linkedin():
    access_token = request.form.get("access_token")
    title = request.form.get("title")
    text = request.form.get("text")
    url = request.form.get("url")
    preview_image = request.files.get("preview_image")

    if not access_token or not title or not text:
        return jsonify({"error": "Missing required parameters"}), 400

    success = post_content_on_linkedin(access_token, title, text, url, preview_image)
    if success:
        return jsonify({"message": "Content posted successfully on LinkedIn!"}), 200
    else:
        return jsonify({"error": "Failed to post content on LinkedIn"}), 500

def post_content_on_linkedin(access_token, title, text, url, preview_image):
    app = linkedin.LinkedInApplication(token=access_token)

    content = {
        "comment": text,
        "title": title,
        "submitted-url": url,
    }

    if preview_image:
        content["submitted-image-url"] = preview_image

    try:
        app.submit_share(content)
        return True
    except Exception as e:
        print(f"Error posting content on LinkedIn: {e}")
        return False

if __name__ == "__main__":
    app.run(debug=True)
