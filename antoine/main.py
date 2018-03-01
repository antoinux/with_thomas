import utils
import numpy as np
from functools import total_ordering
import heapq

##### RIGHT NOW STRAT_EARLY WORKS THE BEST ######

FILE_1, FILE_2, FILE_3, FILE_4, FILE_5 = "a_example.in", "b_should_be_easy.in", "c_no_hurry.in", "d_metropolis.in", "e_high_bonus.in"

DATA_DIR = 'data/'

R, C, F, N, B, T = 0, 0, 0, 0, 0, 0
rides = []
cars = []
cars_sorted = []
ORDER = 's'



@total_ordering
class Ride():
    def __init__(self, p, i):
        self.a = p[0]
        self.b = p[1]
        self.x = p[2]
        self.y = p[3]
        self.s = p[4]
        self.t = p[5]
        self.id = i
    
    def __equal__(self, other):
        if ORDER == 's':
            return self.s == other.s
        else:
            return self.t == other.t

    def __lt__(self, other):
        if ORDER == 's':
            return self.s < other.s
        else:
            return self.t < other.t

@total_ordering
class Car():
    def __init__(self, i):
        self.p = (0, 0)
        self.t = 0
        self.trips = []
        self.points = 0
        self.id = i

    def dist(self, r):
        return abs(self.p[0] - r.a) + abs(self.p[1] -r.b)

    # returns 0 if can't take ride on time, 1 if if can but with no bonus, 2 if
    # it can with bonus
    def can_take_ride(self, r):
        start_time = max(self.t + self.dist(r), r.s)
        end_time = start_time + abs(r.x - r.a) + abs(r.y - r.b)
        if start_time == r.s:
            return 2
        elif end_time <= r.t:
            return 1
        else:
            return 0

    def add_ride(self, r):
        start_time = max(self.t + self.dist(r), r.s)
        end_time = start_time + abs(r.x - r.a) + abs(r.y - r.b)
        self.p = (r.x, r.y)
        self.t = end_time

        lol = self.can_take_ride(r)
        if lol == 1:
            self.points += abs(r.x - r.a) + abs(r.y - r.b)
        if lol == 2:
            self.points += B
        self.trips.append(r.id)

    def __equal__(self, other):
        return self.t == other.t

    def __lt__(self, other):
        return self.t < other.t

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
    rides = [Ride(stuff[i], i) for i in range(N)]

def save_cars(f):
    with open(f, 'w') as fi:
        for i in range(F):
            rl = cars[i].trips
            fi.write(str(len(rl))+' ')
            for x in rl:
                fi.write(str(x) + ' ')
            fi.write('\n') 

def save_cars_old(f):
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
    global ORDER
    ORDER = 's'
    ra = np.argsort(rides)
    global cars
    cars = [ra[i::F] for i in range(F)]

def strat_not_late():
    global ORDER
    ORDER = 't'
    ra = np.argsort(rides)
    global cars
    cars = [ra[i::F] for i in range(F)]

def strat_early_not_stupid():
    global ORDER
    ORDER = 's'
    ra = np.argsort(rides)
    global cars, cars_sorted
    cars = [Car(i) for i in range(F)]
    cars_sorted = [cars[i] for i in range(F)]
    for i in range(N):
        next_car = heapq.heappop(cars_sorted)
        temp_cars = [next_car]
        while next_car.can_take_ride(rides[ra[i]]) == 0:
            if len(cars_sorted) == 0:
                break
            next_car = heapq.heappop(cars_sorted)
            temp_cars.append(next_car)

        if next_car.can_take_ride(rides[ra[i]]) > 0:
            next_car.add_ride(rides[ra[i]])
        for c in temp_cars:
            heapq.heappush(cars_sorted, c)

def strat_early_not_stupid_nazi():
    global ORDER
    ORDER = 's'
    ra = np.argsort(rides)
    global cars, cars_sorted
    cars = [Car(i) for i in range(F)]
    cars_sorted = [cars[i] for i in range(F)]
    for i in range(N):
        next_car = heapq.heappop(cars_sorted)
        temp_cars = [next_car]
        while next_car.can_take_ride(rides[ra[i]]) != 2:
            if len(cars_sorted) == 0:
                break
            next_car = heapq.heappop(cars_sorted)
            temp_cars.append(next_car)

        if next_car.can_take_ride(rides[ra[i]]) == 2:
            next_car.add_ride(rides[ra[i]])
        else:
            for c in temp_cars:
                heapq.heappush(cars_sorted, c)
            next_car = heapq.heappop(cars_sorted)
            temp_cars = [next_car]
            while next_car.can_take_ride(rides[ra[i]]) == 0:
                if len(cars_sorted) == 0:
                    break
                next_car = heapq.heappop(cars_sorted)
                temp_cars.append(next_car)

            if next_car.can_take_ride(rides[ra[i]]) > 0:
                next_car.add_ride(rides[ra[i]])
   

        for c in temp_cars:
            heapq.heappush(cars_sorted, c)



def exe(input_file):
    clean()
    input(input_file)
    strat_early_not_stupid_nazi()
    out = 'data/early_not_stupid_nazi/'
    utils.ensure_dir(out)
    save_cars(out+input_file+'_out')

if __name__ == "__main__":
    exe(FILE_1)
    exe(FILE_2)
    exe(FILE_3)
    exe(FILE_4)
    exe(FILE_5)

