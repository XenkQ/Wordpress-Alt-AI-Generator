import requests

OLLAMA_SERVER_API_END_POINT = "http://10.0.3.8:11434/api/generate" #default local ollama api endpoint

PROMPT_CREATE_TEXT_FROM_IMAGE = """
Generate a vivid and detailed image header, up to 10 words, that clearly describes the main elements and essence of the image,
ensuring it provides enough context for someone who is visually impaired to visualize the scene.
"""

PROMPT_TRANSLATE_TEXT_TO_POLISH = """
Twoje zadanie to tłumaczenie textu. Wysyłaj tylko przetłumaczony tekst na język polski bez żadnego dodatkowego tekstu.
"%s"
"""

llava_params = {
    'model': 'llava:34b',
    'prompt': PROMPT_CREATE_TEXT_FROM_IMAGE,
    'stream': False,
    'images': []
}

bielik_params = {
    'model': 'mwiewior/bielik',
    'stream': False,
}


def can_comminicate_with_ollama_api_end() -> bool:
    response = requests.get(OLLAMA_SERVER_API_END_POINT)

    if response.status_code >= 500 and response.status_code <= 599:
        return False

    return True


def get_image_alt_from_llava_model(image_in_base64: str):
    llava_params['images'] = [image_in_base64]

    model_response = requests.post(OLLAMA_SERVER_API_END_POINT, json=llava_params)

    model_response.raise_for_status()

    return _get_model_reply_from_response(model_response)


def translate_text_to_polish_with_bielik_model(text: str):
    bielik_params['prompt'] = PROMPT_TRANSLATE_TEXT_TO_POLISH % text

    model_response = requests.post(OLLAMA_SERVER_API_END_POINT, json=bielik_params)

    model_response.raise_for_status()

    reply = _get_model_reply_from_response(model_response)

    reply = reply.replace("<s>  ", '') #replacing default bielik prefix

    return reply


def _get_model_reply_from_response(response) -> str:
    return str(response.json()['response']).replace('\n', ' ').replace('\"', '').strip()
