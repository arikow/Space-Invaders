from screen_logic import draw_object, move_obj_yx

import curses


def colors():
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_BLUE, -1)
    curses.init_pair(4, curses.COLOR_WHITE, -1)
    curses.init_pair(5, curses.COLOR_RED, -1)
    return [curses.color_pair(i) for i in range(2, 6)]


class InvalidSpaceManagment(Exception):
    def __init__(self):
        super().__init__(
            "Some hitobxes aren't cover or imaginary hitboxes exist (number of hitobxes doesn't match)"
        )


class PhysicalObject:
    """
    Klasa bazowa dla pozostałych. Nie powinna być wywoływana sama w sobie.
    Posiada parametry:
    scr - 'screen' na którym jest wyświetlany dany obiekt. Jeśli nie ma przydzielonego dla siebie okna jest to stdscr.
    sapce_management - słownik przekazany przez referencje pozwala on jednoczesne działanie paru funkcji na tym samym obiekcie, bez bezpośredniej komunikajci między nimi.
    endurance - wytrzymałość danego obiektu, inaczej życie. Nie jest jeszcze używana przez wszystkie obiekty ale jest zamieszczona z myślą o rozbudowie programu.
    body - ciało w psotaci stringa danego obiektu.

    Każdy obiekt wypisany na ekranie posiada:
    atrybut hitbox - hitbox względem okna stdscr -> słownik powinien sie zgadzac ze słownikiem space_mamangement, obiekty nie moga na siebie nachodzić i się powtarzać.
    mock_hitbox - hitbox względem swojego własnego okna
    """

    def __init__(self, scr, space_management, endurance=1, body=""):
        self._hitbox = {}
        self._mock_hitbox = {}
        self._body = body
        self._mock_screen = scr
        self._endurance = endurance
        self._space_management = space_management

    def space_management(self):
        return self._space_management

    def new_assigment_sm(self, add=False, delate=False):
        """
        Metoda usuwająca/dodawąca pozycje w space management w zależnosćic o parametru do którego zostanie przekazany hitbox do usunięcia.
        """
        if isinstance(delate, dict):
            for cord in delate.keys():
                if cord in self.space_management().keys():
                    self._space_management.pop(cord)

        if isinstance(add, dict):
            self._space_management.update(add)

    def remove(self):
        pass

    def hitbox(self):
        return self._hitbox

    def keys_hitbox(self):
        return list(self.hitbox().keys())

    def vals_hitbox(self):
        return list(self.hitbox().values())

    def mock_hitbox(self):
        return self._mock_hitbox

    def keys_mock_hitbox(self):
        return list(self.mock_hitbox().keys())

    def vals_mock_hitbox(self):
        return list(self.mock_hitbox().values())

    def endurance(self):
        return self._endurance

    def take_damage(self):
        self._endurance -= 1

    def scr(self):
        return self._mock_screen

    def body(self):
        return self._body

    def update_true_hitbox(self):
        """
        Metoda licząca prawdziwą wartość hitboxu obiektu w zależności od jego położenia na stdscr.
        Metoda pobiera umiejscowienie okna na którym znajduję się obiekt i dodaję te współrzędne kolejno do każdego elementu mock_hitbox.
        """
        if self.hitbox():
            self.new_assigment_sm(delate=self.hitbox())
        hitbox = {}
        move_y, move_x = self.scr().getbegyx()
        for key, value in self.mock_hitbox().items():
            y, x = key
            y += move_y
            x += move_x
            hitbox[(y, x)] = value
        self._hitbox = hitbox
        self.new_assigment_sm(add=self.hitbox())


class Shield(PhysicalObject):
    """
    Klasa pojedyńczej tarczy.
    Różni sie od bazowej o:
    cordinates - meijsce w którym tarcza ma zacząć być rysowana. (lewy górny róg od którego zaczyna się rysowanie)
    color - kolor tarczy. Przypisanie None ponieważ potrzebne do testowania.
    """

    def __init__(
        self, scr, space_management, endurance, cordinates, color=None
    ):
        super().__init__(scr, space_management, endurance)
        self._cordinates = cordinates
        if color is None:
            self.color = colors()[0]
        else:
            self.color = color
        self.create_body()

    def __eq__(self, other):
        """
        Potrzebne do testowania obiektu.
        """
        return ("Shield", self.cordinates(), self.endurance()) == other

    def cordinates(self):
        return self._cordinates

    def create_body(self):
        """
        Metoda towrząca ciało na podstawie atrybutu endurance.
        Początkowo elementy tarczy składające się z @ miały miec 2 wytrzymałość. Możliwośc rozbudowy.
        """
        line = "###"
        strong_line = "@@@"
        body = ""
        lvl = 0
        endu = self._endurance
        double_life = self._endurance - 4
        while lvl < endu:
            if double_life > 0:
                f_line, f_char = strong_line, "@"
                double_life -= 1
                endu -= 1
            else:
                f_line, f_char = line, "#"
            if lvl < 3:
                help_lvl = lvl
                formated_line = (
                    (2 - lvl) * " " + f_line + 2 * lvl * f_char + "\n"
                )
            else:
                formated_line = (
                    (2 - help_lvl) * " "
                    + f_line
                    + 2 * help_lvl * f_char
                    + "\n"
                )
            body += formated_line
            lvl += 1
        self._body = body

    def draw(self):
        """
        Metoda rysująca tarczę i korektująca hitbox.
        """
        self._mock_hitbox = draw_object(
            self.scr(), self, self._cordinates, self.color
        )
        self.update_true_hitbox()


class Spaceship(PhysicalObject):
    """
    Klasa Spaceship.
    Różniąca się od bazowej o:
    bullets - referencja na liste wszystkich pocisków, również tych wystrzelonych przez przeciwników.
    Podobne znaczenie co space_management
    kolor - w tymprzypadku zdefiniowant na stałe i domyślny.
    """

    def __init__(self, scr, space_management, lifes, body, bullets):
        super().__init__(scr, space_management, lifes, body)
        self._bullets = bullets
        self.color = colors()[1]

    def bullets(self):
        return self._bullets

    def draw(self, cordinates):
        """
        Metoda czyszcząca ekran, rysujaca obiekt oraz korygująca hitbox.
        """
        self.scr().clear()
        self._mock_hitbox = draw_object(
            self.scr(), self, cordinates, self.color, True
        )
        self.update_true_hitbox()
        return True

    def move_right(self, right=True):
        """
        Metoda obsługująca poruszanie sie na boki obiektu.
        right - od tego zależy w którą storne będzie się poruszał obiekt. True
        """
        move_obj_yx(self, right=right)

    def shot(self, scr, direction=True):
        """
        Metoda inicjująca pocisk w miejscu w ktorym znajduje się srodek obiektu.
        Zawsze inicuje pociski na ekranie stdscr.
        direction - zależy od tego kogo się dotyczy metdoa czy Starship czy Enemy.
        """
        idx = len(self.keys_hitbox()) // 2
        y, x = self.keys_hitbox()[idx]
        if direction:
            y -= 1
        else:
            y += 1
        self._bullets.append(
            Bullet(scr, self._space_management, (y, x), direction)
        )


class Enemy(Spaceship):
    """
    Dziedziczy po Starship.
    Różnice:
    Każdy enemy posiada swój własny index w dwuwymiarowym słowniku wszystkich wrogów.
    """

    def __init__(
        self,
        scr,
        space_management,
        lifes,
        body,
        allenemies,
        row,
        column,
        bullets,
    ):
        super().__init__(scr, space_management, lifes, body, bullets)
        self._allenemies = allenemies
        self._index = (column, row)  # diffrent tuple than others -> (x, y)
        self._allenemies[column][row] = self

    def allenemies(self):
        return self._allenemies

    def index(self):
        return self._index

    def draw(self, cordinates):
        self._mock_hitbox = draw_object(
            self.scr(), self, cordinates, self.color, True
        )
        self.update_true_hitbox()
        return True

    def remove(self):
        """
        Usuwa wroga po trafieniu z słowika wszystkich wrogów
        """
        x, y = self.index()
        self._allenemies[x].pop(y)

    def move_right(self, direction=True):
        move_obj_yx(self, right=direction)


class Bullet(PhysicalObject):
    """
    Różnice od bazowej klasy.
    cordinates - to samo co  w Shield, czyli miejsce w którym ma się pojawić obiekt.
    direction - w którą strone ma lecieć pocisk w góre czy w dół
    """

    def __init__(
        self,
        scr,
        space_management,
        cordinates,
        direction,
        endurance=1,
        body="|",
    ):
        super().__init__(scr, space_management, endurance, body)
        self._hitbox = {cordinates: (self, body)}
        self._direction = direction
        self.puff()

    def direction(self):
        return self._direction

    def puff(self):
        """
        Metoda inicjująca pocisk na ekranie. (jedynie sam obraz)
        """
        self.scr().addstr(*self.keys_hitbox()[0], "|")

    def tick(self, cord, distance):
        """
        Metoda przesuwająca dany pocisk w góre lub w dół w zależnosci od atrybutu direction
        Dodatkowo, możliwość ustawienia dystansu o jaki się przesuwa pocisk.
        """
        val = self._hitbox[cord]
        self._hitbox.pop(cord)
        y, x = cord
        if self.direction():
            y -= distance
        else:
            y += distance
        self._hitbox[(y, x)] = val
