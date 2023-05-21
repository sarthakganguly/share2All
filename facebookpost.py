from flask import Flask, request, jsonify
import facebook
import requests

app = Flask(__name__)

def share_url_with_image_as_post(url, message, image_url, token, tags):
    graph = facebook.GraphAPI(token)

    arrTags = tags.strip()

    strippedArrTags = arrTags.split(',')
    
    allTags = ['#' + eachTag.strip() for eachTag in strippedArrTags]

    allTagsInOne = ' '.join(allTags)

    print(allTagsInOne)

    message = message +' ' + url + ' ' +allTagsInOne

    try:
        post = graph.put_photo(image = open(image_url, 'rb'), message = message, published = False)
        return {'message': 'Post created successfully', 'post_id': post['id']}
    except facebook.GraphAPIError as e:
        return {'error': str(e)}

    # try:
    #     post = graph.put_object(parent_object='me', connection_name='feed', message = message, link = url, picture = image_url)
    #     return {'message': 'Post created successfully', 'post_id': post['id']}
    # except facebook.GraphAPIError as e:
    #     return {'error': str(e)}

@app.route('/fbpost', methods=['POST'])
def post(): 
    url = request.form.get('url')
    message = request.form.get('message')
    image_url = request.form.get('image_url')
    token = request.form.get('token')
    tags = request.form.get('tags')

    result = share_url_with_image_as_post(url, message, image_url, token, tags)
    return jsonify(result)

if __name__ == '__main__':
    app.run()
