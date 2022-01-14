import pytest
from classes import *
from t_data import shields_body_ex, shields_hitbox_ex


class Mock_Screen:
    def __init__(self, size, y=0, x=0):
        self._begyx = y, x
        self._size = size
        self.content = {}

    def addstr(self, y, x, text):
        if x in range(0, x+1) and y in range(0, y+1):
            self.content[(y,x)] = text
        else:
            raise IndexError('Write in screen')

    def getmaxyx(self):
        return self._size

    def getbegyx(self):
        return self._begyx

    def refresh(self):
        pass

    def attron(self, *args):
        pass

    def attroff(self, *args):
        pass

term = Mock_Screen((24, 80))
win =Mock_Screen((24, 80), 73, 0)

@pytest.fixture
def shields(params=term):
    return [
        Shield(term, 0, (0, 9), 1),
        Shield(term, 1, (0, 9), 1),
        Shield(term, 2, (0, 23), 1),
        Shield(term, 3, (0, 37), 1),
        Shield(term, 4, (0, 51), 1),
        Shield(term, 5, (0, 64), 1),
        Shield(term, 6, (0, 78), 1),
        Shield(term, 7, (0, 78), 1),
        Shield(term, 8, (0, 78), 1)
    ]


@pytest.fixture
def spaceships():
    return [
        Spaceship(term, 3, '|o|')
    ]


def test_shield_init(shields):
    s = shields
    assert s[0].cordinates() == (0, 9)
    assert s[0].hitbox() == {}
    assert s[0].mock_hitbox() == {}
    assert s[0].endurance() == 0
    assert shields[0].body() == shields_body_ex[0]


@pytest.mark.parametrize("num, body", [(nr, shields_body_ex[nr]) for nr in range(1, 9)])
def test_shields_body_creator(shields, num, body):
    assert '\n'+shields[num].body() == body

def test_shield_hitbox(shields):
    s = shields[4]
    s.draw()
    assert s.mock_hitbox() == shields_hitbox_ex[4]

    s.update_true_hitbox()
    assert s.hitbox() == shields_hitbox_ex[4]