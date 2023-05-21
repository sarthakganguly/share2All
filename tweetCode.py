from flask import Flask, request, jsonify
import tweepy
from io import BytesIO
from PIL import Image
import requests

app = Flask(__name__)

def post_tweet(url, message, image_url, consumer_key, consumer_secret, access_token, access_token_secret):

    print (url)
    print (message)
    print (image_url)
    print (consumer_key)
    print (consumer_secret)
    print (access_token)
    print (access_token_secret)

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # Download the image
    image_data = Image.open(image_url)

    # Save image in-memory
    b = BytesIO()
    image_data.save(b, "PNG")
    b.seek(0)

    # Upload the image to Twitter
    media_upload = api.media_upload(filename='image.png', file=b)

    print (media_upload)

    # Create the tweet with the URL, text, and attached media
    tweet_text = f"{message}\n{url}"
    
    tweet = api.update_status(status=tweet_text, media_ids=[media_upload.media_id])
    #tweet = api.update_status(status=tweet_text)
    
    return {'message': 'Tweet posted successfully', 'tweet_id': tweet.id_str}

@app.route('/tweeturl', methods=['POST'])
def tweet():
    
    url = request.form.get('url')
    message = request.form.get('message')
    image_url = request.form.get('image_url')

    consumer_key= request.form.get('consumer_key')
    consumer_secret= request.form.get('consumer_secret')
    access_token= request.form.get('access_token')
    access_token_secret= request.form.get('access_token_secret')

    try:
        result = post_tweet(url, message, image_url, consumer_key, consumer_secret, access_token, access_token_secret)
        return jsonify(result)
    except Exception as e:
        return (str(e))

if __name__ == '__main__':
    app.run()
