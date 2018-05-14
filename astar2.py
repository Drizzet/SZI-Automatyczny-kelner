from utils import (
    is_in, memoize, PriorityQueue
)

class Node:
    """ Węzeł w drzewie wyszukiwań. Zawiera odniesienie do węzła rodzica i aktualnego stanu. """

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
    if problem.goal in problem.obstacles:
        return None
    frontier = PriorityQueue('min', f)
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

def astar_search(problem, h=None):
    """ Algorytm przeszukiwania A* - algorytm Greedy Best First Search na podstawie książki,
        gdzie f(n) = g(n) + h(n). Funkcja h(n) jest zaimplementowana w klasie problemu. """

    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))

class PlanRoute():
    """ Definicja problemu ruchu agenta po kracie. """

    def __init__(self, initial, goal, obstacles, dimrow):
        """ Zdefiniowanie stanu początkowego i stanu akceptującego oraz wielkość kraty i zbiór punktów-przeszkód. """

        self.initial = initial
        self.dimrow = dimrow
        self.goal = goal
        self.obstacles = obstacles

    def actions(self, state):
        """ Zwraca wszystkie akcje, które mogą być wykonane w danym stanie. """

        possible_actions = ['UP', 'LEFT', 'DOWN', 'RIGHT']
        x = state[0]
        y = state[1]

        # Zapobieganie niedozwolonym akcjom
        if x == 0:
            if 'LEFT' in possible_actions:
                possible_actions.remove('LEFT')
        if y == 0:
            if 'UP' in possible_actions:
                possible_actions.remove('UP')
        if x == (self.dimrow - 1):
            if 'RIGHT' in possible_actions:
                possible_actions.remove('RIGHT')
        if y == (self.dimrow - 1):
            if 'DOWN' in possible_actions:
                possible_actions.remove('DOWN')

        return possible_actions

    def result(self, state, action):
        """ Dla danego stanu i akcji zwracany jest nowy stan, który jest wynikiem danej akcji. """

        x = state[0]
        y = state[1]
        proposed_loc = tuple()

        # Ruch agenta
        if action == 'UP':
            proposed_loc = (x, y - 1)
        elif action == 'DOWN':
            proposed_loc = (x, y + 1)
        elif action == 'LEFT':
            proposed_loc = (x - 1, y)
        elif action == 'RIGHT':
            proposed_loc = (x + 1, y)
        else:
            raise Exception('InvalidAction')

        if proposed_loc not in self.obstacles:
            state = proposed_loc

        return state

    def goal_test(self, state):
        """ Dla danego stanu zwraca wartość True jeśli stan jest stanem docelowym, 
            w przeciwnym wypadku zwraca wartość False. """

        return state == tuple(self.goal)

    def path_cost(self, c, state1, action, state2):
        """ Zwraca koszt przejścia ścieżki ze stanu state1 przez jakąś akcję do stanu state2,
            zakładając koszt c do osiągnięcia tego stanu. """
        
        return c + 1

    def h(self, node):
        """ Zwraca wartość heurystyki dla danego stanu. """

        # Heurystyka Manhattan
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
