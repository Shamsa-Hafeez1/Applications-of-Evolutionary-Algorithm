import math 
import random 
from final import *
import xlsxwriter
import matplotlib.pyplot as plt

class TravellingSalesPerson(Evolutionary_Algorithm):
    def __init__(self, mutation_rate, no_generations, no_offsprings, pop_size, path, p_scheme, c_scheme, maximize = False ):
        Evolutionary_Algorithm.__init__(self, mutation_rate, no_generations, no_offsprings, pop_size,  p_scheme, c_scheme, maximize)

        file = open(path, 'r')

        Name = file.readline().strip().split()[2]# NAME
        Comment1 = file.readline().strip().split()[2]
        Comment2 = file.readline().strip().split()[2]
        Type = file.readline().strip().split()[2]
        Dimension = int(file.readline().strip().split()[2])
        EdgeWeightType = file.readline().strip().split()[2]
        file.readline()

        self.data = []  

        for i in range(int(Dimension)):
            content = file.readline().strip().split()
            self.data.append((float(content[1]), float(content[2])))

    def fitness(self, individual):
        # Total distance of path 
        fitness = 0 
        for i in range(len(individual)-1): 
            fitness += self.distance(individual[i], individual[i+1])
        fitness += self.distance(individual[0], individual[-1]) # from end to start again 
        return fitness 

    def distance(self, a, b): 
        return math.sqrt((b[0] - a[0])** 2 + (b[1] - a[1]) ** 2)

    def cross_over(self, p1, p2): 
        size = len(p1) 
        offspings = []

        while len(offspings) < self.no_offsprings: 

            o1, o2 = [None] * size, [None] * size  
        
            start_idx, end_idx = -1, -1 

            # Two slices 
            while start_idx >= end_idx: 
                start_idx, end_idx = random.randint(0, size - 1), random.randint(0, size - 1)

            # Starting 
            o1[start_idx:end_idx+1], o2[start_idx:end_idx+1] = p1[start_idx:end_idx+1], p2[start_idx:end_idx+1]
            j, k = end_idx + 1, end_idx + 1

            # Ending 
            for i in range(size - (end_idx - start_idx + 1)):       
                while p2[j % size] in o1: 
                    j += 1 
                while p1[k % size] in o2: 
                    k += 1 
                o1[(end_idx + i + 1) % size], o2[(end_idx + i + 1) % size] = p2[j % size], p1[k % size]
            
            if None in o1 or None in o2: 
                raise Exception("None found in child")

            offspings.append(o1)
            offspings.append(o2)
            
        return offspings[:self.no_offsprings]

    def mutate_offspring(self, o1): 
        # Mutate with probability 
        if random.random() < self.mutation_rate:  
            # Swap two cities 
            a, b = random.randint(0, len(o1) - 1), random.randint(0, len(o1) - 1)
            o1[a], o1[b] = o1[b], o1[a]
        return o1 

    

    def initialize_population(self): 
        # Randomly initialize population 
        pop_ = [] 
        for i in range(self.pop_size): 
            random.shuffle(self.data)
            pop_.append(self.data)
        return pop_



print("TSP Problem............")
print("1: FitnessProportionalSelection, \n2: RankBasedSelection,\n3: BinaryTournament, \n4: Truncation,\n5: Random")
p_scheme = int(input("Enter the parent selection scheme to follow: "))
c_scheme = int(input("Enter the survival selection scheme to follow: "))

no_gen = 5000
iterations = 10 
All_BSF, All_ASF = [] , []
for i in range(iterations):
    knp = TravellingSalesPerson(0.95, no_gen, 20, 30, 'qa194.tsp', p_scheme=p_scheme, c_scheme=c_scheme, maximize= False)    
    BSF, ASF = knp.EA_Cycle()
  
    All_BSF.append(BSF)
    All_ASF.append(ASF)
   

Avg_ASF = []

for i in range(len(ASF)):

    Avg_ASF.append((sum(All_ASF[j][i]  for j in range(len(All_ASF)))) / len(All_ASF))

Avg_BSF = []
for i in range(len(BSF)):
    Avg_BSF.append((sum(All_BSF[j][i]  for j in range(len(All_BSF)))) / len(All_BSF))

genz = [i+1 for i in range(no_gen)]
plt.plot(genz, Avg_ASF, label="ASF")
plt.plot(genz, Avg_BSF, label="BSF")
plt.xlabel("Generations")
plt.ylabel("Fitness")
plt.legend(loc="upper left")
plt.title('TSP')
plt.show()
