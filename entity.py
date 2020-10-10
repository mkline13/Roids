import pygame.math


def _counter(start=0):
    i = start
    while True:
        yield i
        i += 1


class Entity:
    """Entity base class. All entities must subclass this."""
    id_gen = _counter()

    def __init__(self, x, y, data={}):
        # a unique id, used for searching
        self.id = next(self.id_gen)

        # game coordinates
        self.position = pygame.math.Vector2(x, y)

        # game data: hp, damage, armor, etc.
        self.data = data

        # when alive is false, this entity will be removed from the entity list
        self.alive = True

        # collision
        self.collision_radius = 0
        self.team = ''

    def update(self, dt):
        pass

    def draw(self, surf):
        pass

    def collide_with(self, other):
        pass

    def on_death(self):
        pass