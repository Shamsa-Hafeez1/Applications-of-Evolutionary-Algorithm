import random 
from final import *
import matplotlib.pyplot as plt

class Knapsack(Evolutionary_Algorithm):
    '''Implementation of Evolutionary_Algorithm in Knapsack Problem'''

    def __init__(self, mutation_rate, no_generations, no_offsprings, pop_size, path, p_scheme, c_scheme, maximize = False ):
        Evolutionary_Algorithm.__init__(self, mutation_rate, no_generations, no_offsprings, pop_size,  p_scheme, c_scheme, maximize)

        file = open(path, 'r')
        first_line = file.readline().strip().split()
        n = int(first_line[0]) # possible number of items we have 

        self.wmax = int(first_line[1]) #maximum weight possible 

        self.data = [] 

        for i in range(n): 
            x = file.readline().strip().split()
            self.data.append((int(x[0]), int(x[1]))) # (profit, weight)

    def fitness(self, individual): 
        ''' Calculates the fitness of the Knap sack based on profit and weight 

        Args: 
        - self: Ref to the class 
        - individual: The chromosome whose fitness value is being calculated 

        Returns:
        - Fitness of a chromosome 
        '''
        fitness, weight = 0, 0
        for i in individual: 
            fitness += i[0] # Sum all the profits
            weight += i[1] # Sum all the weights 

        if weight > self.wmax: # Penalize when weight exceeds threshold 
            fitness = 0        # Such a chromosome cannot be tolderated in the population 
        return fitness 


    def total_weight(self, lst):
        ''' Calculates the total weight of the knapsack 

        Args: 
        - self: Ref to the class 
        - lst: The chromosome whose weight needs to be calculated 

        Returns: 
        Total weight of the knapsack 
        ''' 
        w = 0 
        for i in range(len(lst)): 
            w+=lst[i][1]
        return w 

    def cross_over(self, p1, p2): 
        ''' Performs cross over operation between parents in KnapSack Problem 

        Args: 
        - self: Ref to the class 
        - p1: Parent 1 
        - p2: Parent 2 

        Returns: 
        The list of offspings from parent p1 and p2 as per the 
        number of offsprings required 
        '''
        size = min(len(p1), len(p2))
        off_springs = [] 

        while len(off_springs) != self.no_offsprings: 
          
            x = random.randint(0, size-1)
            o1 = p1[:x+1] # Add x elements in o1 
            i = random.randint(0, len(p2)-1)
            while self.total_weight(o1) < self.wmax: 
                if p2[i] not in o1: # and self.total_weight(o1) + p2[i][1] < self.wmax: 
                    o1.append(p2[i])
                i+=1 
                if i == len(p2): 
                    break 

            
            off_springs.append(o1)
           
            
        return off_springs

    def mutate_offspring(self, chromosome):  
        ''' Mutates the chromosome of the Knapsack problem 

        Args: 
        - self: Ref to the class 
        - chromosome: The chromosome that shall be mutated 

        Returns: 
        A chromosome that may be mutated 
        '''
        if random.random() > self.mutation_rate: # Mutate with a probability 
            chromosome.pop(random.randint(0, len(chromosome)-1)) 
            x = random.sample(self.data, 1)[0]

            while x in chromosome: # cannot put the same thing again in the Knapsack  
                x = random.sample(self.data, 1)[0]
            
            chromosome.append(x) 
        return chromosome

    def initialize_population(self): 
        ''' Initializes the population of the Knapsack prolem 

        Args: 
        - self: Ref to the class 

        Returns: 
        Randomly initialized population 
        '''
        pop_ = [] 
        for i in range(self.pop_size): 
            weight = 0
            sol = [] 
            data1 = copy.deepcopy(self.data)

            while len(data1) != 0: 
                x = random.randint(0, len(data1)-1)

                # Only the items within the weight are legally allowed to be inside knapsack 
                if weight + data1[x][1] <= self.wmax and data1[x] not in sol:
                    sol.append(data1[x])
                    weight += data1[x][1]

                data1.pop(x)

            # pop_.append(sol[:-1]) 
        return pop_


print("Knapsack Problem............")
print("1: FitnessProportionalSelection, \n2: RankBasedSelection,\n3: BinaryTournament, \n4: Truncation,\n5: Random")
p_scheme = int(input("Enter the parent selection scheme to follow: "))
c_scheme = int(input("Enter the survival selection scheme to follow: "))

no_gen = 300
iterations = 10 
All_BSF, All_ASF = [] , []
for i in range(iterations):
    knp = Knapsack(0.5, no_gen, 5, 10, 'f8_l-d_kp_23_10000', p_scheme = p_scheme, c_scheme = c_scheme, maximize= True)    
    BSF, ASF = knp.EA_Cycle()
    All_BSF.append(BSF)
    All_ASF.append(ASF)
    
# Calculate the Average ASF and BSF 
Avg_ASF = []
for i in range(len(ASF)):
    Avg_ASF.append((sum(All_ASF[j][i]  for j in range(len(All_ASF)))) / len(All_ASF))

Avg_BSF = []
for i in range(len(BSF)):
    Avg_BSF.append((sum(All_BSF[j][i]  for j in range(len(All_BSF)))) / len(All_BSF))

# Plot the graph 
genz = [i+1 for i in range(no_gen)]
plt.plot(genz, Avg_ASF, label="ASF")
plt.plot(genz, Avg_BSF, label="BSF")
plt.xlabel("Generations")
plt.ylabel("Fitness")
plt.legend(loc="upper left")
plt.title('Knapsack - Binary Tournament, Rank Based Selection')
plt.show()