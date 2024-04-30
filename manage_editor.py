import os

class file:
    def __init__(self, path):
        with open(path, "r") as f:
            data = f.read()
        self.path = path
        self.name = path.split('/')[-1]
        self.data = data
        self.read = os.access(path, os.R_OK)
        self.write = os.access(path, os.W_OK)
        self.execute = os.access(path, os.X_OK)
        self.size = os.path.getsize(path)

class open_files:
    def __init__(self):
        self.files = []

    def add_file(self, path):
        self.files.append(file(path))

def init_open_files():
    return open_files()