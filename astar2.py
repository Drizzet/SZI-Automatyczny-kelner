import heapq

class PriorityQueue:
    """ Kolejka priorytetowa, w której minimalny element (wynik
        determinuje funkcja f i kolejność) zwracany jest jako pierwszy. """
    def __init__(self, f=lambda x: x):
        self.heap = []
        self.f = f

    def append(self, item):
        """ Wstawianie elementu na odpowiedniej pozycji. """
        heapq.heappush(self.heap, (self.f(item), item))

    def pop(self):
        """ Zwrócenie elementu z najmniejszą wartością funkcji f (uwzględniając kolejność). """
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """ Zwrócenie aktualnej długości kolejki. """
        return len(self.heap)

    def __contains__(self, item):
        """ Zwraca wartość True jeśli element jest w kolejce. """
        return (self.f(item), item) in self.heap

    def __getitem__(self, key):
        """ Pobranie konkretnego elementu. """
        for _, item in self.heap:
            if item == key:
                return item

    def __delitem__(self, key):
        """ Usunięcie pierwszego wystąpienia klucza. """
        self.heap.remove((self.f(key), key))
        heapq.heapify(self.heap)

class Node:
    """ Węzeł w grafie wyszukiwań. Zawiera odniesienie do węzła rodzica i aktualnego stanu. """
    def __init__(self, state, parent=None, action=None, path_cost=0):
        """ Tworzenie węzła na podstawie rodzica i akcji. """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem):
        """ Zwraca listę węzłów dostępnych w jednym kroku od węzła. """
        return [self.child_node(problem, action)
                for action in problem.actions(self.state)]

    def child_node(self, problem, action):
        """ Zwraca węzeł potomny. """
        next_node = problem.result(self.state, action)
        return Node(next_node, self, action,
                    problem.path_cost(self.path_cost, self.state,
                                      action, next_node))

    def solution(self):
        """ Zwraca sekwencję akcji jak dojść z korzenia do danego węzła. """
        return [node.action for node in self.path()[1:]]

    def path(self):
        """ Zwraca listę węzłów tworzących ścieżkę z korzenia do danego węzła. """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

def best_first_graph_search(problem, f):
    """ Algorytm znajduje węzły w kolejności od najmniejszej wartości funkcji f. """
    node = Node(problem.initial)
    if problem.goal_test(node.state):
        return node
    if problem.goal in problem.obstacles.obstaclesAll:
        return None
    frontier = PriorityQueue(f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                incumbent = frontier[child]
                if f(child) < f(incumbent):
                    del frontier[incumbent]
                    frontier.append(child)
    return None

def astar_search(problem):
    """ Algorytm przeszukiwania A* - algorytm Greedy Best First Search na podstawie książki,
        gdzie f(n) = g(n) + h(n). Funkcja h(n) jest zaimplementowana w klasie problemu. """
    h = problem.h
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

class PlanRoute():
    """ Definicja problemu ruchu agenta po kracie. """
    def __init__(self, initial, goal, obstacles, dimrow):
        """ Zdefiniowanie stanu początkowego i stanu akceptującego oraz wielkość kraty i zbiór punktów-przeszkód. """
        self.initial = initial
        self.goal = goal
        self.obstacles = obstacles
        self.dimrow = dimrow

    def actions(self, state):
        """ Zwraca wszystkie akcje, które mogą być wykonane w danym stanie. """
        possible_actions = ['Forward', 'TurnLeft', 'TurnRight']
        x = state[0]
        y = state[1]
        dir = state[2]

        # Zapobieganie niedozwolonym akcjom
        if x == 0 and dir == 'W':
            if 'Forward' in possible_actions:
                possible_actions.remove('Forward')
        if y == 0 and dir == 'N':
            if 'Forward' in possible_actions:
                possible_actions.remove('Forward')
        if x == (self.dimrow - 1) and dir == 'E':
            if 'Forward' in possible_actions:
                possible_actions.remove('Forward')
        if y == (self.dimrow - 1) and dir == 'S':
            if 'Forward' in possible_actions:
                possible_actions.remove('Forward')

        return possible_actions

    def result(self, state, action):
        """ Dla danego stanu i akcji zwracany jest nowy stan, który jest wynikiem danej akcji. """
        x = state[0]
        y = state[1]
        dir = state[2]
        proposed_loc = [x, y]

        # Ruchy agenta
        if action == 'Forward':
            if dir == 'N':
                proposed_loc = [x, y - 1]
            elif dir == 'S':
                proposed_loc = [x, y + 1]
            elif dir == 'W':
                proposed_loc = [x - 1, y]
            elif dir == 'E':
                proposed_loc = [x + 1, y]
            else:
                raise Exception('InvalidOrientation')

        elif action == 'TurnLeft':
            if dir == 'N':
                dir = 'W'
            elif dir == 'S':
                dir = 'E'
            elif dir == 'E':
                dir = 'N'
            elif dir == 'W':
                dir = 'S'
            else:
                raise Exception('InvalidOrientation')

        elif action == 'TurnRight':
            if dir == 'N':
                dir = 'E'
            elif dir == 'S':
                dir = 'W'
            elif dir == 'E':
                dir = 'S'
            elif dir == 'W':
                dir = 'N'
            else:
                raise Exception('InvalidOrientation')

        if (proposed_loc[0], proposed_loc[1]) not in self.obstacles.obstaclesAll:
            state = (proposed_loc[0], proposed_loc[1], dir)

        return state

    def goal_test(self, state):
        """ Dla danego stanu zwraca wartość True jeśli stan jest stanem docelowym, 
            w przeciwnym wypadku zwraca wartość False. """
        return (state[0] == self.goal[0]) and (state[1] == self.goal[1])

    def path_cost(self, c, state1, action, state2): ## przyklad - do zmiany sa warunki!
        """ Zwraca koszt przejścia ścieżki ze stanu state1 przez jakąś akcję do stanu state2,
            zakładając koszt c do osiągnięcia stanu state1. """


        ## Analizowanie ruchu
        if(action == 'TurnLeft' or action == 'TurnRight'):
            c = c + 4;
       ## if (action == 'Forward'):
        ##    c = c + 1;

        ### Analizowanie state1
        ## stoliki w I kolumnie:
        if (state1[0] - 1, state1[1] - 1) in self.obstacles.desksI:
            c = c - 1
        if (state1[0] - 1, state1[1]) in self.obstacles.desksI:
            c = c - 1
        if (state1[0] - 1, state1[1] + 1) in self.obstacles.desksI:
            c = c - 1
        if (state1[0] + 1, state1[1] - 1) in self.obstacles.desksI:
            c = c - 1
        if (state1[0] + 1, state1[1]) in self.obstacles.desksI:
            c = c - 1
        if (state1[0] + 1, state1[1] + 1) in self.obstacles.desksI:
            c = c - 1

        ## stoliki w II kolumnie:
        if (state1[0] - 1, state1[1] - 1) in self.obstacles.desksII:
            c = c - 1
        if (state1[0] - 1, state1[1]) in self.obstacles.desksII:
            c = c - 1
        if (state1[0] - 1, state1[1] + 1) in self.obstacles.desksII:
            c = c - 1
        if (state1[0] + 1, state1[1] - 1) in self.obstacles.desksII:
            c = c - 1
        if (state1[0] + 1, state1[1]) in self.obstacles.desksII:
            c = c - 1
        if (state1[0] + 1, state1[1] + 1) in self.obstacles.desksII:
            c = c - 1

        ## okna
        if (state1[0] - 1, state1[1]) in self.obstacles.windows:
            c = c - 1

        ## wc
        if (state1[0] + 1, state1[1]) in self.obstacles.wc:
            c = c - 1

        ## wyjscie
        if (state1[0] + 1, state1[1]) in self.obstacles.wyjscie:
            c = c - 1
        if (state1[0] - 1, state1[1]) in self.obstacles.wyjscie:
            c = c - 1
        if (state1[0], state1[1] + 1) in self.obstacles.wyjscie:
            c = c - 1
        if (state1[0], state1[1] - 1) in self.obstacles.wyjscie:
            c = c - 1

        ### Analizowanie state2
        ## stoliki w I kolumnie:
        if (state2[0] - 1, state2[1] - 1) in self.obstacles.desksI:
            c = c + 20
        if (state2[0] - 1, state2[1]) in self.obstacles.desksI:
            c = c + 20
        if (state2[0] - 1, state2[1] + 1) in self.obstacles.desksI:
            c = c + 20
        if (state2[0] + 1, state2[1] - 1) in self.obstacles.desksI:
            c = c + 20
        if (state2[0] + 1, state2[1]) in self.obstacles.desksI:
            c = c + 20
        if (state2[0] + 1, state2[1] + 1) in self.obstacles.desksI:
            c = c + 20

        ## stoliki w II kolumnie:
        if (state2[0] - 1, state2[1] - 1) in self.obstacles.desksII:
            c = c + 20
        if (state2[0] - 1, state2[1]) in self.obstacles.desksII:
            c = c + 20
        if (state2[0] - 1, state2[1] + 1) in self.obstacles.desksII:
            c = c + 20
        if (state2[0] + 1, state2[1] - 1) in self.obstacles.desksII:
            c = c + 20
        if (state2[0] + 1, state2[1]) in self.obstacles.desksII:
            c = c + 20
        if (state2[0] + 1, state2[1] + 1) in self.obstacles.desksII:
            c = c + 20

        ## okna
        if (state2[0] - 1, state2[1]) in self.obstacles.windows:
            c = c + 8
        if (state2[0]) == (self.dimrow - 1):
            c = c + 8

        ## wc
        if (state2[0] + 1, state2[1]) in self.obstacles.wc:
            c = c + 150

        ## wyjscie
        if (state2[0] + 1, state2[1]) in self.obstacles.wyjscie:
            c = c + 2
        if (state2[0] - 1, state2[1]) in self.obstacles.wyjscie:
            c = c + 2
        if (state2[0], state2[1] + 1) in self.obstacles.wyjscie:
            c = c + 2
        if (state2[0], state2[1] - 1) in self.obstacles.wyjscie:
            c = c + 2

        return c

    def h(self, node):
        """ Zwraca wartość heurystyki Manhattan dla danego stanu. """
        x1 = node.state[0]
        y1 = node.state[1]
        x2 = self.goal[0]
        y2 = self.goal[1]
        return abs(x2 - x1) + abs(y2 - y1)

### jednostka: 1 - przejście o 1 kratkę; początkowa kratka to kratka (0, 0)
### indeksowanie kratek: góra/lewo: (0, 0); dół/prawo: (rozmiar - 1, rozmiar - 1)
### krata: 17x17
### obstacles = set([(0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 3), (1, 4)])
### r = PlanRoute((0, 0), (0, 5), obstacles, 17)
### solution = None
### if (astar_search(r) != None):
    ###     solution = astar_search(r).solution()
### print(solution)
