import math

import requests


def get_delta(toponym_dict):
    envelope = toponym_dict['boundedBy']['Envelope']
    lower = list(map(float, envelope['lowerCorner'].split()))
    upper = list(map(float, envelope['upperCorner'].split()))
    return upper[0] - lower[0], upper[1] - lower[1]


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b

    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    distance = math.sqrt(dx * dx + dy * dy)
    return distance


def get_coords(geocode):
    response = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": geocode,
        "format": "json"
    })
    pos = response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"]
    return list(map(float, pos.split()))
