from os import path
import os

DATA_DIR = 'data/'

def read_file(file_name):
    p = path.join(DATA_DIR, file_name)
    with open(p) as f:
        content = f.readlines()
    return [x.strip() for x in content]

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

if __name__ == "__main__":
    print('haha')
