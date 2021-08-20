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


def download_image(url, file_name, params = None):
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


def fetch_spacex_lunch(flight_number):
    spacex_url = "https://api.spacexdata.com/v4/launches/"
    spacex_template = "images/images_SPACEX/spacex{}.jpg"
    response = requests.get(spacex_url)
    response.raise_for_status()
    links = response.json()[flight_number]["links"]["flickr"]["original"]
    for filenumber, link in enumerate(links):
        file_name = spacex_template.format(filenumber)
        download_image(link, file_name)


def fetch_nasa_apod(token, images_quantity):
    nasa_endpoint = "https://api.nasa.gov/planetary/apod"
    nasa_apod_template = "images/images_NASA/{title}{ext}"
    params = {"api_key": token, "count": images_quantity}
    response = requests.get(nasa_endpoint, params=params)
    response.raise_for_status()
    image_descriptions = response.json()
    for image_description in image_descriptions:
        url = image_description["url"]
        title = image_description["title"]
        ext = get_extension(url)
        file_name = nasa_apod_template.format(title=title, ext=ext)
        download_image(url, file_name)


def fetch_nasa_epic(token):
    epic_endpoint = "https://api.nasa.gov/EPIC/api/natural/images"
    nasa_epic_template = "images/images_EPIC/{title}.png"
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
        file_name = nasa_epic_template.format(title=title)
        download_image(url, file_name, params=params)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("NASA_TOKEN")
    
    flight_number = random.randint(1,157)
    image_quantity = 30

    make_directory("./images/images_SPACEX")
    fetch_spacex_lunch(flight_number)
    make_directory("./images/images_NASA")
    fetch_nasa_apod(token,image_quantity)
    make_directory("./images/images_EPIC")
    fetch_nasa_epic(token)
