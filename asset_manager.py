import pygame.image, pygame.mixer
import pygame.draw, math
from random import randint

pygame.init()


def _generate_ship():
    surf = pygame.surface.Surface((32, 32))
    col = (255, 255, 255)
    points = [(5, 31), (16, 0), (17, 0), (28, 31)]
    pygame.draw.polygon(surf, col, points, width=2)
    return surf


def generate_asteroid(radius, resolution=10):
    surf = pygame.surface.Surface((48, 48))
    col = (255, 255, 255)
    points = []
    for i in range(resolution):
        angle = (i + 1) / resolution * 2 * math.pi
        magnitude = radius - randint(0, int(radius * 0.4))
        #SOH CAH TOA
        x = math.cos(angle) * magnitude
        y = math.sin(angle) * magnitude
        points.append((x + surf.get_width() // 2, y + surf.get_height() // 2))
    pygame.draw.polygon(surf, col, points, width=2)
    return surf


def _generate_bullet(size):
    surf = pygame.surface.Surface((size, size))
    col = (255, 255, 255)
    surf.fill(col)
    return surf


images = {
    "test": pygame.image.load('resources/test.png'),
    "ship": _generate_ship(),
    "bullet": _generate_bullet(4),
}


sounds = {
    "test": pygame.mixer.Sound('resources/test.wav'),
    "shoot": pygame.mixer.Sound('resources/shoot.wav'),
    "explode": pygame.mixer.Sound('resources/explode.wav'),
}


def init_images(surf):
    for k, v in images.items():
        print('initializing image:', k, v)
        v.convert(surf)
        v.set_colorkey((255, 0, 255))


if __name__ == '__main__':
    a = _generate_asteroid(32)