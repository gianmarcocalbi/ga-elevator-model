import numpy as np

class car:
    floor = 0
    pass

class elevator:
    def __init__(self, shaft_height):
        self.car = car()
    pass

class egc:
    def __init__(self, height, shafts_amount):
        self.floors = np.zeros(height)
        self.elevators = []

        for i in range(shafts_amount):
            self.elevators.append(elevator(height))
