import models_interactions
from sql_operations import *
import wordpress_operations
from image_utils import get_image_in_base64_text_from_url
import logger

__LOGO = r"""
     _    _   _____   ____  ____  _____ ____ ____  
    / \  | | |_   _| |  _ \|  _ \| ____/ ___/ ___| 
   / _ \ | |   | |   | |_) | |_) |  _| \___ \___ \ 
  / ___ \| |___| |   |  __/|  _ <| |___ ___) |__) |
 /_/   \_\_____|_|   |_|   |_| \_\_____|____/____/ 
"""

_YES_VARIANTS = ('yes', 'y', 'true')

print(__LOGO + "\n")

__mode = input("Connection Mode [0 - Database | 1 - Wordpress]: ")
__use_empty_alt_user_reply = input("Check for existing empty alt fields [yes | no]: ").lower()
__add_prefix_to_generated_alt_user_reply = input("Add prefix for image alt? [yes | no]: ").lower()

if not models_interactions.can_comminicate_with_ollama_api_end():
    print('\033[91m' + "Ollama server not connected or bad api endpoint url" + '\033[0m')
    logger.write_log("[Ollama Connection Error]", "Ollama server not connected or bad api endpoint url")
    exit(0)

__rows_to_change = []
__use_empty_alt = __use_empty_alt_user_reply in _YES_VARIANTS
__add_prefix_to_generated_alt = __add_prefix_to_generated_alt_user_reply in _YES_VARIANTS
__sql_operations = SQL_Operations()

if __mode == '0':
    if not __sql_operations.can_connect_to_database():
        print('\033[91m' + "Can't connect to database" + '\033[0m')
        logger.write_log("[Database Connection Error]", "Can't connect to database")
        exit(0)
    elif not __sql_operations.can_login_with_credentials():
        print('\033[91m' + "Can't use database with provided credentials" + '\033[0m')
        logger.write_log("[Database Credentials Error]", "Can't use database with provided credentials")
        exit(0)

    __rows_to_change = __sql_operations.get_data(GetDataOperations.IMAGE_IDS_LINKS_WITHOUT_ALT)

    if __use_empty_alt:
        __rows_to_change.extend(__sql_operations.get_data(GetDataOperations.IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW))
elif __mode == '1':
    if not wordpress_operations.can_connect_with_credentials():
        print('\033[91m' + "Can't use wordpress with provided credentials" + '\033[0m')
        logger.write_log("[Database Credentials Error]", "Can't use wordpress with provided credentials")
        exit(0)

    #TODO: Wordpress 

if len(__rows_to_change) == 0:
    print('\033[91m' + "Images to alter not found" + '\033[0m')
    logger.write_log("[Data base]", "Images to alter not found")
    exit(0)

alt_results = {}

print(f"Found {len(__rows_to_change)} images without alt")
print("-----------------------Generation Starts-----------------------\n")

print("---Alt text generation---")
for row in enumerate(__rows_to_change):
    model_response_text = models_interactions.get_image_alt_from_llava_model(get_image_in_base64_text_from_url(row[1]))

    model_response_text.title()

    logger.write_log(f"Alt id {row[0]} llava response: ", model_response_text)

    print(f"[{row[0]} Image] {row[1]}\n[Alt] {model_response_text}\n")

    alt_results[row[0]] = [row[1], model_response_text]

print("\n---Alt translation---")
for i, key in enumerate(alt_results):
    model_response_text_translated = models_interactions.translate_text_to_polish_with_bielik_model(
        alt_results[key][1]).title()

    logger.write_log(f"Alt id {key} bielik response:", model_response_text_translated)

    if __add_prefix_to_generated_alt:
        model_response_text_translated = "[AI] " + model_response_text_translated

    if __mode == '0':
        if __use_empty_alt:
            __sql_operations.change_data(key, model_response_text_translated, ChangeDataOperations.UPDATE_EXISTING_IMAGE_ALT_DATA)

        __sql_operations.change_data(key, model_response_text_translated, ChangeDataOperations.INSERT_ROW_WITH_IMAGE_ALT_DATA)
    elif __mode == '1':
        wordpress_operations.update_image_alt(key, model_response_text_translated)

    print(f"[{i + 1} Image] {alt_results[key][0]}\n[Alt in english] {alt_results[key][1]}\n"
          f"[Alt in polish] {model_response_text_translated}\n")

print("-----------------------Generation Ends-----------------------")

