from flask import Flask, request
from pinterest import Pinterest

app = Flask(__name__)

# access token - pina_AMA5PMAWACOFOAQAGAAOSDRKGLFBTCABACGSPJ4YFTD3N5ORWVP3M5YP2WXEOP7CAM34KDHFQW4W4U5HNA35GLMV377H23AA

@app.route('/pinterestpin', methods=['POST'])
def pin_to_pinterest():
    url = request.form.get('url')
    message = request.form.get('message')
    image_file = request.files.get('image')

    # Pinterest API credentials
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'
    access_token = 'your_access_token'

    # Create a Pinterest API client
    pinterest = Pinterest(client_id=client_id, client_secret=client_secret, access_token=access_token)

    # Upload image to Pinterest
    image_url = pinterest.upload_pin_image(image_file)

    # Create pin
    pin_data = {
        'board': 'your_board_id',  # Replace with your board ID
        'note': message,
        'link': url,
        'image_url': image_url,
    }

    response = pinterest.create_pin(**pin_data)

    if response['status'] == 'success':
        return 'Pin successful!'
    else:
        return 'Error occurred while pinning to Pinterest.'

if __name__ == '__main__':
    app.run()
