import requests
import base64


def get_image_in_base64_text_from_url(url: str) -> str:
    """
    Get image in base64 string from url

    >>> get_image_in_base64_text_from_url(r"https://pl.wikipedia.org/wiki/testtest.jpg")
    ''
    >>> get_image_in_base64_text_from_url(r"https://leba.eu/pl/wp-content/uploads/2024/07/przetarg-2.jpg")
    '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'
    """

    res = requests.get(url)

    if 400 <= res.status_code <= 599:
        return ''

    base64_data = res.content

    base64_bytes = (base64.encodebytes(base64_data)
                    .decode('ascii')
                    .replace('\n', ''))

    return base64_bytes
