import sys
from io import BytesIO

import requests
from PIL import Image

from functions import lonlat_distance

toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
json_response = response.json()

toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

search_json = requests.get('https://search-maps.yandex.ru/v1/', params={
    'apikey': '97b0bfba-2257-4f97-97e6-1f3d2f8a5fd3',
    'text': 'аптека',
    'll': ','.join([toponym_longitude, toponym_lattitude]),
    'lang': 'ru_RU',
    'type': 'biz',
}).json()['features'][0]
print(f'Адрес: {search_json["properties"]["CompanyMetaData"]["address"]}')
print(f'Название: {search_json["properties"]["CompanyMetaData"]["name"]}')
print(f'Время работы: {search_json["properties"]["CompanyMetaData"]["Hours"]["text"]}')
distance = round(lonlat_distance(
    list(map(float, toponym_coodrinates.split())),
    list(map(float, search_json["geometry"]["coordinates"]))
))
print(f'Расстояние: {distance} метров')

response = requests.get("http://static-maps.yandex.ru/1.x/", params={
    "l": "map",
    "pt": ','.join([toponym_longitude, toponym_lattitude, 'round']) + '~' + ','.join(
        [*map(str, search_json["geometry"]["coordinates"]), 'comma'])
})

Image.open(BytesIO(
    response.content)).show()
