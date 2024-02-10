import curses, os

#Curses Initialization
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
stdscr.keypad(1)

#Loading Settings
import load_settings
colors = load_settings.fetch_color_profiles()

#Constants (not exactly but yea)
import load_directory
mode = 'explorer'   #May be explorer or editor depending on which one is being used
notif_msg = ''   #Msg to be displayed once a major event takes place
cwd = load_directory.fetch_cwd()   #Fetch the current working directory

#Function to handle keypresses in the explorer
def handle_explorer_events(key):
    global cwd
    if key == curses.KEY_UP or key == curses.KEY_DOWN:
        cwd.scroll({curses.KEY_UP: -1, curses.KEY_DOWN: 1}[key])

    elif key == curses.KEY_ENTER or key == 13 or key == 10:
        load_directory.cd(cwd.items[cwd.pos].name)
        cwd = load_directory.fetch_cwd()



#Function to handle keypresses in the editor
def handle_editor_events(key):
    pass

#Function to render the explorer
def render_explorer():
    y,x = stdscr.getmaxyx()
    top = 0
    while top + y - 1 < cwd.pos + 1:
        top += y - 1
    bottom = y - 1 if len(cwd.items[top:]) > y - 1 else len(cwd.items[top:])

    stdscr.clear()
    stdscr.refresh()

    stdscr.addstr(0, 0, (cwd.path + ' '*(x - len(cwd.path) if x > len(cwd.path) else 0))[:x], colors.general[1])
    for i in range(top, top + bottom):
        c = None
        if cwd.items[i].type == 'dir':
            c = colors.explorer_dir
        elif cwd.items[i].type == 'file':
            c = colors.explorer_file
        elif cwd.items[i].type == 'unknown':
            c = colors.explorer_unknown
        
        c = c[{False: 0, True: 1}[cwd.pos == i]]
        stdscr.addstr(i - top + 1, 0, cwd.items[i].name[:x], c)

    stdscr.refresh()


#Function to render the editor
def render_editor():
    pass

#Main event loop
while True:
    if mode == 'explorer':
        render_explorer()
        handle_explorer_events(stdscr.getch())
    elif mode == 'editor':
        render_editor()
        handle_editor_events(stdscr.getch())