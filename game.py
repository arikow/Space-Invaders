import curses
from interface import count_middle_scr

def start_screen(stdscr):
    midy, midx = count_middle_scr(stdscr)

    stdscr.addstr(midy, 20, 'Press key to begin...')
    stdscr.refresh()
    key = stdscr.getch()
    return True


def play(stdscr):

    start_screen(stdscr)

