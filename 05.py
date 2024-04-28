import sys

import requests

toponym_to_find = " ".join(sys.argv[1:])
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    'results': 1,
    'kind': 'district',
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)
pos = response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
geocoder_params['geocode'] = pos

response = requests.get(geocoder_api_server, params=geocoder_params)
print(response.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name'])
