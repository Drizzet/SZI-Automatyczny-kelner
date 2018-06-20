from numpy import random
from cmath import *


def Genetic(windows, rooms):
    population = initPopulation(10)
    iteration = 0
    population.sort(key=lambda x: -fitness(x, windows, rooms))
    while (iteration <= 500):
        newPopulation = []
        for x in range(0, len(population), 2):
            parent1 = population[x]
            v = x+1
            if(random.randint(0, 10) > 5):
                v = random.randint(1, 10)
                while v==x:
                    v=random.randint(1,10)

            parent2 = population[v]
            child1, child2 = crossover(parent1, parent2)
            mutation(child1)
            mutation(child2)
            newPopulation.append(child1)
            newPopulation.append(child2)
        for t in newPopulation:
            if (t not in population):
                population.append(t)
        population.sort(key=lambda x: -fitness(x, windows, rooms))
        best = population[0]
        print(iteration,fitness(best,windows,rooms),best)
        delete = len(newPopulation)
        del population[delete:]
        iteration = iteration + 1
        if(fitness(best,windows,rooms)>1200):
            iteration = 1001

    return set(best)


def mutation(tables):
    if (random.randint(0, 100) <= 15):
        i = random.randint(1, 14)
        j = random.randint(1, 14)
        p = random.randint(1, 9)
        tables[p] = (i, j)


def crossover(tables1, tables2):
    point = random.randint(1, 8)
    c = tables1[:point]
    a = tables2[point:]
    for i in a:
            c.append(i)
    d = tables2[:point]
    b = tables1[point:]
    for i in b:
            d.append(i)
    return (c, d)


def initPopulation(n):
    population = []
    for i in range(n):
        individual = [(random.randint(1, 14),random.randint(1, 14)) for a in range(10)]
        if individual not in population:
            population.append(individual)
    return population


def fitness(tables, windows, rooms):
    fitness = 0
    for table in tables:
        o = sqrt(pow((table[0] - 8), 2) + pow((table[1] - 7), 2))
        fitness -= o
        for window in windows:
            o = sqrt(pow((table[0] - window[0]), 2) + pow((table[1] - window[1]), 2))
            fitness -= o*0.5
        for room in rooms:
            o = sqrt(pow((table[0] - room[0]), 2) + pow((table[1] - room[1]), 2))
            if round(o.real) >5:
                fitness += 5
        count = 0
        for table2 in tables:
            o = (sqrt(pow((table[0] - table2[0]), 2) + pow((table[1] - table2[1]), 2)))
            if round(o.real) < 3:
                fitness -= 10 * o
            else:
                if round(o.real) <= 10:
                    fitness += o * 4
            if(o==0):
                fitness -= 100
            if(table[0]==table2[0] or table[1]==table2[1]):
                count +=1
            if(table[0] - table2[0]==1 and table[1] - table2[1]==1):
                fitness -=25
        fitness -= count*5
    return round(fitness.real)
