from numpy import random



def Genetic(tables, windows, rooms, size):
    iteration = 0
    tables = list(tables)
    while(iteration <=250):
        print(iteration)
        #newtables = list([])
        optiontables = [ tables[i] for i in range(len(tables))]

        for i in range(len(optiontables)):
            flag = False
            optiontables[i] = (random.randint(1,size-2),random.randint(0,size-1))
            #optiontables[i] = (tables[i][0]+random.randint(-1,1),tables[i][1]+random.randint(-1,1))
            print(Fitness(optiontables,windows,rooms), Fitness(tables,windows,rooms))
            if(Fitness(optiontables,windows,rooms) > Fitness(tables,windows,rooms)):
                for j in range(len(optiontables)):
                    if(optiontables[i]==tables[j] or optiontables[i][1]==0 or optiontables[i][1]==14 or optiontables[i][0]==0 or optiontables[i][0]==14):
                        flag = True
                if(flag != True):
                    tables[i] = optiontables[i]
                    print("zmieniam",tables[i],flag,tables,optiontables)
            else:
                optiontables[i] = tables[i]
                print("zostawiam",tables,optiontables)
        # for oldtable in tables:
        #     #table = (oldtable[0]+random.randint(-1,1),oldtable[1]+random.randint(-1,1))
        #     table = (random.randint(1,size-2),random.randint(0,size-1))
        #     newtables.add(table)
        # while(len(newtables)!=len(tables)):
        #     table = (random.randint(1, size - 2), random.randint(0, size - 1))
        #     newtables.add(table)
        #
        # fitness = Fitness(tables,windows,rooms)
        # newfitness = Fitness(newtables,windows,rooms)
        # print(tables, fitness,newtables, newfitness)
        # if(newfitness>fitness):
        #    tables = newtables
        iteration += 1
    return set(tables)

def Fitness(tables, windows, rooms):
    fitness = 0
    for table in tables:
        for window in windows:
            if(table == window or table == (window[0],window[1]-1) or table == (window[0],window[1]+1)):
                fitness -= 100
            for i in range(-1,1):
                for j in range(-1,1):
                    if(table == (window[0]+i,window[1]+j)):
                        fitness += 20

        for room in rooms:
            if(table == room or table == (room[0],room[1]-1) or table == (room[0],room[1]+1)):
                fitness -= 100
            for i in range(-2,2):
                for j in range(-2,2):
                    if(table == (room[0]+i,room[1]+j)):
                        fitness -= 15


        for table2 in tables:
            if (table != table2):
                for i in range(-2,2):
                    for j in range(-2,2):
                        if (i == 0):
                            if (table == (table2[0] + i, table2[1] + j)):
                                fitness -= 50
                        else:
                            if (j == 0):
                                if (table == (table2[0] + i, table2[1] + j)):
                                    fitness -= 1
                            else:
                                fitness -= 10
            else:
                fitness -= 70

    return fitness