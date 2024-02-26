'''
Loads all the data related to the current working directory

get_cwd() creates a cwd object and returns it

A cwd object contains the current working directory path, a list of all items, a list of all items which are directories only, a list of all items which are files only and a list of all items which can't be identified as either a file or a directory
Each item stored in either of the lists is an object of its own

Dir objects contain the path for the directory and permissions related to the directory

File objects contain the path for the file and data related to the file itself

Unknown item objects contain only the path for the item

A cwd object will also have the necessary data required by the rendering function to render the items to the output when viewing the files and directories in the program
'''


import os

#Directory class for items in the current working directory which are specifically directories
class dir:
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]
        self.type = 'dir'
        self.read = os.access(path, os.R_OK)
        self.write = os.access(path, os.W_OK)
        self.execute = os.access(path, os.X_OK)

#File class for items in the current working directory which are specifically files
class file:
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]
        self.type = 'file'
        self.read = os.access(path, os.R_OK)
        self.write = os.access(path, os.W_OK)
        self.execute = os.access(path, os.X_OK)
        self.size = os.path.getsize(path)

#Class for items in the current working directory which cannot be distinguished as either a directory or a file
class unknown:
    def __init__(self, path):
        self.path = path
        self.name = path.split('/')[-1]
        self.type = 'unknown'

#CWD class containing all information related to the current working directory, including items and their data
class cwd:
    def __init__(self):
        path = os.getcwd()
        list = ['..'] + os.listdir()

        self.path = path
        self.items = []
        self.files = []
        self.dirs = []

        #Create objects for all items in the current working directory and add the mto the respective lists
        for i in range(len(list)):
            p = f'{path}/{list[i]}'
            if os.path.isdir(p):
                item_obj = dir(p)
                self.items.append(item_obj)
                self.dirs.append(item_obj)
            elif os.path.isfile(p):
                item_obj = file(p)
                self.items.append(item_obj)
                self.files.append(item_obj)
            else:
                item_obj = unknown(p)
                self.items.append(item_obj)

        #Data required for rendering the output when dislpaying files and directories
        self.pos = 0   #Position of the selected/highlighted item

    #Function to scroll up or down
    def scroll(self, val):
        self.pos += val
        if self.pos < 0:
            self.pos = len(self.items) - 1
        elif self.pos > len(self.items) - 1:
            self.pos = 0

#Load items, initialize item objects and pack them in the cwd object and return it
def fetch_cwd():
    return cwd()

#Change the current working directory
def cd(loc):
    os.chdir(loc)