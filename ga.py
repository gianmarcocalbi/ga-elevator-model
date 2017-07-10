import numpy as np
import math
import statistics

class ga:
    MAX_POPULATION_SIZE = 50
    
    def __init__(self, nf, nc, pt, it, hcu, hcd, cf, cdf):
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
        """N = max(
            MAX_POPULATION_SIZE,
            pow(self.NC, (self.HC[0].count(1) + self.HC[1].count(1)))
        )"""
        N = self.MAX_POPULATION_SIZE
        
        initialPopulation = []
        
        for n in range(N):
            pU = []
            pD = []
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
        nf = self.nf #number of floors N
        nc = self.nc #number of cars C
        pt = self.pt #passive_time: the car stops at a floor
        hcu = self.hcu #hall call floors: from 1 to K
        hcd = self.hcd #hall call floors: from 1 to K
        cf = self.cf #car floor: value in [1,N]
        cdf = self.cdf #car destination floor: from 1 to N
        k = self.k #landing calls

        # minimum number of stops between between hall call
        # floor and car floor assigned to that call
        ns = np.ones(len(hcu)*2) # temp value
        
        Tavg = 0
        for hcf in self.hc_index["up"]:
            # hcf = current hall call floor
            car = individual[hcf] # car assigned to current hc
            T = 0
            # if HCi >= CFn
            if hcf >= cf[car]:
                # if car is stopped or going up, that is:
                # destination >= current floor
                if cdf[car] >= cf[car]:
                    T = (hcf-cf[car])*self.it+ns[hcf]*self.pt
                else:
                    T = (cf[car]-hcf)*self.it+ns[hcf]*self.pt
            else:
                if cdf[car] >= cf[car]:
                    T = (nf-cf[car]+nf-1+hcf-1)*self.it+ns[hcf]*self.pt
                else:
                    T = (cf[car]-1+nf-1+nf-hcf)*self.it+ns[hcf]*self.pt
            Tavg += T/k

        for hcf in self.hc_index["down"]:
            # hcf = current hall call floor
            car = individual[hcf+nf-1] # car assigned to current hc
            T = 0
            # if car is stopped or going up, that is:
            # destination >= current floor
            if cdf[car] >= cf[car]:
                T = (nf-cf[car]+nf-hcf)*self.it+ns[hcf]*self.pt
            else:
                T = (cf[car]-1+hcf-1)*self.it+ns[hcf]*self.pt
            Tavg += T/k

        
        return 1/Tavg
    
    
    def run(self):
        population = self.generateInitialPopulation()
        i = 0
        alpha = 0.5
        countEval = 0
        """
        while i < maxIteration:
            offspring = []
            fitness_dict = {}
            # fitness
            while len(offspring) < len(population):
                alpha = sqrt((1-i)/maxIteration)/2
                p1_index, p2_index = roulette()
                p1 = population[p1_index]
                p2 = population[p2_index]
                c = crossover(p1,p2)
                c = mutation(c)
                new_population.append(c)
                countEval += 1
                
            population = offspring
            variance = statistics.variance(population)
            thres = i*variance*(2/math.sqrt(countEval))
            if termination():
                break
            
            i += 1
        
        return best_individual(population)
        """
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
    hcu = (0,1,0,0,0)
    hcd = (0,0,0,0,0)

    # Car Floors: floors where ith car is
    cf = [3,1]

    # Car destination floors: floors where car are going to
    cdf = [1,6]
    
    ga = ga(nf, nc, pt, it, hcu, hcd, cf, cdf)

    print(ga.fitness([-1,1,-1,-1,-1,-1,-1,-1,-1,-1]))
    print(ga.fitness([-1,0,-1,-1,-1,-1,-1,-1,-1,-1]))

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