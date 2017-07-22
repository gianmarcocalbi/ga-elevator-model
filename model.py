# -*- coding: utf-8 -*-

import time
import ga
import names
import numpy as np
import traceback


SETTINGS = {}


STATS = {
    "waiting_time" : [],
    "riding_time" : [],
    "total_time" : []
}

DEBUG = False

TIME = 0

class passenger:
    id_counter = 0
    def __init__(self, origin_floor, destination_floor, name, birth_time=time.time()):
        self.MAX_WAITING_TIME = 9999
        self.destination_floor = destination_floor
        self.birth_time = birth_time
        self.get_on_time = 0
        self.name = name
        self.quit_time = birth_time + self.MAX_WAITING_TIME
        self.origin_floor = origin_floor
        self.id_counter += 1
        self.pid = self.id_counter

        if destination_floor > origin_floor:
            self.direction = "up"
        else:
            self.direction = "down"


class elevator:
    def __init__(self, _id, floors_amount, capacity, signals):
        self.direction = 'up'
        self.is_moving = False
        self.current_floor = 0
        self.destination_floor = 0
        self.passenger = []
        self._id = _id
        self.signals = signals

        self.timer = {
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

        self.capacity = capacity
        self.floors_amount = floors_amount


    def getAction(self):
        action = None
        for (key,val) in self.timer.items():
            if val >= 0 and action is None:
                action = key
            elif val > 0:
                action = key
        if action is None:
            action = "idle"
        return action


    def isIdle(self):
        return [v for (_,v) in self.timer.items()].count(-1) == len(self.timer)


    def isEmpty(self):
        return len(self.passenger) == 0


    def updateDirection(self):
        if self.current_floor <= self.destination_floor:
            self.direction = 'up'
        else:
            self.direction = 'down'
        self.setHeader()


    def updateDestinationFloor(self, destination_floor=None):
        if destination_floor is None or not (0 <= destination_floor <= self.floors_amount-1):
            """if self.direction == 'up':
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
                raise Exception("Elevator direction is neither up nor down")"""

            max_destination_floor = 0
            min_destination_floor = self.floors_amount-1

            for p in self.passenger:
                if p.destination_floor < self.current_floor:
                    if p.destination_floor < min_destination_floor:
                        min_destination_floor = p.destination_floor

                if p.destination_floor > self.current_floor:
                    if p.destination_floor > max_destination_floor:
                        max_destination_floor = p.destination_floor

            if 0 <= max_destination_floor <= self.floors_amount-1 == min_destination_floor:
                destination_floor = max_destination_floor
            elif max_destination_floor == 0 <= min_destination_floor <= self.floors_amount-1:
                destination_floor = min_destination_floor
            else:
                raise Exception("Elevator direction is neither up nor down")

        self.signals["setElevatorDestinationFloor"].emit(self.destination_floor, destination_floor, self._id)

        self.destination_floor = destination_floor
        self.updateDirection()


    def stop(self):
        self.is_moving = False
        for key in self.timer:
            self.timer[key] = -1
        self.updateDestinationFloor(self.current_floor)
        self.setHeader("idle")



    def getOff(self):
        global TIME
        passenger_index = self.passengersGettingOff()
        if DEBUG:
            print(passenger_index)
        new_passenger = []
        for i in range(len(self.passenger)):
            p = self.passenger[i]
            if i not in passenger_index:
                new_passenger.append(p)
            else:
                STATS["waiting_time"].append(p.get_on_time - p.birth_time)
                STATS["riding_time"].append(TIME - p.get_on_time)
                STATS["total_time"].append(TIME - p.birth_time)
                print(str.format(
                    "> passenger {0} arrived at floor {1} (desired={2}) from {3} in {4} seconds",
                    p.name,
                    str(self.current_floor),
                    str(p.destination_floor),
                    str(p.origin_floor),
                    str(int(TIME-p.birth_time))
                ))

        self.signals["unloadPassengersFromElevator"].emit(self._id, passenger_index)

        self.passenger = new_passenger


    def passengersGettingOff(self, floor=None):
        if floor is None:
            floor = self.current_floor

        getting_off = []
        for i in range(len(self.passenger)):
            p = self.passenger[i]
            if p.destination_floor == floor:
                getting_off.append(i)
        return getting_off


    def setHeader(self, action=None):
        if action is None:
            action = self.getAction().lower()

        action = action.lower()

        if action != "idle":
            action += " (" + str(self.timer[action]) + ")"

        self.signals["setElevatorHeader"].emit(self._id, self.direction, action)


    def load(self):
        self.timer["loading"] = SETTINGS["elevator"]["timing"]["loading"]
        self.setHeader("loading")


    def unload(self):
        self.timer["unloading"] = SETTINGS["elevator"]["timing"]["unloading"]
        self.setHeader("unloading")


    def moveToStop(self):
        self.is_moving = False
        self.timer["move_to_stop"] = SETTINGS["elevator"]["timing"]["move_to_stop"]
        self.setHeader("move_to_stop")


    def stopToMove(self):
        self.is_moving = True
        self.timer["stop_to_move"] = SETTINGS["elevator"]["timing"]["stop_to_move"]
        self.setHeader("stop_to_move")


    def move(self):
        self.is_moving = True
        self.timer["moving"] = SETTINGS["elevator"]["timing"]["moving"]
        self.setHeader("moving")


class egc:
    def __init__(self, signals):
        self.floor_queue = []
        self.elevator = []
        self.new_calls = False
        self.assignment = []

        self.nf = SETTINGS["floors_amount"]
        self.nc = SETTINGS["shafts_amount"]

        self.signals = signals

        for el_id in range(self.nc):
            self.elevator.append(elevator(el_id, self.nf, SETTINGS["elevator"]["capacity"], self.signals))

        for _ in range(self.nf):
            self.floor_queue.append([])

        for _ in range(self.nf-1):
            self.assignment.append(-1)
            self.assignment.append(-1)


    def passengersGettingOn(self, elevator_id):
        up_getting_on = []
        down_getting_on = []

        el = self.elevator[elevator_id]

        if self.assignment[el.current_floor] == elevator_id:
            for i in range(len(self.floor_queue[el.current_floor])):
                p = self.floor_queue[el.current_floor][i]
                if p.destination_floor > el.current_floor:
                    if len(up_getting_on) + len(el.passenger) < el.capacity:
                        up_getting_on.append(i)

        if self.assignment[int(el.current_floor + len(self.assignment)/2)-1] == elevator_id:
            for i in range(len(self.floor_queue[el.current_floor])):
                p = self.floor_queue[el.current_floor][i]
                if p.destination_floor < el.current_floor:
                    if len(down_getting_on) + len(el.passenger) < el.capacity:
                        down_getting_on.append(i)


        dir = ""
        if el.destination_floor == el.current_floor:
            # choose between upgoings and downgoings passsengers
            tmp_time = time.time()
            for p_id in up_getting_on + down_getting_on:
                p = self.floor_queue[el.current_floor][p_id]
                if p.birth_time < tmp_time:
                    tmp_time = p.birth_time
                    dir = p.direction

        if el.destination_floor > el.current_floor or dir == "up":
            return up_getting_on
        elif el.destination_floor < el.current_floor or dir == "down":
            return down_getting_on
        else:
            if len(up_getting_on + down_getting_on) > 0:
                raise Exception("At least one passenger should get on but no one did")

        return []


    def getOn(self, elevator_id):
        passenger_index = self.passengersGettingOn(elevator_id)
        new_floor_queue = []

        el = self.elevator[elevator_id]

        #p_count = {"up": 0, "down": 0}

        for i in range(len(self.floor_queue[el.current_floor])):
            p = self.floor_queue[el.current_floor][i]
            #p_count[p.direction] += 1

            if i not in passenger_index:
                new_floor_queue.append(p)
            else:
                p.get_on_time = TIME
                el.passenger.append(p)
                self.signals["loadPassengerOnElevator"].emit(elevator_id, p.direction, p.destination_floor, p.name)
                self.signals["dequeueFromFloor"].emit(p.origin_floor, p.direction, 0)

        self.floor_queue[el.current_floor] = new_floor_queue


    def step(self):

        for el in self.elevator:
            for key in el.timer:
                if el.timer[key] >= 0:
                    el.timer[key] -= 1

        # elevator ID counter
        el_id = 0

        # loop through every elevator in self.elevator
        for el in self.elevator:
            el.setHeader()
            # loop through every key in el.timer dictionary
            for key in el.timer:
                # timer equal to 0 it means some action have to occur
                if el.timer[key] == 0:
                    el.timer[key] = -1
                    # switch to find which is the key equal to 0

                    # if the key is 'moving'
                    if key == 'moving':
                        # then increment or decremtn the floor with regards to
                        # the direction (up or down respectively)
                        curr_floor = el.current_floor

                        if el.destination_floor > el.current_floor:
                            el.current_floor += 1
                        elif el.destination_floor < el.current_floor:
                            el.current_floor -= 1
                        else:
                            # if the direction is neither up nor down
                            # then do nothing
                            pass

                        self.signals["setElevatorFloor"].emit(curr_floor, el.current_floor, el_id)

                        # if there is one or more passenger in the elevator who need to get off
                        # or if there are up or down calls at the current floor
                        if len(el.passengersGettingOff()) > 0 or len(self.passengersGettingOn(el_id)) > 0:
                            # then stop (that is decelerate, stop and open doors)
                            el.moveToStop()
                        else:
                            # else continue moving upward or downward
                            el.move()

                    elif key == 'move_to_stop':
                        # if there is one or more passenger in the elevator who needs to get off
                        if len(el.passengersGettingOff()) > 0:
                            el.unload()

                        # else if there is one or more passenger who needs to get on 
                        elif len(self.passengersGettingOn(el_id)):
                            el.load()

                    elif key == 'stop_to_move':
                        # azione di movimento
                        el.move()

                    elif key == 'loading':
                        # p = self.floor_queue[el.current_floor].dequeue()
                        # el.passenger.append(p)
                        # el.timer['stop_to_move'] = H
                        self.getOn(el_id)
                        el.stopToMove()

                        if self.assignment[el.current_floor] == el_id:
                            self.assignment[el.current_floor] = -1

                        if self.assignment[int(el.current_floor+len(self.assignment)/2)-1] == el_id:
                            self.assignment[int(el.current_floor + len(self.assignment) / 2) - 1] = -1

                        self.updateElevatorsDestinationFloor()

                    elif key == 'unloading':
                        # p = el.passenger.dequeue()
                        # self.floor_queue[el.current_floor].enqueue(p)
                        # el.timer['move_to_stop'] = L
                        el.getOff()

                        if len(self.passengersGettingOn(el_id)) > 0:
                            el.load()
                            self.updateElevatorsDestinationFloor()
                        elif el.current_floor != el.destination_floor:
                            el.stopToMove()

                    else:
                        raise KeyError("Unknown elevator timer key in step function")
            el_id += 1

        #Se abbiamo nuove chiamate:
        if self.new_calls:
            if DEBUG:
                print("GA will parse new calls")
            # Passive Time
            pt = SETTINGS["elevator"]["timing"]["loading"] + SETTINGS["elevator"]["timing"]["move_to_stop"] + SETTINGS["elevator"]["timing"]["stop_to_move"]
            # Inter floor trip time
            it = SETTINGS["elevator"]["timing"]["moving"]

            # Hall call UP/DOWN
            hcu = []
            hcd = []
            call_flag = False
            for i in range(len(self.floor_queue)):
                queue = self.floor_queue[i]
                if i < len(self.floor_queue)-1:
                    hcu.append(0)
                if i > 0:
                    hcd.append(0)

                for p in queue:
                    call_flag = True
                    if p.destination_floor > p.origin_floor:
                        hcu[i] = 1
                    elif p.destination_floor < p.origin_floor:
                        hcd[i-1] = 1
                    else:
                        raise Exception("Passenger destination_floor == origin_floor")

            cf = []
            cdf = []
            for el in self.elevator:
                cf.append(el.current_floor)
                cdf.append(el.destination_floor)

            try:
                '''
                print(
                    "\n****************************************",
                    "\nhcu=" + str(hcu),
                    "\nhcd=" + str(hcd),
                    "\ncf=" + str(cf),
                    "\ncdf=" + str(cdf),
                    "\n****************************************"
                )
                input()
                '''
                if call_flag:
                    self.assignment = ga.ga(self.nf, self.nc, pt, it, list(hcu), list(hcd), cf, cdf).computeSolution()
            except Exception as e:
                print(
                    "GA error DEBUG",
                    "hcu=" + str(list(hcu)),
                    "hcd=" + str(list(hcd)),
                    "cf=" + str(cf),
                    "cdf=" + str(cdf)
                )
                raise e


            self.new_calls = False
            self.updateElevatorsDestinationFloor()

        for el_id in range(len(self.elevator)):
            el = self.elevator[el_id]
            if el.isIdle():
                if el.destination_floor != el.current_floor:
                    el.stopToMove()
                else:
                    if len(self.passengersGettingOn(el_id)) > 0:
                        el.load()
                    else:
                        for i in range(len(self.floor_queue)):
                            queue = self.floor_queue[i]

                            upgoings = 0
                            downgoings = 0
                            for p in queue:
                                if p.destination_floor > p.origin_floor:
                                    upgoings += 1
                                else:
                                    downgoings += 1

                            if i == 0:
                                up_assign = self.assignment[i]
                                if up_assign == -1 and upgoings > 0:
                                    self.new_calls = True
                                    break

                            elif 0 < i < len(self.floor_queue)-1:
                                down_assign = self.assignment[i + int(len(self.assignment) / 2) - 1]
                                if down_assign == -1 and downgoings > 0:
                                    self.new_calls = True
                                    break
                                up_assign = self.assignment[i]
                                if up_assign == -1 and upgoings > 0:
                                    self.new_calls = True
                                    break

                            elif i == len(self.floor_queue)-1:
                                down_assign = self.assignment[i + int(len(self.assignment) / 2) - 1]
                                if down_assign == -1 and downgoings > 0:
                                    self.new_calls = True
                                    break

    def updateElevatorsDestinationFloor(self):
        for i in range(len(self.elevator)):
            el = self.elevator[i]
            el_id = i
            if el.isEmpty():
                el_call = []
                el_call_distance = []
                for j in range(len(self.assignment)):
                    call_el_id = self.assignment[j]
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
                        if j >= int(len(self.assignment)/2):
                            call_floor = j - len(self.assignment) / 2 + 1

                        el_call.append(call_floor)
                        el_call_distance.append(abs(el.current_floor - call_floor))
                if len(el_call_distance) > 0:
                    el.updateDestinationFloor(int(el_call[el_call_distance.index(min(el_call_distance))]))
                else:
                    el.stop()
            else:
                el.updateDestinationFloor()
        self.signals["setAssignment"].emit(self.assignment)


class model:
    def __init__(self, plotEvent, closeEvent, runEvent, runOnceEvent, signals):
        np.random.seed(SETTINGS["ga"]["seed"])
        self.egc = egc(signals)
        self.plotEvent = plotEvent
        self.closeEvent = closeEvent
        self.runEvent = runEvent
        self.runOnceEvent = runOnceEvent
        self.signals = signals
        self.speed = 0
        ga.SETTINGS = SETTINGS

    # pass di tempo discreto da t a t+1
    def step(self):
        # generazione passeggeri
        self.egc.step()


    # lancia gli step in successione
    def start(self):
        global TIME
        self.signals["setTime"].emit(str(TIME))

        while True:

            if self.closeEvent.is_set():
                return

            if self.plotEvent.is_set():
                self.plotEvent.clear()
                self.signals["plot"].emit(STATS)


            if (self.runEvent.is_set() or self.runOnceEvent.is_set()) and TIME < SETTINGS["total_duration"]:
                start_time = time.time()
                self.runOnceEvent.clear()

                if np.random.rand() <= 0.80 and TIME < 50:
                    dest = np.random.randint(self.egc.nf)
                    orig = np.random.randint(self.egc.nf)
                    check = 0
                    while orig == dest:
                        orig = np.random.randint(self.egc.nf)
                        if check == 100:
                            exit("ERROR")
                        else:
                            check += 1
                    p = passenger(orig, dest, names.get_full_name(), TIME)

                    print(str.format("{0} calls at floor {1} (directed to {2})", p.name, orig, dest))

                    self.egc.floor_queue[orig].append(p)
                    self.egc.new_calls = True

                    self.signals["enqueueAtFloor"].emit(orig, p.direction, p.destination_floor, p.name)

                try:
                    self.step()
                except Exception as e:
                    print(str(e))
                    self.printModel()
                    raise e

                TIME += 1
                self.signals["setTime"].emit(str(TIME))
                end_time = time.time()
                if self.speed/25 - (end_time - start_time) > 0 and self.runEvent.is_set():
                    time.sleep(self.speed/25 - (end_time - start_time))

    def setSpeed(self, speed):
        self.speed = speed

    def printModel(self):
        global TIME

        print("------- MODEL -------")
        print("TIME=" + str(TIME))
        print("ASSIGNEMENT=" + str(self.egc.assignment))

        print("\n------- ELEVATORS -------")
        for i in range(len(self.egc.elevator)):
            el = self.egc.elevator[i]
            p_names = [p.name for p in el.passenger]
            print(str.format("Elevator {0} => current_floor={1} - destination_floor={2} - passengers={3}", i, el.current_floor, el.destination_floor, p_names))
            print("\t" + str(el.timer))

        print("\n------- FLOOR QUEUE -------")
        for i in range(len(self.egc.floor_queue)):
            queue = self.egc.floor_queue[i]
            p_names = []
            for p in queue:
                if p.destination_floor > p.origin_floor:
                    p_names.append(str.format("{0}(▲ {1})", p.name, p.destination_floor))
                else:
                    p_names.append(str.format("{0}(▼ {1})", p.name, p.destination_floor))
            print(str.format("Floor {0} => passengers={1}", i, p_names))


if __name__ == '__main__':

    SETTINGS = {
        "shafts_amount" : 2,
        "floors_amount" : 6,
        "elevator" : {
            "capacity" : 5,
            "timing" : { # in seconds
                # movimento da un piano ad un altro
                'moving' : 3,

                # decelerazione + apertura_porte
                'move_to_stop' : 2,

                # chiusura_porte + accelerazione
                'stop_to_move' : 2,

                # caricamento_passeggeri + selezione_piano
                'loading' : 3,

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