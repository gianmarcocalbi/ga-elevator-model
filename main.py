import numpy as np
import time

class passenger:
    origin_floor = 0
    destination_floor = 0
    birth_time = 0
    max_waiting_time = 9999
    quit_time = 0
    def __init__(self, origin_floor, destination_floor, birth_time=time.time()):
        self.destination_floor = destination_floor
        self.birth_time = birth_time
        self.quit_time = birth_time + self.max_waiting_time
        self.origin_floor = origin_floor

class elevator:
    direction = 'up'
    curr_floor = 0
    capacity = 0
    floors_amount = 0
    passenger = []
    def __init__(self, floors_amount, capacity):
        self.capacity = capacity
        self.floors_amount = floors_amount

class egc:
    floor = ()
    elevator = ()
    
    def __init__(self, settings):
        self.floor = np.zeros(settings["floors_amount"])
        self.elevator = np.zeros(settings["shafts_amount"])

        for i in range(settings["shafts_amount"]):
            self.elevator[i] = elevator(settings["floors_amount"], settings["capacity"])
            
        for i in range(len(self.floor)):
            self.floor[i] = []
    
    def gaStep(self):
        pass
    
class model:
    time = 0
    settings = {}
    def __init__(self):
        settings = {
            "shafts_amount" : 3,
            "floors_amount" : 10,
            "elevator" : {
                "capacity" : 5
            },
            "passenger" : {
                "max_waiting_time" : 300 # secondi
            }
        }
        self.egc = egc(settings)
    
    # pass di tempo discreto da t a t+1
    def step(self):
        # generazione passeggeri
        origin = np.random.randint(self.settings["floors_amount"])
        destination = np.random.randint(self.settings["floors_amount"])
        while destination == origin:
            destination = np.random.randint(self.settings["floors_amount"])
        p = passenger(origin, destination)
        self.egc.floor[origin].append(p)
        
        self.egc.gaStep()
    
    # lancia gli step in successione
    def start(self):
        while (time < 1000): #temp
            self.step()
            time += 1

if __name__ == '__main__':
    # random seed
    np.random.seed(0)
    model = model()
    model.start()