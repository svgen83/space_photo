import datetime
import os
import pathlib
import random
from urllib.parse import urlsplit
from urllib.parse import unquote

import requests
from dotenv import load_dotenv


def make_directory(image_folder):
    pathlib.Path(image_folder).mkdir(parents=True, exist_ok=True)


def download_image(url, file_name, params=None):
    response = requests.get(url, params)
    response.raise_for_status()
    with open(file_name, "wb") as file:
        file.write(response.content)


def get_extension(url):
    unquoted_url = unquote(url)
    splitted_url = urlsplit(unquoted_url)
    splitted_url_path = os.path.splitext(splitted_url.path)
    extension = splitted_url_path[1]
    return extension


def fetch_spacex_lunch(flight_number, image_folder, file_name_template):
    spacex_url = "https://api.spacexdata.com/v4/launches/"
    
    response = requests.get(spacex_url)
    response.raise_for_status()
    links = response.json()[flight_number]["links"]["flickr"]["original"]

    for filenumber, link in enumerate(links):
        file_name = file_name_template.format(filenumber)
        download_image(link, file_name)


def fetch_nasa_apod(token, image_folder, file_name_template, images_quantity):
    nasa_endpoint = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": token, "count": images_quantity}
    
    response = requests.get(nasa_endpoint, params=params)
    response.raise_for_status()
    image_descriptions = response.json()

    for image_description in image_descriptions:
        url = image_description["url"]
        title = image_description["title"]
        ext = get_extension(url)
        file_name = file_name_template.format(title, ext)
        download_image(url, file_name)


def fetch_nasa_epic(token, image_folder, file_name_template):
    epic_endpoint = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": token}
    
    response = requests.get(epic_endpoint, params=params)
    response.raise_for_status()
    image_descriptions = response.json()
    image_endpoint = "https://api.nasa.gov/EPIC/archive/natural/{file_date}/png/{title}.png"

    for image_description in image_descriptions:
        title = image_description["image"]
        image_date = image_description["date"]
        date_time = datetime.datetime.fromisoformat(image_date)
        file_date = date_time.strftime("%Y/%m/%d")
        url = image_endpoint.format(file_date=file_date, title=title)
        file_name = file_name_template.format(title)
        download_image(url, file_name, params=params)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("NASA_TOKEN")
    
    flight_number = random.randint(1,157)
    image_quantity = 30
    
    spacex_folder = "./images/images_SPACEX/"
    nasa_folder = "./images/images_NASA/"
    epic_folder = "./images/images_EPIC/"

    spacex_template = "images/images_SPACEX/spacex{}.jpg"
    nasa_apod_template = "images/images_NASA/{0}{1}"
    nasa_epic_template = "images/images_EPIC/{}.png"

    make_directory(spacex_folder)
    fetch_spacex_lunch(flight_number, spacex_folder, spacex_template)
    make_directory(nasa_folder)
    fetch_nasa_apod(token,nasa_folder, nasa_apod_template, image_quantity)
    make_directory(epic_folder)
    fetch_nasa_epic(token, epic_folder, nasa_epic_template)
