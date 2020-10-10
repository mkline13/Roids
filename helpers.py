
def wrap(position):
    if position.x > 800:
        position.x = 0
    elif position.x < 0:
        position.x = 800

    if position.y > 600:
        position.y = 0
    elif position.y < 0:
        position.y = 600