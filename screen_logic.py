import curses

def get_middle_scr(stdscr):
    my, mx = stdscr.getmaxyx()
    return my//2, mx//2

def dist_from_right_border(stdscr, y, x):
    my, mx = stdscr.getmaxyx()
    return my-y, mx-x