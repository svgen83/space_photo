import datetime
import os
import pathlib
import random
from urllib.parse import urlsplit
from urllib.parse import unquote

import requests
from dotenv import load_dotenv



def make_directory(path_name):
    pathlib.Path(path_name).mkdir(parents=True, exist_ok=True)

def get_image(url, file_name, params = None):
    response = requests.get(url, params)
    response.raise_for_status()
    with open(file_name, 'wb') as file:
        file.write(response.content)


def get_extension(url):
    unquoted_url = unquote(url)
    splitted_url = urlsplit(unquoted_url)
    splitted_url_path = os.path.splitext(splitted_url.path)
    extension = splitted_url_path[1]
    return extension


def fetch_spacex_lunch(flight_number, template_name, get_image):
    spacex_url = "https://api.spacexdata.com/v4/launches/"
    response = requests.get(spacex_url)
    response.raise_for_status()
    links = response.json()[flight_number]["links"]["flickr"]["original"]
    for filenumber, link in enumerate(links):
        file_name = spacex_template_name.format(filenumber)
        get_image(link, file_name)

        
def fetch_nasa_apod(token, images_quantity, template_name, get_image, get_extension):
    nasa_endpoint = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": token, "count": images_quantity}
    response = requests.get(nasa_endpoint, params=params)
    response.raise_for_status()
    image_descriptions = response.json()
    for image_description in image_descriptions:
        url = image_description["url"]
        title = image_description["title"]
        ext = get_extension(url)
        file_name = nasa_apod_template_name.format(title=title, ext=ext)
        get_image(url, file_name)


def fetch_nasa_epic(token, template_name, get_image):
    epic_endpoint = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": token}
    response = requests.get(epic_endpoint, params=params)
    response.raise_for_status()
    image_descriptions = response.json()
    image_endpoint = "https://api.nasa.gov/EPIC/archive/natural/{file_date}/png/{title}.png"
    for image_description in image_descriptions:
        title = image_description["image"]
        image_date = image_description["date"]
        a_date_time = datetime.datetime.fromisoformat(image_date)
        file_date = a_date_time.strftime("%Y/%m/%d")
        url = image_endpoint.format(file_date=file_date, title=title)
        file_name = nasa_epic_template_name.format(title=title)
        get_image(url, file_name, params=params)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("NASA_TOKEN")
    
    flight_number = random.randint(1,157)
    images_quantity = 30

    spacex_path_name = './images/images_SPACEX'
    nasa_apod_path_name = './images/images_NASA'
    nasa_epic_path_name = './images/images_EPIC'

    spacex_template_name = "images/images_SPACEX/spacex{}.jpg"
    nasa_apod_template_name = "images/images_NASA/{title}{ext}"
    nasa_epic_template_name = "images/images_EPIC/{title}.png"

    make_directory(spacex_path_name)
    fetch_spacex_lunch(flight_number, spacex_template_name, get_image)
    make_directory(nasa_apod_path_name)
    fetch_nasa_apod(token,images_quantity, nasa_apod_template_name, get_image, get_extension)
    make_directory(nasa_epic_path_name)
    fetch_nasa_epic(token,nasa_epic_template_name, get_image)
    
    
