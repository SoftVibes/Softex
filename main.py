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
import manage_directory, manage_editor
mode = 'explorer'   #May be explorer or editor depending on which one is being used
notif_msg = 'Press CTRL+H for help'   #Msg to be displayed once a major event takes place
cwd = manage_directory.fetch_cwd()   #Fetch the current working directory
open_files = manage_editor.init_open_files()   #Fetch the open files object


#Function to handle keypresses in the explorer
def handle_explorer_events(key):
    global cwd
    global notif_msg
    global mode
    if key == curses.KEY_UP or key == curses.KEY_DOWN:
        cwd.scroll({curses.KEY_UP: -1, curses.KEY_DOWN: 1}[key])

    elif key == curses.KEY_ENTER or key == 13 or key == 10:
        if cwd.items[cwd.pos].type == 'dir':
            manage_directory.cd(cwd.items[cwd.pos].name)
            cwd = manage_directory.fetch_cwd()
            notif_msg = 'Changed the current directory. Press CTRL+H for help'
        elif cwd.items[cwd.pos].type == 'file':
            open_files.add_file(cwd.items[cwd.pos].path)
            notif_msg = f'Opened {cwd.items[cwd.pos].name} in the editor. Press CTRL+E to switch between editor and explorer'
        else:
            notif_msg = 'Not a file/directory, cannot perform any action on it. Press CTRL+H for help'

    elif key == 5:
        mode = 'editor'
        notif_msg = 'Switched mode to editors. Press CTRL+H for help'

    elif key == 14:
        pass

#Function to render the explorer
def render_explorer():
    y,x = stdscr.getmaxyx()
    top = 0
    while top + y - 2 < cwd.pos + 1:
        top += y - 2
    bottom = y - 2 if len(cwd.items[top:]) > y - 2 else len(cwd.items[top:])

    stdscr.clear()
    stdscr.refresh()

    #Filling the top line with the directory path 
    stdscr.addstr(0, 0, (cwd.path + ' '*(x - len(cwd.path) if x > len(cwd.path) else 0))[:x], colors.general[1])
    
    #Printing the items
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

    #Printing the notif msg, insstr used to fill the bottom right character on the screen
    global notif_msg
    stdscr.insstr(y - 1, 0, (notif_msg + ' '*(x - len(notif_msg) if x > len(notif_msg) else 0))[:x], colors.general[1])
    stdscr.refresh()
    notif_msg = 'Press CTRL+H for help'



#Function to handle keypresses in the editor
def handle_editor_events(key):
    pass

#Function to render the editor
def render_editor():
    pass

#Main event loopk
while True:
    if mode == 'explorer':
        render_explorer()
        handle_explorer_events(stdscr.getch())
    elif mode == 'editor':
        render_editor()
        handle_editor_events(stdscr.getch())
