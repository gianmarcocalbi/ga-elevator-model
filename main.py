import numpy as np
import time
from ga import *

SETTINGS = {}

DEBUG = False

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
        # movimento da un piano ad un altro
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

    def isIdle(self):
        return [v for (_,v) in self.timer.items()].count(-1) == len(self.timer)

    def isEmpty(self):
        return len(self.passenger) == 0

    def updateDirection(self):
        if self.current_floor <= self.destination_floor:
            self.direction = 'up'
        else:
            self.direction = 'down'
            
    def updateDestinationFloor(self, destination_floor=None):
        if destination_floor == None:
            if self.direction == 'up':
                destination_floor = 0
                for p in self.passenger:
                    if p.destination_floor > destination_floor:
                        destination_floor = p.destination_floor
            elif self.direction == 'down':
                destination_floor = self.floors_amount-1
                for p in self.passenger:
                    if p.destination_floor < destination_floor:
                        destination_floor = p.destination_floor
            else:
                raise Exception("Elevator direction is neither up nor down")
                
        self.destination_floor = destination_floor
        self.updateDirection()
    
    def moveToStop(self):
        self.timer["move_to_stop"] = SETTINGS["elevator"]["timing"]["move_to_stop"]
        
    def stopToMove(self):
        self.timer["stop_to_move"] = SETTINGS["elevator"]["timing"]["stop_to_move"]
        
    def move(self):
        self.timer["moving"] = SETTINGS["elevator"]["timing"]["moving"]
    
class egc:
    def __init__(self):
        self.floor_queue = []
        self.elevator = []
        self.new_calls = False
        self.assignement = []
        
        self.nf = SETTINGS["floors_amount"]
        self.nc = SETTINGS["shafts_amount"]

        for _ in range(self.nc):
            self.elevator.append(elevator(self.nf, SETTINGS["elevator"]["capacity"]))
            
        for _ in range(len(self.floor_queue)):
            self.floor_queue.append([])
    
    def step(self):
        el_id = 0
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
                        
                        # flags:
                        # True if there is one or more incoming up calls at the
                        # current floor for the current elevator
                        up_call = False
                        # the same for incoming down calls
                        down_call = False
                        
                        # if the current floor is the lowest
                        if el.current_floor == 0:
                            # then check only up calls
                            # if that call is assigned to current el
                            if self.assignement[el.current_floor] == el_id:
                                # then set flag to true
                                up_call = True
                                
                        # if the current floor is the highest
                        elif el.current_floor == el.floors_amount-1:
                            # then check only down calls
                            if self.assignement[el.current_floor+len(self.assignement)/2] == el_id:
                                down_call = True
                        
                        # else, that is current_floor is neither the lowest nor the highest
                        else:
                            # then check for both up and down calls
                            if self.assignement[el.current_floor] == el_id:
                                up_call = True
                            if self.assignement[el.current_floor+len(self.assignement)/2] == el_id:
                                down_call = True
                        
                        # if there is one or more passenger in the elevator who need to get off
                        # or if there are up or down calls at the current floor
                        if [p.destination_floor for p in el.passenger].count(el.current_floor) > 0 or up_call or down_call:
                            # then stop (that is decelerate, stop and open doors)
                            el.moveToStop()
                        else:
                            # else conitnue moving upward or downward
                            el.move()
                        
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
                        raise KeyError("Unknown elevator timer key in step function")
                
                if el.timer[key] >= 0:
                    el.timer[key] -= 1
            el_id += 1
        
        #Se abbiamo nuove chiamate:
        if self.new_calls:
            # Passive Time
            pt = 1 ################################## TODO
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
            
            self.assignement = ga(self.nf, self.nc, pt, it, hcu, hcd, cf, cdf).computeSolution()
            self.new_calls = False
            self.updateElevatorsDestinationFloor()

        for el in self.elevator:
            if el.isIdle():
                if el.destination_floor != el.current_floor:
                    el.stopToMove()
                

    def updateElevatorsDestinationFloor(self):
        for i in range(len(self.elevator)):
            el = self.elevator[i]
            el_id = i
            if el.isEmpty():
                el_call = []
                el_call_distance = []
                for j in range(len(self.assignement)):
                    call_el_id = self.assignement[j]
                    """
                    [ -1, -1, +0, -1, -1 |||| -1, -1, -1, -1, +1 ]
                    """
                    if call_el_id == el_id:
                        # se j < len(...) allora è nella prima metà dell'assignement
                        # quindi il piano della chiamta è semplicemente j
                        call_floor = j
                        # altrimenti se j è nella seconda metà degli assignment,
                        # per trovare il piano effettivo
                        # dobbiamo sottrarre metà della lunghezza dell'array e aggiungere
                        # 1 per trovare il piano reale di chiamata
                        if j >= len(self.assignement)/2:
                            call_floor = j - len(self.assignement)/2 + 1
                        
                        el_call.append(call_floor)
                        el_call_distance.append(abs(el.current_floor - call_floor))
                el.updateDestinationFloor(el_call[el_call_distance.index(min(el_call_distance))])
            else:
                el.updateDestinationFloor()
        
        
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
    def __init__(self):
        self.egc = egc()
    
    # pass di tempo discreto da t a t+1
    def step(self):
        # generazione passeggeri
        origin = np.random.randint(SETTINGS["floors_amount"])
        destination = np.random.randint(SETTINGS["floors_amount"])
        while destination == origin:
            destination = np.random.randint(SETTINGS["floors_amount"])
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
    
    SETTINGS = {
        "shafts_amount" : 3,
        "floors_amount" : 10,
        "elevator" : {
            "capacity" : 5,
            "timing" : { # in seconds
                # movimento da un piano ad un altro
                'moving' : 3,
                
                # decelerazione + apertura_porte
                'move_to_stop' : 3,
                
                # chiusura_porte + accelerazione
                'stop_to_move' : 3,
                
                # caricamento_passeggeri + selezione_piano
                'loading' : 5,
                
                # scaricamento passeggeri
                'unloading' : 3
            }
        },
        "passenger" : {
            "max_waiting_time" : 300 # secondi
        }
    }
    
    model = model()
    model.start()