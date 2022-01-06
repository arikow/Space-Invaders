import curses

def get_middle_scr(stdscr):
    my, mx = stdscr.getmaxyx()
    return my//2, mx//2

def frac_dist_from_border(stdscr, frac_up, frac_left):
    my, mx = stdscr.getmaxyx()
    return int(my*frac_up), int(mx*frac_left)