from entity import *
import entity_manager
import asset_manager

from helpers import wrap
import math


class Ship(Entity):
    def __init__(self, x, y):
        data = {
            "hp": 1,
            "damage": 1
        }

        super().__init__(x, y, data)

        self.image = asset_manager.images['ship']

        self._controls = {
            'left': False,
            'right': False,
            'thrust': False,
            'shoot': False,
        }

        # Motion vars
        self.angle = 0  #angle of rotation in radians
        self.velocity = pygame.math.Vector2(0, 0)

        self._rotation_rate = 4
        self._acceleration_rate = 7
        self._max_speed = 6

        # Weapon vars
        self.cooldown_max = 0.2
        self.cooldown = 0

        # Collisions
        self.collision_radius = 11
        self.team = 'player'

    def update(self, dt):
        # Convert control data into numbers
        rotation = (-1 if self._controls['left'] else 0) + (1 if self._controls['right'] else 0)
        thrust = 1 if self._controls['thrust'] else 0

        # Update angle
        self.angle += rotation * self._rotation_rate * dt

        # Update velocity
        delta_velocity = pygame.math.Vector2(0, 0)
        delta_velocity.from_polar(
            (self._acceleration_rate * dt * thrust, self.angle * (180 / math.pi))
        )

        # apply the change in velocity
        self.velocity += delta_velocity

        # clamp velocity to a maximum speed
        if self.velocity.length() > self._max_speed:
            self.velocity.scale_to_length(self._max_speed)

        # apply velocity to position
        self.position += self.velocity
        wrap(self.position)

        # shoot the gun?
        if self.cooldown > 0:
            self.cooldown -= dt
        elif self._controls['shoot'] and self.cooldown <= 0:
            entity_manager.spawn('bullet', self.position.x, self.position.y, self.angle, self)
            asset_manager.sounds['shoot'].play()
            self.cooldown = self.cooldown_max

        self.clear_controls()

    def draw(self, surf):
        angle = -self.angle * (180 / math.pi) + 270
        img = pygame.transform.rotozoom(self.image, angle, 1)
        offset = pygame.math.Vector2(img.get_width() // 2, img.get_height() // 2)
        pos = self.position - offset
        surf.blit(img, pos)
        # surf.blit(self.image, pos)

    def set_controls(self, **kwargs):
        for k, v in kwargs.items():
            if k in self._controls:
                self._controls[k] = v
            else:
                raise KeyError(f'no such control ({name}) attached to {self.__class__.__name__}')

    def clear_controls(self):
        for k in self._controls.keys():
            self._controls[k] = False

    def collide_with(self, other):
        damage = other.data.get('damage', 0)
        if damage:
            self.data['hp'] -= damage
            if self.data['hp'] <= 0:
                self.alive = False
            print(self, 'damaged', damage)

    def on_death(self):
        entity_manager.spawn('explosion', self.position.x, self.position.y)