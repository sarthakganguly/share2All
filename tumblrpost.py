from io import BytesIO
from PIL import Image
from flask import Flask, request
from pytumblr import TumblrRestClient

app = Flask(__name__)

@app.route('/tumblrpost', methods=['POST'])
def post_to_tumblr():
    url = request.form.get('url')
    message = request.form.get('message')
    imagePath = request.form.get('image_url')
    urlName = request.form.get('urlName')
    blogName = request.form.get('blogName')
    tagsList = request.form.get('tags')         # ["testA", "testB", "testC"]
    statePost = request.form.get('state')       # "queue", "published", "draft"

    videoUrl = request.form.get('videoUrl')
    audioUrl = request.form.get('audioUrl')

    # Get Tumblr API credentials
    consumer_key = request.form.get('consumer_key')
    consumer_secret = request.form.get('consumer_secret')
    access_token = request.form.get('access_token')
    access_token_secret = request.form.get('access_token_secret')

    # Create a Tumblr client
    client = TumblrRestClient(
        consumer_key,
        consumer_secret,
        access_token,
        access_token_secret
    )

    message = message + ' ['+ urlName +']' + '(' + url + ')'

    response = ''

    arrTags = tagsList.split(',')

    try:
        if not (videoUrl):
            #Creates a photo post using a local filepath
            response = client.create_photo(blogName, state = statePost,
                                        tweet=message, format="markdown", tags=arrTags, 
                                        data=imagePath, caption ="##" + message)
            
        else:
            #Creating an upload from YouTube
            response = client.create_video(blogName, state = statePost, 
                                        tweet = message, format="markdown", tags = arrTags,
                                        embed=videoUrl, caption = "##" + message)
            
        return (str(response['id']) + ' ' + 'it worked!')
    except Exception as e:
        return (str(e))

if __name__ == '__main__':
    app.run()