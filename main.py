import curses
from interface import *
from game import play

def refresh_screen():
    return menu

def main(stdscr):
    curses.curs_set(0)

    select_menu = ['PLAY', 'LOAD OPTIONS', 'SCOREBOARD', 'HELP', 'EXIT']
    
    select_idx = menu(stdscr, select_menu)
    
    menu_idx = {0: play(stdscr), 1: load_options(), 2: scoreboard(), 3: help(), 4: ext()}

    menu_idx[select_idx]


curses.wrapper(main)