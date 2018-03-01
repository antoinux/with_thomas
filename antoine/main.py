import utils
import numpy as np
from functools import total_ordering

FILE_1, FILE_2, FILE_3, FILE_4, FILE_5 = "a_example.in", "b_should_be_easy.in", "c_no_hurry.in", "d_metropolis.in", "e_high_bonus.in"

DATA_DIR = 'data/'

R, C, F, N, B, T = 0, 0, 0, 0, 0, 0
rides = []
cars = []

@total_ordering
class Ride():
    def __init__(self, p):
        self.a = p[0]
        self.b = p[1]
        self.x = p[2]
        self.y = p[3]
        self.s = p[4]
        self.t = p[5]
    
    def __equal__(self, other):
        return self.s == other.s

    def __lt__(self, other):
        return self.s < other.s

def clean():
    global rides, cars
    rides = []
    cars = []

def input(file_name):
    lines = utils.read_file(file_name)
    global R, C, F, N, B, T
    R = int(lines[0].split()[0])
    C = int(lines[0].split()[1])
    F = int(lines[0].split()[2])
    N = int(lines[0].split()[3])
    B = int(lines[0].split()[4])
    T = int(lines[0].split()[5])
    global rides
    stuff = [[int(x) for x in lines[i].split()] for i in range(1, N+1)]
    rides = [Ride(x) for x in stuff]

def save_cars(f):
    with open(f, 'w') as fi:
        for i in range(F):
            fi.write(str(len(cars[i]))+' ')
            for x in cars[i]:
                fi.write(str(x) + ' ')
            fi.write('\n')

def strat_dummy():
    ra = np.random.permutation(N)
    bulks = np.array_split(ra, F)
    global cars
    cars = bulks

def strat_early():
    ra = np.argsort(rides)
    global cars
    cars = [ra[i::F] for i in range(F)]

def exe(input_file):
    clean()
    input(input_file)
    strat_early()
    out = 'data/early/'
    utils.ensure_dir(out)
    save_cars(out+input_file+'_out')

if __name__ == "__main__":
    exe(FILE_1)
    exe(FILE_2)
    exe(FILE_3)
    exe(FILE_4)
    exe(FILE_5)

