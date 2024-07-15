import models_interactions
import sql_operations
from image_utils import get_image_in_base64_text_from_url
import logger

LOGO = r"""
     _    _   _____   ____  ____  _____ ____ ____  
    / \  | | |_   _| |  _ \|  _ \| ____/ ___/ ___| 
   / _ \ | |   | |   | |_) | |_) |  _| \___ \___ \ 
  / ___ \| |___| |   |  __/|  _ <| |___ ___) |__) |
 /_/   \_\_____|_|   |_|   |_| \_\_____|____/____/ 
"""

YES_VARIANTS = ('yes', 'y', 'true')

print(LOGO + "\n")

mode = input("Connection Mode [0 - Database | 1 - Wordpress]: ")
use_empty_alt = input("Check for existing empty alt fields [yes | no]: ").lower()
add_prefix_to_generated_alt = input("Add prefix for image alt? [yes | no]: ").lower()

if not models_interactions.can_comminicate_with_ollama_api_end():
    print('\033[91m' + "Ollama server not connected or bad api endpoint url" + '\033[0m')
    logger.write_log("[Ollama Connection Error]", "Ollama server not connected or bad api endpoint url")
    exit(0)

if not sql_operations.can_connect_to_database():
    print('\033[91m' + "Can't connect to database" + '\033[0m')
    logger.write_log("[Database Connection Error]", "Can't connect to database")
    exit(0)

# if not sql_operations.can_login_with_credentials():
#     print('\033[91m' + "Can't use database with provided credentials" + '\033[0m')
#     logger.write_log("[Database Credentials Error]", "Can't use database with provided credentials")
#     exit(0)

rows_to_change = sql_operations.get_data(sql_operations.GetDataOperations.IMAGE_IDS_LINKS_WITHOUT_ALT)
alt_results = {}

if use_empty_alt in YES_VARIANTS:
    rows_to_change.extend(sql_operations.get_data(sql_operations.GetDataOperations.IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW))

if len(rows_to_change) == 0:
    print('\033[91m' + "Images to alter not found" + '\033[0m')
    logger.write_log("[Data base]", "Images to alter not found")
    exit(0)

if mode == '0':
    print(f"Found {len(rows_to_change)} images without alt")
    print("-----------------------Generation Starts-----------------------\n")

    print("---Alt text generation---")
    for i, row in enumerate(rows_to_change):
        model_response_text = models_interactions.get_image_alt_from_llava_model(get_image_in_base64_text_from_url(row[1]))

        model_response_text.title()

        logger.write_log(f"Alt id {i} llava response: ", model_response_text)

        print(f"[{i + 1} Image] {row[1]}\n[Alt] {model_response_text}\n")

        alt_results[i] = [row[1], model_response_text]

    print("\n---Alt translation---")
    for i, key in enumerate(alt_results):
        model_response_text_translated = models_interactions.translate_text_to_polish_with_bielik_model(alt_results[key][1]).title()

        if add_prefix_to_generated_alt in YES_VARIANTS:
            model_response_text_translated = "[AI]" + model_response_text_translated

        logger.write_log(f"Alt id {key} bielik response:", model_response_text_translated)

        sql_operations.change_data(key, model_response_text_translated, sql_operations.ChangeDataOperations.UPDATE_EXISTING_IMAGE_ALT_DATA)

        print(f"[{i + 1} Image] {alt_results[key][0]}\n[Alt in english] {alt_results[key][1]}\n[Alt in polish] {model_response_text_translated}\n")

    print("-----------------------Generation Ends-----------------------")

elif mode == '1':
    #TODO: add worpdress api connection
    pass