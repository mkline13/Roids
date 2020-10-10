from entity import *
import asset_manager, entity_manager

from random import randint


class Test(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = asset_manager.generate_asteroid(23)

        self.spawn_counter_max = 0.7
        self.spawn_counter = self.spawn_counter_max

    def update(self, dt):
        self.spawn_counter -= dt
        # if self.spawn_counter <= 0:
        #     entity_manager.spawn('explosion', self.position.x + randint(-20, 20), self.position.y + randint(-20, 20))
        #     self.spawn_counter = self.spawn_counter_max

    def draw(self, surf):
        surf.blit(self.image, self.position)

    def on_death(self):
        pass