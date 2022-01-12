import pytest
import curses
from classes import *
from testing_data import shields_examples as shields


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


@pytest.fixture
def term():
    return Mock_Screen((24, 80))


@pytest.fixture
def shields():
    return [
        Shield(term, 5, (10, 10), 10)
    ]


@pytest.fixture
def spaceships():
    return [
        Spaceship(term, 3, '|-|')
    ]


def test_shield_init(shields):
    s = shields
    assert s[0].cordinates() == (10, 10)
    assert s[0].hitbox() == []
    assert s[0].mock_hitbox() == []
    assert s[0].endurance() == 5

def test_hitbox():
    term = Mock_Screen((24, 80))
    s = Shield(term, 1, (10, 10), 10)

    s.draw()
    assert s.mock_hitbox() == [[(10, 12), '#'],
    [(10, 13), '#'],
    [(10, 14), '#']
    ]

    s.set_hitbox()
    assert s.hitbox() == [[(10, 12), '#'],
    [(10, 13), '#'],
    [(10, 14), '#']
    ]