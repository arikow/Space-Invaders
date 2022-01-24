import curses
from game import play
from screen_logic import *
from model_io import load_scoreboard, clear_scoreboard, read_readme


def set_position(key, pos, len):
    """
    Funkcja ustawiające indeks zależny od ilości klikniętych strzałek w górę lub w dół
    Ograniczona [0; 3]
    Używana to przykazywania informacji co wybrał użytkownik.
    """
    if key == curses.KEY_UP and pos > 0:
        return pos - 1
    elif key == curses.KEY_DOWN and pos < len - 1:
        return pos + 1
    else:
        return pos


def menu(stdscr, select):
    """
    Funckja inicjująca menu.
    """
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_CYAN)

    position_idx = 0

    key = None

    while key != 10:

        midy, midx = get_middle_scr(stdscr)

        stdscr.erase()

        for word in select:
            if position_idx == select.index(word):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(
                    midy - len(select) // 2 + select.index(word),
                    midx - len(word) // 2,
                    word,
                )
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(
                    midy - len(select) // 2 + select.index(word),
                    midx - len(word) // 2,
                    word,
                )

        stdscr.refresh()

        key = stdscr.getch()
        position_idx = set_position(key, position_idx, len(select))

    stdscr.erase()
    return position_idx


def scoreboard(scr):
    """
    Funkjca wyświetlająca tablicę graczy znajdujących się w pliku scoreboard.csv
    Pozwala na zresetowanie tej listy, lecz jeśli menualnie dopisze się tam gracza to funckja nie sortuje ich.
    Dopiero po rozegraniu jednej rozgrywki i zapisaniu swojego wyniku to sie stanie.
    Modyfikowanie scoreboard.csv nie zalecane.
    """
    key = 0
    while key != 27:
        y, x = scr.getmaxyx()
        start = (x - len("SCOREBOARD")) // 2
        scr.clear()
        scr.addstr(1, start, "SCOREBOARD")
        players = load_scoreboard()
        i = 0
        for nick, score in players.items():
            row = str(i + 1) + ". " + nick + ": " + str(score)
            scr.addstr(2 + i, start, row)
            i += 1
            if i >= 10:
                break
        scr.addstr(
            i + 3,
            (x - len("Press ESC to quit or R to reset")) // 2,
            "Press ESC to quit or R to reset",
        )
        while key != 27:
            key = scr.getch()
            if key == 82 or key == 114:
                clear_scoreboard()


def help(scr):
    """
    Funkcja wyświetlająca plik readme.txt w konsoli.
    """
    key = 0
    header, text = read_readme()
    y, x = scr.getmaxyx()
    scr.addstr(1, (x - len(header)) // 2, header)
    scr.addstr(3, 0, text)
    while key != 27:
        key = scr.getch()


def ext(scr):
    pass


def main(stdscr):
    curses.curs_set(0)
    curses.use_default_colors()
    curses.set_escdelay(100)

    select_menu = ["PLAY", "SCOREBOARD", "HELP", "EXIT"]

    menu_idx = {0: play, 1: scoreboard, 2: help, 3: ext}

    select_idx = -1
    while select_idx != 3:
        select_idx = menu(stdscr, select_menu)
        menu_idx[select_idx](stdscr)


curses.wrapper(main)
