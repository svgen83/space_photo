import telegram
import time
import os
from dotenv import load_dotenv


if __name__ == "__main__":
            
    load_dotenv()
    token = os.getenv("TELEGRAM_TOKEN")
    bot = telegram.Bot(token=token)
    channel_chat_id = "@space_gen"
    image_directory = "images"
    space_images_pathes = []
    for root, dirs, files in os.walk(image_directory, topdown=False):
        for name in files:
            space_images_path = os.path.join(root, name)
            space_images_pathes.append(space_images_path)
    print(space_images_pathes)
    while True:
        for space_images_path in space_images_pathes:
            if os.path.getsize(space_images_path)>0:
                bot.send_photo(chat_id=channel_chat_id,photo=open(space_images_path, 'rb'))
            time.sleep(86400)
   
