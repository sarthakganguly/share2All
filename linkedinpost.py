from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SHARES_API = "https://api.linkedin.com/v2/shares"

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
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    payload = {
        "author": f"urn:li:person:{access_token}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text,
                },
                "shareMediaCategory": "ARTICLE",
                "media": [],
            },
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
        },
    }

    if url:
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "ARTICLE"
        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"].append({
            "status": "READY",
            "originalUrl": url,
            "title": {
                "text": title,
            },
        })

    if preview_image:
        image_data = preview_image.read()
        response = requests.post(
            "https://api.linkedin.com/v2/assets?action=registerUpload",
            headers=headers,
            json={"registerUploadRequest": {"recipes": ["urn:li:digitalmediaRecipe:feedshare-image"]}},
        )
        response_data = response.json()
        asset = response_data.get("value").get("asset")
        upload_url = response_data.get("value").get("uploadMechanism").get("com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest").get("uploadUrl")

        headers["Content-Type"] = "application/octet-stream"
        response = requests.put(upload_url, headers=headers, data=image_data)
        response.raise_for_status()

        payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"].append({
            "media": asset,
        })

    try:
        response = requests.post(SHARES_API, headers=headers, json=payload)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error posting content on LinkedIn: {e}")
        return False

if __name__ == "__main__":
    app.run(debug=True)
