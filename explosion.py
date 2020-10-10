from entity import *
import asset_manager

from random import randint


class Explosion(Entity):
    def __init__(self, x, y, rate=0.3, size=20):
        super().__init__(x, y)

        self.rate = 1/rate
        self.life = 1
        self.size = size

        asset_manager.sounds['explode'].play()

    def update(self, dt):
        self.life -= dt * self.rate
        if self.life <= 0:
            self.alive = False

    def draw(self, surf):
        x = randint(-self.size, self.size) + self.position.x
        y = randint(-self.size, self.size) + self.position.y
        pygame.draw.circle(surf, (255, 255, 255), (x, y), self.life * 20, width=3)

