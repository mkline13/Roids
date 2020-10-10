from entity import *
import asset_manager
from helpers import wrap
import math


class Bullet(Entity):
    def __init__(self, x, y, angle, owner, damage=1):
        data = {
            "damage": damage,
        }
        super().__init__(x, y, data)

        self.image = asset_manager.images['bullet']

        # Velocity
        speed = 600
        self.velocity = pygame.math.Vector2(0, 0)
        self.velocity.from_polar((speed, angle * (180 / math.pi)))
        self.life = 0.5

        # Collisions
        self.collision_radius = 2
        self.team = 'player'

    def update(self, dt):
        if self.life > 0:
            self.position += self.velocity * dt
            wrap(self.position)
            self.life -= dt
        else:
            self.alive = False

    def draw(self, surf):
        surf.blit(self.image, self.position - (2, 2))

    def collide_with(self, other):
        self.alive = False
