from os import path

DATA_DIR = 'data/'

def read_file(file_name):
    p = path.join(DATA_DIR, file_name)
    with open(p) as f:
        content = f.readlines()
    return [x.strip() for x in content]


if __name__ == "__main__":
    print('haha')
