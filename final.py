import math 
import random 
import numpy as np 
import copy

class Evolutionary_Algorithm:
    def __init__(self, mutation_rate, no_generations, no_offsprings, pop_size, p_scheme = 5, c_scheme = 1, maximize = True):
        self.mutation_rate = mutation_rate
        self.no_generations = no_generations
        self.no_offsprings = no_offsprings
        self.pop_size = pop_size
        self.maximize = maximize
        self.p_scheme = p_scheme
        self.c_scheme = c_scheme
        self.selection_schemes = {1: self.FitnessProportionalSelection, 
                                    2: self.RankBasedSelection,
                                    3: self.BinaryTournament, 
                                    4: self.Truncation,
                                    5: self.Random}


    def fitness_stats(self, Cg): 

        fit = [self.fitness(i) for i in Cg]
        if self.maximize:
            return sum(fit) / len(Cg), max(fit)

        return sum(fit) / len(Cg), min(fit) # BFS, AFS 

    def parent_selection(self, Cg): 
        
        fitness_list = [self.fitness(i) for i in Cg]
        p1 = self.selection_schemes[self.p_scheme](Cg, fitness_list)
        fitness_list.remove(self.fitness(p1))
        Cg.remove(p1) # Remove the first one so that the same is not selected again 
        p2 = self.selection_schemes[self.p_scheme](Cg, fitness_list)
        return p1, p2


        
    def FitnessProportionalSelection(self, Cg, fitness_list = None): 
        # FPS selection scheme 
        if fitness_list == None:
            fitness_list = [fitness_list(i) for i in Cg]

        if not self.maximize:
            fitness_list = [1/i for i in fitness_list]
       
        total_fitness = sum(fitness_list)
        normalized_fitness = [i/total_fitness for i in fitness_list]
        range_ = []

        for i in range(len(normalized_fitness)): 
            if i == 0: 
                range_.append((0, normalized_fitness[i]))
            elif i == len(normalized_fitness) - 1: 
                range_.append((range_[-1][-1], 1))
            else: 
                range_.append((range_[-1][-1], range_[-1][-1] + normalized_fitness[i]))

        x = random.random() # check the range to which it belongs 
        for i in range(len(range_)): 
            if range_[i][1] > x >= range_[i][0]:
                return Cg[i]

    def RankBasedSelection(self, Cg, fitness_list = None): 
        # RBS Selection scheme 
        if fitness_list == None:
            fitness_list = [self.fitness(i) for i in Cg]
            
        if not self.maximize:
            fitness_list = [1/i for i in fitness_list]

        sorted_fit = sorted(fitness_list)
        total_rank = sum(i+1 for i in range(len(fitness_list)))
        normalized_fitness = []

        for i in fitness_list: 
            normalized_fitness.append((sorted_fit.index(i) + 1) / total_rank)

        range_ = []
        for i in range(len(normalized_fitness)): 
            if i == 0: 
                range_.append((0, normalized_fitness[i]))
            elif i == len(normalized_fitness) - 1: 
                range_.append((range_[-1][-1], 1))
            else: 
                range_.append((range_[-1][-1], range_[-1][-1] + normalized_fitness[i]))
                
        x = random.random()
        for i in range(len(range_)): 
            if range_[i][1] > x >= range_[i][0]:
                return Cg[i]

    def BinaryTournament(self, Cg, fitness_list = None): 
        # BT selection scheme 
        c1, c2 = random.randint(0, len(Cg)-1), random.randint(0, len(Cg)-1)
        if self.maximize:
            if fitness_list == None:
                if self.fitness(Cg[c1]) > self.fitness(Cg[c2]):
                    return Cg[c1]
                return Cg[c2]
            else:   
                if fitness_list[c1] > fitness_list[c2]:
                    return Cg[c1]
                return Cg[c2]
        else:
            if fitness_list == None:
                if self.fitness(Cg[c1]) <= self.fitness(Cg[c2]):
                    return Cg[c1]
                return Cg[c2]
            else:
                if fitness_list[c1] <= fitness_list[c2]:
                    return Cg[c1]
                return Cg[c2]
        

    def Truncation(self, Cg, fitness_list = None ):
        # Return the worst 
        if fitness_list == None: 
            fitness_list = [self.fitness(i) for i in Cg]

        if self.maximize:
            min_idx = np.argmin(fitness_list)
            return Cg[min_idx]

        max_indx = np.argmax(fitness_list)
        return Cg[max_indx]

    def Random(self, Cg, fitness_list = None): 
        return Cg[random.randint(0, len(Cg) - 1)]

    def New_Generation(self, Cg): 
        while len(Cg) != self.pop_size: 
            Cg.remove(self.selection_schemes[self.c_scheme](Cg))
        return Cg

    def EA_Cycle(self):

        BSF = [] 
        ASF = [] 
        g = 0 
        Cg = self.initialize_population() 
        
        for i in range(self.no_generations): 
            
            p1, p2 = self.parent_selection(Cg) 
            
            offsprings = self.cross_over(p1, p2) 
            
            offsprings = [self.mutate_offspring(i) for i in offsprings]
            
            Cg += offsprings
            Cg = self.New_Generation(Cg)
            g += 1 
            fitness_stats_ = self.fitness_stats(Cg)
           
            ASF.append(fitness_stats_[0])
            BSF.append(fitness_stats_[1])
      
        return BSF, ASF 







