import requests
import pathlib
import os.path
import os
from urllib.parse import urlsplit
from urllib.parse import unquote
import datetime
from dotenv import load_dotenv


def get_image(url, filename):
    response = requests.get(url)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def fetch_spacex_lunch(get_image=get_image):
    pathlib.Path('./images/images_SPACEX').mkdir(parents=True, exist_ok=True)
    spacex_url = "https://api.spacexdata.com/v4/launches/"
    flight_number = 118
    response = requests.get(spacex_url)
    response.raise_for_status()
    links = response.json()[flight_number]["links"]["flickr"]["original"]
    for filenumber, link in enumerate(links):
        filename = "images/images_SPACEX/spacex{}.jpg".format(filenumber)
        get_image(link, filename)


def get_extencion(url):
    u = unquote(url)
    split_url_result = urlsplit(u)
    split_path_result = os.path.split(split_url_result.path)
    split_name_results = os.path.splitext(split_path_result[1])
    extencion = split_name_results[1]
    return extencion


def fetch_nasa_apod(get_image=get_image, get_extencion=get_extencion):
    pathlib.Path('./images/images_NASA').mkdir(parents=True, exist_ok=True)
    nasa_endpoint = "https://api.nasa.gov/planetary/apod"
    images_quantity = 50
    params = {"api_key": token, "count": images_quantity}
    response = requests.get(nasa_endpoint, params=params)
    response.raise_for_status
    image_descriptions = response.json()
    image_urls = []
    for image_description in image_descriptions:
        image_url = image_description["url"], image_description["title"]
        image_urls.append(image_url)
    for image_url in image_urls:
        url, title = image_url
        ext = get_extencion(url)
        if ext != None:
            filename = "images/images_NASA/{title}{ext}".format(title=title, ext=ext)
            get_image(url, filename)


def fetch_nasa_epic(get_image=get_image):
    pathlib.Path('./images/images_EPIC').mkdir(parents=True, exist_ok=True)
    epic_endpoint = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {"api_key": token}
    response = requests.get(epic_endpoint, params=params)
    response.raise_for_status
    image_descriptions = response.json()
    image_endpoint = "https://api.nasa.gov/EPIC/archive/natural/{file_date}/png/{title}.png"
    image_names = []
    for image_description in image_descriptions:
        image_name = image_description["image"], image_description["date"]
        image_names.append(image_name)
    for image_name in image_names:
        title, image_date = image_name
        aDateTime = datetime.datetime.fromisoformat(image_date)
        file_date = aDateTime.strftime("%Y/%m/%d")
        response = requests.get(image_endpoint.format(file_date=file_date,
                                                      title=title),
                                params={"api_key": token})
        response.raise_for_status
        url = response.url
        filename = "images/images_EPIC/{title}.png".format(title=title)
        get_image(url, filename)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("NASA_TOKEN")
    fetch_nasa_apod(get_image=get_image, get_extencion=get_extencion)
    fetch_nasa_epic(get_image=get_image)
    fetch_spacex_lunch(get_image=get_image)
    
