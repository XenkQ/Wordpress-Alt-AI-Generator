import datetime

LOG_FILE_PATH = r"log.txt"

def write_log(context: str, text: str):
    with open(LOG_FILE_PATH, 'a', encoding='utf-8') as file:
        curr_time = datetime.datetime.now().strftime("%H:%M:%S")
        file.write(f"[{curr_time}] {context} {text}\n")
