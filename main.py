import numpy as np
import time
from ga import *


class passenger:
    origin_floor = 0
    destination_floor = 0
    birth_time = 0
    MAX_WAITING_TIME = 9999
    quit_time = 0
    def __init__(self, origin_floor, destination_floor, birth_time=time.time()):
        self.destination_floor = destination_floor
        self.birth_time = birth_time
        self.quit_time = birth_time + self.MAX_WAITING_TIME
        self.origin_floor = origin_floor

class elevator:
    direction = 'up'
    is_moving = False
    current_floor = 0
    capacity = 0
    floors_amount = 0
    destination_floor = 0
    passenger = []
    
    timer = {
        'moving' : -1,
        
        # decelerazione + apertura_porte
        'move_to_stop' : -1,
        
        # chiusura_porte + accelerazione
        'stop_to_move' : -1,
        
        # caricamento_passeggeri + selezione_piano
        'loading' : -1,
        
        # scaricamento passeggeri
        'unloading' : -1
    }
    
    def __init__(self, floors_amount, capacity):
        self.capacity = capacity
        self.floors_amount = floors_amount

    
class egc:
    def __init__(self, settings):
        self.floor_queue = []
        self.elevator = []
        self.nf = settings["floors_amount"]
        self.nc = settings["shafts_amount"]

        for _ in range(self.nc):
            self.elevator.append(elevator(self.nf, settings["elevator"]["capacity"]))
            
        for _ in range(len(self.floor_queue)):
            self.floor_queue.append([])
    
    def step(self):
        
        for el in self.elevator:
            for key in el.timer:
                if el.timer[key] == 0:
                    if key == 'moving':
                        if el.direction == 'up':
                            el.current_floor += 1 
                        elif el.direction == 'down':
                            el.current_floor -= 1
                        else:
                            raise Exception("Unknown elevator direction")
                            
                        # TODO: scegliere l'azione da intraprendere    
                        
                    elif key == 'move_to_stop':
                        el.is_moving = False
                        # TODO: scegliere l'azione da intraprendere
                        # load / unload
                        
                    elif key == 'stop_to_move':
                        el.is_moving = True
                        # azione di movimento
                        # el.move()
                        # cioè el.timer['moving'] = K
                        
                    elif key == 'loading':
                        # p = self.floor_queue[el.current_floor].dequeue()
                        # el.passenger.append(p)
                        # el.timer['stop_to_move'] = H
                        pass
                        
                    elif key == 'unloading':
                        # p = el.passenger.dequeue()
                        # self.floor_queue[el.current_floor].enqueue(p)
                        # el.timer['move_to_stop'] = L
                        pass
                        
                    else:
                        raise KeyError("Unknown timer key")
                
                if el.timer[key] >= 0:
                    el.timer[key] -= 1
        
        """
        # Passive Time
        pt = 1
        # Inter floor trip time
        it = 3
        
        # Hall call UP/DOWN
        hcu = np.zeros(self.nf)
        hcd = np.zeros(self.nf)
        f = 0
        for p_waiting_at_f in self.floor_queue:
            for p in p_waiting_at_f:
                if p.destination_floor > p.origin_floor:
                    hcu[f] = 1
                elif p.destination_floor < p.origin_floor:
                    hcd[f] = 1
                else:
                    raise Exception("Passenger destination_floor == origin_floor")
            f += 1

        cf = []
        cdf = []
        for el in self.elevator:
            cf.append(el.current_floor)
            cdf.append(el.destination_floor)
        
        call_assignement = ga(self.nf, self.nc, pt, it, hcu, hcd, cf, cdf).computeSolution()
        """
        
        """
        
        each elevator:
            if an action is running
                - incrementare/decrementare tempi di attesa vari
                - diminuire spazio disponibile in elevator per ogni salita
            else:
                - intraprende un'azione
        egc:
            - modificare la floor_queue
        each passenger:
            if destination_floor != 0:    
                if quit_time < MAX_WAITING_TIME:
                    - incrementa waiting_time
                else
                    quitta_male()
            else:
                -settare destination_floor
        if new calls
            run genetic algorithm        
                
        
        decrementare i timer
        se qualche timer è scaduto -> compi l'azione
        imposta tutti i timer per le azioni successive
        nuove chiamate? ricalcola gli assegnamenti
        """
class model:
    time = 0
    settings = {}
    def __init__(self):
        self.settings = {
            "shafts_amount" : 3,
            "floors_amount" : 10,
            "elevator" : {
                "capacity" : 5
            },
            "passenger" : {
                "max_waiting_time" : 300 # secondi
            }
        }
        self.egc = egc(self.settings)
    
    # pass di tempo discreto da t a t+1
    def step(self):
        # generazione passeggeri
        origin = np.random.randint(self.settings["floors_amount"])
        destination = np.random.randint(self.settings["floors_amount"])
        while destination == origin:
            destination = np.random.randint(self.settings["floors_amount"])
        p = passenger(origin, destination)
        self.egc.floor_queue[origin].append(p)
        
        self.egc.step()
    
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