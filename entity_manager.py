from test_entity import *
from explosion import *
from ship import *
from asteroid import *
from bullet import *


# Dictionary of entities by name
# k: entity names, v: entity classes
_spawn_dict = {
    "test": Test,
    "explosion": Explosion,
    "ship": Ship,
    "asteroid": Asteroid,
    "bullet": Bullet
}

# list of all entities
_entity_list = []


def update(dt):
    global _entity_list
    clean_up = []

    # Update each entity in _entities
    for i, e in enumerate(_entity_list):
        e.update(dt)

        if not e.alive:
            e.on_death()
            clean_up.append(i)

    # Clean up 'dead' entities
    for i in reversed(clean_up):
        del _entity_list[i]

    # Collision detection
    _collide_entities()


def draw(surf):
    for e in _entity_list:
        e.draw(surf)


def spawn(name, *args, **kwargs):
    # log spawn info
    # print('-SPAWNING', name, args, kwargs)

    try:
        # create new entity from spawn dict
        new_ent = _spawn_dict[name](*args, **kwargs)

        # append the entity to the list
        _entity_list.append(new_ent)
        return new_ent
    except KeyError:
        print(f"-CANNOT SPAWN, no such entity: '{name}'")


def reset():
    _entity_list.clear()

def _collide_entities():
    for i, e1 in enumerate(_entity_list):
        for e2 in _entity_list[i+1:]:
            if e1.team != e2.team:
                coll_dist = e1.collision_radius + e2.collision_radius
                if e1.position.distance_to(e2.position) <= coll_dist:
                    e1.collide_with(e2)
                    e2.collide_with(e1)
