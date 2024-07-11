import models_interactions
import sql_operations
from image_utils import get_image_in_base64_text_from_url
import logger

mode = input("Connection Mode [0 - Database | 1 - Wordpress]: ")
use_empty_alt = input("Check for existing empty alt fields [yes | no]: ").lower()

rows_to_change = sql_operations.get_data(sql_operations.GetDataOperations.IMAGE_IDS_LINKS_WITHOUT_ALT)

if use_empty_alt == 'yes' or use_empty_alt == 'y':
    rows_to_change.extend(sql_operations.get_data(sql_operations.GetDataOperations.IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW))

if mode == '0':
    print(f"Found {len(rows_to_change)} images without alt")
    print("-----------------------Generation Starts-----------------------")

    for i, row in enumerate(rows_to_change):
        model_response_text = models_interactions.get_image_alt_from_llava_model(get_image_in_base64_text_from_url(row[1]))
        logger.write_log(f"Row {i} llava response: ", model_response_text)

        model_response_text_translated = models_interactions.translate_text_to_polish_with_bielik_model(model_response_text)
        logger.write_log(f"Row {i} bielik response:", model_response_text_translated)

        sql_operations.change_data(row[0], model_response_text_translated, sql_operations.ChangeDataOperations.UPDATE_EXISTING_IMAGE_ALT_DATA)

        print(f"{i + 1} Image: {row[1]}\nAlt from image in english: {model_response_text}\nAlt polish translation: {model_response_text_translated}")

    print("-----------------------Generation Ends-----------------------")

elif mode == '1':
    #TODO: add worpdress api connection
    pass