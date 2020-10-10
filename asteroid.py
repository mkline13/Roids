from entity import *
import entity_manager, score
import asset_manager

from helpers import wrap
import math
from random import uniform, choice, randint


class Asteroid(Entity):
    def __init__(self, x, y, size=2):
        data = {
            "hp": 1,
            "size": size,  # 2 sizes, big and small
            "damage": 1,
        }
        super().__init__(x, y, data)

        # Collision
        if size > 1:
            self.collision_radius = 24
        else:
            self.collision_radius = 16
        self.team = 'roids'

        self.image = asset_manager.generate_asteroid(self.collision_radius - 1)

        # Spin variables
        self.angle = 0  # angle of rotation in radians
        self.spin = uniform(2, 4) * choice([-1, 1])

        # Velocity
        speed = 200 * (1 / size)
        self.velocity = pygame.math.Vector2(0, 0)
        self.velocity.from_polar((speed, randint(0, 359)))

        # Score
        score.increment_asteroids()

    def update(self, dt):
        if self.data['hp'] < 1:
            self.alive = False
            return
        self.angle += dt * self.spin
        self.position += self.velocity * dt
        wrap(self.position)

    def draw(self, surf):
        angle = -self.angle * (180 / math.pi) + 90
        img = pygame.transform.rotozoom(self.image, angle, 1)
        offset = pygame.math.Vector2(img.get_width() // 2, img.get_height() // 2)
        pos = self.position - offset
        surf.blit(img, pos)

    def collide_with(self, other):
        damage = other.data.get('damage', 0)
        if damage:
            self.data['hp'] -= damage
            if self.data['hp'] <= 0:
                self.alive = False
            print(self, 'damaged', damage)

    def on_death(self):
        entity_manager.spawn('explosion', self.position.x, self.position.y)
        if self.data['size'] > 1:
            entity_manager.spawn('asteroid', self.position.x, self.position.y, size=1)
            entity_manager.spawn('asteroid', self.position.x, self.position.y, size=1)
            entity_manager.spawn('asteroid', self.position.x, self.position.y, size=1)
        score.increment_score()