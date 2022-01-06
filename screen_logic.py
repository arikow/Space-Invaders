import curses

def get_middle_scr(stdscr):
    my, mx = stdscr.getmaxyx()
    return my//2, mx//2

def frac_dist_from_border(stdscr, frac_up, frac_left):
    my, mx = stdscr.getmaxyx()
    return int(my*frac_up), int(mx*frac_left)

def draw_lines(stdscr, body_ls, cordinates, color):
    y, x = cordinates
    length = [len(line) for line in body_ls]
    x -= max(length)//2
    i = 0
    stdscr.attron(color)
    for line in body_ls:
        stdscr.addstr(y+i, x, line)
        i += 1
    stdscr.attroff(color)
    return True
