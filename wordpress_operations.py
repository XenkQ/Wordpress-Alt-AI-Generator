import requests
import json

headers = {
    'Authorization': '',
    'Content-Type': 'application/json'
}

with open('credentials.json', 'r') as file:
    data = json.loads(file.read())['wordpress_mode_credentials']

    wordpress_media_endpoint = f"{data['wordpress_url']}/wp-json/wp/v2/media"
    username = data['username']
    password = data['password']

    headers['Authorization'] = 'Basic' + (username + ':' + password)


def can_connect_with_credentials() -> bool:
    if not username:
        return False

    response = requests.get(wordpress_media_endpoint, auth=(username, password))

    if response.status_code >= 500 and response.status_code <= 599:
        return False

    return True


def update_image_alt(media_id: int, alt_text: str):
    if not can_connect_with_credentials():
        return

    new_alt = {
        'alt_text': alt_text
    }

    url = f"{wordpress_media_endpoint}/{media_id}"

    requests.put(url=url, headers=headers, json=new_alt)
