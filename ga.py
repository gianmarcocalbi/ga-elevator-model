import numpy as np
import math
import statistics

class ga:
    MAX_POPULATION_SIZE = 50
    population = []
    individual = np.zeros(10)
    chromosome_length = 0
    
    def __init__(self, NF, NC, PT, IT, HC, CF, CDF):
        self.NF = NF
        self.NC = NC
        self.PT = PT
        self.IT = IT
        self.HC = HC
        self.CF = CF
        self.CDF = CDF
        self.K = self.HC[0].count(1) + self.HC[1].count(1)
        
    def generateInitialPopulation(self):
        """N = max(
            MAX_POPULATION_SIZE,
            pow(self.NC, (self.HC[0].count(1) + self.HC[1].count(1)))
        )"""
        N = self.MAX_POPULATION_SIZE
        
        initialPopulation = []
        
        for n in range(N):
            p = [[],[]]
            for i in range(len(self.HC[0])):
                if self.HC[0][i] == 1:
                    p[0].append(np.random.randint(0, self.NC))
                else:
                    p[0].append(-1)
                    
                if self.HC[1][i] == 1:
                    p[1].append(np.random.randint(0, self.NC))
                else:
                    p[1].append(-1)
            initialPopulation.append(p)
        return initialPopulation
    
    def fitness(self, individual):
        fitness_value = 0
        direction = ''
        NF = self.NF #number of floors N
        NC = self.NC #number of cars C
        PT = self.PT #passive_time: the car stops at a floor
        HC = self.HC #hall call floors: from 1 to K
        CF = self.CF #car floor: value in [1,N]
        CDF = self.CDF #car destination floor: from 1 to N
        K = self.K #landing calls
        T = [] #estimated waiting_time for each call i: from 1 to K
        
        Tavg = 0
        
        for i in range(len(HC)):
            Ti = 0
            if direction == 'up' or direction == 'stop':
                if HC[i] >= self.CF[]:
            
            Tavg += Ti/K
        

        
        return fitness_value
    
    
    def run(self):
        population = self.generateInitialPopulation()
        i = 0
        alpha = 0.5
        countEval = 0
        
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

class hallcall:
    def __init__(self):
        
        pass
   
if __name__ == '__main__':
    # random seed
    # 6 piani
    NF = 6 #Number of floors
    NC = 2 #Number of cars
    PT = 1 #Passive Time
    IT = 3 #Inter floor trip time
    HC = ( #[HC1... HCi ... HCK] Hall call floors di dimensione (6-1)*2
        (1,0,0,0,0),
        (0,1,1,1,0)
    )
    HC = (       ###da sistemare ASSOLUTAMENTE Sì
        (1,0),
        (0,1),
        (1,0),
        (1,0),
        (0,0),
        (0,0)    
    )
    CF = [3,5] #[CF1...CFn...CFN] Car floors
    CDF = [1,6] #[CDF1 …CDFn .....CDFN] Car destination floors
    
    ga = ga(NF, NC, PT, IT, HC, CF, CDF)
    
    print(ga.generateInitialPopulation())
    
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