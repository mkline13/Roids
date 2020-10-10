

# every time an asteroid is created, increment _asteroids
_asteroids = 0

# every time an asteroid is destroyed, increment _score
_score = 0


def increment_score():
    global _score
    _score += 1


def increment_asteroids():
    global _asteroids
    _asteroids += 1


def get_score():
    global _score
    return _score


def get_asteroids():
    global _asteroids
    return _asteroids


def get_remaining():
    global _score, _asteroids
    return _asteroids - _score


def reset():
    global _score, _asteroids
    _score = 0
    _asteroids = 0