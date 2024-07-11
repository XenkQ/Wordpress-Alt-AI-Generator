import requests
import base64

def get_image_in_base64_text_from_url(url: str) -> str:
    res = requests.get(url)
    res.raise_for_status()

    base64_data = res.content

    base64_bytes = base64.encodebytes(base64_data)

    return base64_bytes.decode('ascii')
