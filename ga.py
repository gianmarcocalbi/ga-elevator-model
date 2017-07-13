# -*- coding: utf-8 -*-

import numpy as np
import math
#import statistics
from sklearn import preprocessing
import warnings
warnings.filterwarnings("ignore")

class ga:
    def __init__(self, nf, nc, pt, it, hcu, hcd, cf, cdf):
        self.MAX_POPULATION_SIZE = 50
        self.MAX_GA_ITERATIONS = 100
        self.MUTATION_PROB = 0.01
        self.CROSSOVER_PROB = 0.7
        
        self.nf = nf
        self.nc = nc
        self.pt = pt
        self.it = it
        self.hcu = hcu
        self.hcd = hcd
        self.cf = cf
        self.cdf = cdf
        self.k = self.hcu.count(1) + self.hcd.count(1)

        self.hc_index = {
            'up' : [],
            'down' : []
        }
        for j in range(nf-1):
            if self.hcu[j] == 1:
                self.hc_index["up"].append(j)
            if self.hcd[j] == 1:
                self.hc_index["down"].append(j)
        
    def generateInitialPopulation(self):
        """
        N = max(
            MAX_POPULATION_SIZE,
            pow(self.NC, (self.HC[0].count(1) + self.HC[1].count(1)))
        )
        """
        N = self.MAX_POPULATION_SIZE
        
        initialPopulation = []
        
        for n in range(N):
            pU = [] #population that goes up
            pD = [] #population that goes down
            for i in range(self.nf-1):
                if self.hcu[i] == 1:
                    pU.append(np.random.randint(0, self.nc))
                else:
                    pU.append(-1)
                    
                if self.hcd[i] == 1:
                    pD.append(np.random.randint(0, self.nc))
                else:
                    pD.append(-1)
                    
            initialPopulation.append(pU+pD)
            
        return initialPopulation

    def fitness(self, individual):
        pt = self.pt #passive_time: the car stops at a floor
        it = self.it
        NF = self.nf
        
        # minimum number of stops between between hall call
        # floor and car floor assigned to that call
        ns = np.ones(len(self.hcu)*2) # temp value, TO FIX
        
        Tavg = 0
        for hcf in self.hc_index["up"]:
            # hcf = current hall call floor
            car = individual[hcf] # car assigned to current hc
            T = 0
            HCi = hcf
            CFn = self.cf[car]
            NSi = ns[hcf]
            if HCi >= CFn:
                # if car is stopped or going up, that is:
                # destination >= current floor
                if self.cdf[car] >= CFn:
                    T = (HCi-CFn)*it+NSi*pt
                else:
                    T = (CFn-HCi)*it+NSi*pt
            else:
                if self.cdf[car] >= CFn:
                    T = (NF-CFn+NF-1+HCi-1)*it+NSi*pt
                else:
                    T = (CFn-1+NF-1+NF-HCi)*it+NSi*pt
            Tavg += T/self.k
            
        for hcf in self.hc_index["down"]:
            # hcf = current hall call floor
            car = individual[hcf+self.nf-1] # car assigned to current hc
            T = 0
            HCi = hcf
            CFn = self.cf[car]
            NSi = ns[hcf]
            # if car is stopped or going up, that is:
            # destination >= current floor
            if self.cdf[car] >= CFn:
                T = (NF-CFn+NF-HCi)*it+NSi*pt
            else:
                T = (CFn-1+HCi-1)*it+NSi*pt
            Tavg += T/self.k
        
        if Tavg == 0:
            return 0
        return 1/Tavg
    
    def roulette(self, population, fitness_dict):
        PROB = np.zeros(len(population))
        for i in range(len(population)):
            key = "".join(str(x) for x in population[i])
            PROB[i] = fitness_dict[key]
        
        PROB = preprocessing.normalize(PROB, norm='l1')[0]
        
        X = np.random.rand()
        cumulative_p = 0
        for i in range(len(PROB)):
            cumulative_p += PROB[i]
            if cumulative_p >= X:
                return i
        
        raise Exception("Roulette failed (this error should never occur)")
    
    def crossover(self, parent1, parent2, prob):
        child = parent1
        if np.random.rand() >= 0.5:
            child = parent2
        
        if np.random.rand() <= prob:
            if np.random.rand() <= prob:
                # 1 pto di crossover
                x = np.random.randint(len(parent1))
                if np.random.rand() >= 0.5:
                    child = parent1[0:x] + parent2[x:len(parent1)]
                else:
                    child = parent2[0:x] + parent1[x:len(parent1)]
            else:
                # 2 pti di crossover
                x1 = np.random.randint(len(parent1))
                x2 = np.random.randint(len(parent1))
                x1 = min(x1,x2)
                x2 = max(x1,x2)
                if x1 != x2:
                    if np.random.rand() >= 0.5:
                        child = parent1[0:x1] + parent2[x1:x2] + parent1[x2:len(parent1)]
                    else:
                        child = parent2[0:x1] + parent1[x1:x2] + parent2[x2:len(parent1)]
                else:
                    x = x1
                    if np.random.rand() >= 0.5:
                        child = parent1[0:x] + parent2[x:len(parent1)]
                    else:
                        child = parent2[0:x] + parent1[x:len(parent1)]
                    
        return child
    
    def mutation(self, chromosome, prob):
        if np.random.rand() <= prob and self.nc > 1:
            indexes = []
            for i in range(len(chromosome)):
                if chromosome[i] != -1:
                    indexes.append(i)
                    
            x = indexes[np.random.randint(len(indexes))]
            car = list(range(self.nc))
            car.remove(chromosome[x])
            chromosome[x] = car[np.random.randint(len(car))]
            
        return chromosome
    
    def computeSolution(self):
        population = self.generateInitialPopulation()
        i = 0
        alpha = 0.5
        fitness_dict = {}
        
        while i < self.MAX_GA_ITERATIONS:
            offspring = []
            # fitness
            for j in range(len(population)):
                x = population[j]
                
                #    [-1,1,-1,-1,-1,-1,-1,-1,-1,-1] ->
                # -> "-11-1-1-1-1-1-1-1-1"
                key = "".join(str(_) for _ in x)
                if key not in fitness_dict:
                    fitness_dict[key] = self.fitness(x)
            
            while len(offspring) < len(population):
                #alpha = math.sqrt((1-i)/maxIteration)/2
                
                parent1_index = self.roulette(population, fitness_dict)
                parent2_index = self.roulette(population, fitness_dict)
                
                parent1 = population[parent1_index]
                parent2 = population[parent2_index]
                
                child = self.crossover(parent1, parent2, self.CROSSOVER_PROB)
                child = self.mutation(child, self.MUTATION_PROB)
                
                offspring.append(child)
                
            population = offspring
            #variance = statistics.variance(population)
            #thres = i*variance*(2/math.sqrt(countEval))
            
            #if termination():
                #break
                
            i += 1
            
            ###############################################################temp
            if i == self.MAX_GA_ITERATIONS:
                count = []
                obj = []
                for j in range(len(population)):
                    if population[j] not in obj:
                        obj.append(population[j])
                        count.append(1)
                    else:
                        count[obj.index(population[j])] += 1
                return obj[count.index(max(count))]
            
            """if i == self.MAX_GA_ITERATIONS:
                ret = []
                for j in population:
                    if j not in ret:
                        print(str(j) + " ==> " + str(fitness_dict["".join(str(_) for _ in j)]))
            """          
            
        #return best_individual(population)
        
class hallcall:
    def __init__(self):
        pass

if __name__ == '__main__':
    # random seed
    np.random.seed(0)

    # Number of floors
    nf = 6
    # Number of cars (e.g. elevators)
    nc = 2
    # Passive Time
    pt = 1
    # Inter floor trip time
    it = 3

    # Hall call UP/DOWN
    hcu = (0,0,0,0,1)
    hcd = (0,0,1,0,1)

    # Car Floors: floors where i-th car is
    cf = [3,5]

    # Car destination floors: floors where car are going to
    cdf = [3,5]
    
    ga = ga(nf, nc, pt, it, hcu, hcd, cf, cdf)
    print(ga.computeSolution())
    #print(ga.fitness([-1,1,-1,-1,-1,-1,-1,-1,-1,-1]))
    #print(ga.fitness([-1,0,-1,-1,-1,-1,-1,-1,-1,-1]))

    p1 = [-1,1,0,-1,1,-1,1,-1,-1,1]
    p2 = [-1,0,-1,-1,0,-1,1,-1,0,-1]
    
    #for i in range(10):
    #    print(ga.mutation(p1, 0.9))

    #print(ga.generateInitialPopulation())
    
    """
    il Genetic Algorithm riceve una serie di parametri tra cui HC, cioè le Hall Call
    che indicano per ogni piano se c'è una chiamata UP e/o DOWN
    restituisce una soluzione di assegnamento, cioè per ogni chiamata quale ascensore
    la dovrà servire.
    La computazione del ga è effettuata ad ogni step. Dopo che il ga restituisce una
    soluzione si decide per ogni ascesore che movimento fare: UP di un piano,
    DOWN di un piano, STOP (per far salire le persone).
    La soluzioni per le chiamate in attesa vengono ricalcolate TUTTE ogni volta che
    c'è una nuova chiamata
    """