import random 
from final import *
import matplotlib.pyplot as plt

class GraphColoring(Evolutionary_Algorithm):
    '''Implementation of Evolutionary Algorithm in the Graph Coloring Problem '''

    def __init__(self, mutation_rate, no_generations, no_offsprings, pop_size, path, p_scheme, c_scheme, maximize = False ):
        Evolutionary_Algorithm.__init__(self, mutation_rate, no_generations, no_offsprings, pop_size,  p_scheme, c_scheme, maximize)

        file = open(path, 'r')  # Read 
        first_line = file.readline().strip().split()
        total_nodes = int(first_line[-2])
        total_entries = int(first_line[-1])

        # Read the file 
        lst = []  
        for i in range(total_entries):
            x = file.readline().strip().split()
            lst.append((int(x[1])-1, int(x[2])-1))

        # Store the map {node : [neighbors of the node ] }
        self.graph_map = {i: [] for i in range(total_nodes)} 

        for i in range(total_entries):
            self.graph_map[lst[i][0]].append(lst[i][1]) 
    
    def fitness(self, individual): 
        ''' Calculates the fitness of an individual in the graph coloring problem 

        Args: 
        - self: Reference to the class 
        - individual: The chromosome whose fitness needs to be calculated 

        Returns: 
        fitness of an individual chromosome in the graph coloring problem 
        '''
        total_distinctive_colors = len(set(individual.values()))

        clashes = 0 
        for i in self.graph_map: 
            for j in self.graph_map[i]: 
                if individual[j] == individual[i]: 
                    clashes += 1 

        # Assuming 50 as our penalty for each 
        return (clashes * 50) + total_distinctive_colors 

    def cross_over(self, p1, p2): 
        ''' Performs cross over operation between given two parents 

        Args: 
        - self: Reference to the class 
        - p1: Parent 1 
        - p2: Parent 2 

        Returns: 
        The list of offsprings produced from cross over of p1 and p2 
        '''
        size = len(p1) 
        offspings = []

        while len(offspings) < self.no_offsprings:
            o1, o2 = dict(), dict()

            # Take any random index in the chromosome  
            start_idx = random.randint(0, size-1)
            
            # For all the nodes before start_indx, colors of 
            # p1 transmits to o1 and p2 transmits to o2 
            i = 0 
            while i != start_idx:
                o1[i] = p1[i] 
                o2[i] = p2[i] 
                i+=1 

            # For all the nodes after start_indx, colors of 
            # p2 transmits to o1 and p1 transmits to o2 
            while i != size:
                o1[i] = p2[i] 
                o2[i] = p1[i]
                i+=1 

            offspings.append(o1)
            offspings.append(o2)

        return offspings[:self.no_offsprings]

    def mutate_offspring(self, o1): 
        ''' Mutates the individual as per the probability of mutation 

        Args: 
        - self: Reference to the self 
        - o1: The individual to be mutated 

        Returns: 
        - A possibly mutated individual 
        '''
        if random.random() > self.mutation_rate: 
            x = random.randint(0, len(o1)-1) # Node to change color 
            color_to_change = random.randint(0, len(o1)-1) # Color to be substituted 
            o1[x] = color_to_change
        return o1
    
    def initialize_population(self): 
        ''' Initializes the population of the Graph coloring problem 

        Args: 
        - self: Reference to the class 

        Returns: A list / population of the individuals randomly generated in the population 
        '''
        solutions = [] 
        for i in range(self.pop_size): 

            solution = {} # {node_1: color_1, node_2 : color_2, ... }
            x = [i for i in range(len(self.graph_map))] # The possible range of colors = range of nodes in map 

            for i in range(len(self.graph_map)):  
                color = random.choice(x) # Take a random color 
                solution[i] = color      # Give the node this color 
                x.remove(color)          # This color shall not be reassigned 

            solutions.append(solution) 

        return solutions


no_gen = 700
iterations = 10 
All_BSF, All_ASF = [] , []
for i in range(iterations):
    tsp = GraphColoring(0.3, no_gen, 15, 30, 'gcol1.txt', p_scheme=1, c_scheme=2, maximize= False)
    BSF, ASF = tsp.EA_Cycle()
 
    All_BSF.append(BSF)
    All_ASF.append(ASF)


# --------------------------- 
# CALCULATING AVG ASF AND BSF 
# ---------------------------

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
plt.title('Graph Coloring - FPS, RBS')
plt.show()