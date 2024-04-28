import random
from io import BytesIO
import pygame
import requests

from functions import get_coords

CITIES = ['Мурманск', 'Москва', 'Рязань', 'Ярославль', 'Владивосток']
STATIC_URL = "http://static-maps.yandex.ru/1.x/"

images = list()
for city in CITIES:
    coords = get_coords(city)
    coords[0] += random.randrange(60) / 1000 * random.choice([-1, 1])
    coords[1] += random.randrange(60) / 1000 * random.choice([-1, 1])
    spn = str(random.randrange(25) / 1000)
    response = requests.get(STATIC_URL, params={
        'll': ','.join(list(map(str, coords))),
        'spn': ','.join([spn, spn]),
        'l': random.choice(['map', 'sat'])
    })
    images.append(pygame.image.load(BytesIO(response.content)))

pygame.init()
screen = pygame.display.set_mode((600, 450))
run = True
image = random.choice(images)
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        elif event.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]:
            prev = image
            while prev == image:
                image = random.choice(images)
    screen.fill((0, 0, 0))
    screen.blit(image, (0, 0))
    pygame.display.flip()
pygame.quit()
