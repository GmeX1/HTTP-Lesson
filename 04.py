import sys
from io import BytesIO

import requests
from PIL import Image

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
    'results': 10
}).json()['features']

points = list()
for feature in search_json:
    coords = list(map(str, feature['geometry']['coordinates']))
    if 'Hours' in feature['properties']['CompanyMetaData']:
        if 'Availabilities' in feature['properties']['CompanyMetaData']['Hours']:
            interval = feature['properties']['CompanyMetaData']['Hours']['Availabilities'][0]
            if 'TwentyFourHours' in interval:
                if interval['TwentyFourHours']:
                    points.append(','.join([*coords, 'pm2gnm']))
                else:
                    points.append(','.join([*coords, 'pm2blm']))
            else:
                points.append(','.join([*coords, 'pm2blm']))
        else:
            points.append(','.join([*coords, 'pm2blm']))
    else:
        points.append(','.join([*coords, 'pm2grm']))

response = requests.get("http://static-maps.yandex.ru/1.x/", params={
    "l": "map",
    "pt": '~'.join(points)
})

Image.open(BytesIO(
    response.content)).show()
