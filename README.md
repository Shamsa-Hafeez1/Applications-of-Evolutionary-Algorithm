# Applications of Evolutionary Algorithm
Implementation of Evolutionary Algorithm in Travelling Salesperson problem, Knapsack problem and Graph Coloring problem along with analysis on selection schemes. 

## 1. Travelling Salesman Problem (TSP)

The dataset used is obtained from http://www.math.uwaterloo.ca/tsp/world/countries.html and it contains 194 cities. 

### Chromosome Representation: 
Each chromosome is in the form of the list. The length of the list is equal to the number of places to visit. Thus, the length is 194. The list consists of tuples whose first and second index represents the x and y coordinates of the city to visit respectively. The index of the city decides the order in which it is visited. For example:
[(x1, y1), (x2, y2), (x3, y3), ..., (x194, y194)]

### Fitness Function: 
The fitness function calculates and returns the total distance to be travelled when a salesperson passes through a given path 

![AddReadme](https://user-images.githubusercontent.com/110885397/235683887-56f91ef9-536d-4570-a912-e6cce7e1e4b2.PNG)

## 2. Knapsack Problem: The knapsack problem is a problem in combinatorial optimization: Given a set of items, each with a weight and a value, determine the number of each item to include in a collection so that the total weight is less than or equal to a given limit and the total value is as large as possible

The dataset used is obtained from http://artemisa.unicauca.edu.co/~johnyortega/instances_01_KP/ 
Report uses ‘f8_l-d_kp_23_10000’ data instance which contains 23 items and a knapsack of capacity 10000

### Chromosome Representation: 
Each chromosome is a list that consists of tuples.The list represents the bag. Each tuple represents an item. The first element of the tuple represents the profit of the item and the second element of the tuple represents the weight of the item. Note that unlike the chromosome of TSP, the order of the tuples in the list does not matter. For example:
[(p1, w1), (p2, w2), (p3, w3)]
This list shows that there are 3 items in the bag: One item has a profit of p1 and a weight of w1. Another item has a profit of p2 and a weight of w2. Another item has a profit of p3 and a weight of w3. Through this way the chromosome exactly represents the configuration of an individual in the population.

### Fitness Function: 
The fitness function returns the total profit of the items in the bag. Note that if the weight of the items in the bag exceeds that maximum weight allowed then the fitness function penalizes it by considering its fitness to be zero.

![image](https://user-images.githubusercontent.com/110885397/235684833-8e5c3594-2edb-4cfa-afd4-b840b4bf670b.png)

## 2. Knapsack Problem: Graph Coloring is a classic problem in Computer Science in which you are required to color the vertices of a graph (vertex coloring) with minimum colors such that no two adjacent vertices are of same color

Dataset was obtained from http://people.brunel.ac.uk/~mastjjb/jeb/orlib/files/  (File name: gcol1.txt) 

### Chromosome Representation:  
Notice that the graph coloring problem needs to store the graph (nodes and edges) as well as the color of each node. Since the graph (nodes and edges) remains the same throughout the process of Evolutionary Algorithm, what we really need to identify an individual chromosome is the color assigned to its nodes. The graph is stored in graph map dictionary where the key is the node and the value is the list of its corresponding neighbourhood nodes. Now, our actual chromosome is a dictionary with key as the node number and the value as the color assigned to it. Note that colors are represented in the form of whole numbers (We can assume it to be arbitrarily any hexadecimal value of color). For example: { 1: 2, 2: 2, 3: 1 }

### Fitness Function: 
This is a minimization problem and we need to minimize the number of colors used to color the graph. Thus our fitness value would be total distinctive colors used to color the nodes of our map. Since, we have a constraint that no adjacent nodes should be of same color, therefore we cannot tolerate such chromosomes in our population whose adjacent nodes are of same color. Therefore we assign them a high fitness value by adding 50 times the number of colors clashing. Thus, if the least fit chromosomes are discarded first then individuals with clashing colors shall be discarded first

![image](https://user-images.githubusercontent.com/110885397/235687200-6e79252e-7704-44af-81ce-03a2547bc5dd.png)

