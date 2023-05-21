from flask import Flask, request, jsonify
import tweepy

app = Flask(__name__)

def post_tweet(message, consumer_key, consumer_secret, access_token, access_token_secret):
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    try:
        api.update_status(message)
        return {'message': 'Tweet posted successfully'}
    except tweepy.TweepError as e:
        return {'error': str(e)}

@app.route('/tweet', methods=['POST'])
def tweet():
    message = request.form.get('message')
    consumer_key = "g5thavUL7YqN0oMVeeCSfqDxg"
    consumer_secret = 'PREHV5uwLniZAZfgZMbEKStUZYpXsHHnSsOIpd4a1K5JntrhAo'
    access_token = '75488021-PYqIM4tyYAi6SkbeUa7dxKtiTfTfbFE51yCmUAs7g'
    access_token_secret = 'N1OTICrc6cJWeFaBrSP02j1QxyPlF7NiHCtxu0NrSDjy4'

    result = post_tweet(message, consumer_key, consumer_secret, access_token, access_token_secret)
    return jsonify(result)

if __name__ == '__main__':
    app.run()


# Consumer API Key - g5thavUL7YqN0oMVeeCSfqDxg
# Consumer API Key Secret - PREHV5uwLniZAZfgZMbEKStUZYpXsHHnSsOIpd4a1K5JntrhAo
# Bearer token - AAAAAAAAAAAAAAAAAAAAAMwnBgEAAAAAf3Lw9MavP8f6Y6PFXBydIYXwON8%3D6m85ujoyqR0WCws3iJ8OtbsPCkQWWOyUncPnInzmFCvkWUVat7
# Access Token - 75488021-PYqIM4tyYAi6SkbeUa7dxKtiTfTfbFE51yCmUAs7g
# Access Token Secret - N1OTICrc6cJWeFaBrSP02j1QxyPlF7NiHCtxu0NrSDjy4
# Oauth 2 client id - d1lUdFRmT2JhWE9IQzNpV1U2Wmk6MTpjaQ
# Oauth 2 client secret - sGFNTKEL7MJkBKo3fWu1Iw4f8yjK686JNb1-eaNMxJCZhwsxP_