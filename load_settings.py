'''
Loads all settings from settings.json

fetch_color_profiles() creates a color_profile object with all the loaded color profiles from settings.json and initialized curses color codes and returns it
'''


import curses, json

#Loading the json file
with open("settings.json", "r") as f:
    data = json.load(f)


#Loading the color profiles and creating necessary objects
colors = {"black": curses.COLOR_BLACK, "white": curses.COLOR_WHITE, "blue": curses.COLOR_BLUE, "red": curses.COLOR_RED, "green": curses.COLOR_GREEN, "yellow": curses.COLOR_YELLOW, "cyan": curses.COLOR_CYAN, "magenta": curses.COLOR_MAGENTA}

class color_profile:
    def __init__(self):

        #Color profile for general text
        curses.init_pair(1, colors[data['general']['fg']], colors[data['general']['bg']])
        curses.init_pair(2, colors[data['general']['bg']], colors[data['general']['fg']])
        self.general = [curses.color_pair(1), curses.color_pair(2)]

        #Color profile for directory name
        curses.init_pair(3, colors[data['explorer']['directory']['fg']], colors[data['explorer']['directory']['bg']])
        curses.init_pair(4, colors[data['explorer']['directory']['bg']], colors[data['explorer']['directory']['fg']])
        self.explorer_dir = [curses.color_pair(3), curses.color_pair(4)]

        #Color profile for file name
        curses.init_pair(5, colors[data['explorer']['file']['fg']], colors[data['explorer']['file']['bg']])
        curses.init_pair(6, colors[data['explorer']['file']['bg']], colors[data['explorer']['file']['fg']])
        self.explorer_file = [curses.color_pair(5), curses.color_pair(6)]

        #Color profile for unknown item
        curses.init_pair(7, colors[data["explorer"]["unknown"]["fg"]], colors[data["explorer"]["unknown"]["bg"]])
        curses.init_pair(8, colors[data["explorer"]["unknown"]["bg"]], colors[data["explorer"]["unknown"]["fg"]])
        self.explorer_unknown = [curses.color_pair(7), curses.color_pair(8)]

        #Color profile for editor text
        curses.init_pair(9, colors[data['editor']['fg']], colors[data['editor']['bg']])
        curses.init_pair(10, colors[data['editor']['bg']], colors[data['editor']['fg']])
        self.editor = [curses.color_pair(9), curses.color_pair(10)]

        #Color profiles for specific syntax highlighting in editor
        syntax_highlights = {}
        for i in range(len(list(data["editor"]["syntax-highlights"].keys()))):
            curses.init_pair(11 + i, colors[data["editor"]["syntax-highlights"][list(data["editor"]["syntax-highlights"].keys())[i]]["fg"]], colors[data["editor"]["syntax-highlights"][list(data["editor"]["syntax-highlights"].keys())[i]]["bg"]])
            curses.init_pair(12 + i, colors[data["editor"]["syntax-highlights"][list(data["editor"]["syntax-highlights"].keys())[i]]["bg"]], colors[data["editor"]["syntax-highlights"][list(data["editor"]["syntax-highlights"].keys())[i]]["fg"]])
            syntax_highlights[list(data["editor"]["syntax-highlights"].keys())[i]] = [curses.color_pair(11 + i), curses.color_pair(12 + i)]

        self.syntax = syntax_highlights
        
#Fetch and return a color_profile object
def fetch_color_profiles():
    return color_profile()