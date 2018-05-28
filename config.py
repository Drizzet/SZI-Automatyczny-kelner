from text import *
from order import *
from genetic import *

pygame.init()

def startCustomer(ind):
    text = []
    talks = startConversation()
    test_data = prepareTestData(talks)
    talkCustomer = talk(talks, test_data, ind)
    talkText = talkCustomer[0]
    order = talkCustomer[1]
    for x in talkText:
        text.append(create_text(x, font_preferences, 16, (0, 0, 0)))
    return [text, order]

class Obstacles:
    def __init__(self, desksI, desksII, windows, wc, wyjscie, customersObstacles):
        self.desksI = desksI
        self.desksII = desksII
        self.windows = windows
        self.customers = customersObstacles
        self.wc = wc
        self.wyjscie = wyjscie
        self.obstaclesAll = desksI | desksII | windows | wc | wyjscie | customersObstacles

font_preferences = ["Arial"]
txt = (create_text("Rozmowa kelnera z klientem:", font_preferences, 20, (0, 0, 0)))
ordersHeader = (create_text("Historia zamówień: ", font_preferences, 20, (0, 0, 0)))

j = -1

size = 15  ### ile kratek w rzedzie/kolumnie
m = 50  ## mnoznik 1 kratki na ekranie w px
sizeWindow = size * m  ### rozmiar okna w px

waiterCoordsX = 0  ## polozenie X kelnera w jednostkach kratek
waiterCoordsY = 0  ## polozenie Y kelnera w jednostkach kratek
coordsX = 0  ## cel X w jednostkach kratek
coordsY = 0  ## cel Y w jednostkach kratek

### Pomieszczenia
weWyX = 0
weWyY = 3
wyjscie = set([(weWyX, weWyY)])
wcX = 0
wcY = 7
wc = set([(wcX, wcY)])
kuchniaX = 0
kuchniaY = 11
rooms = set([(weWyX, weWyY), (wcX, wcY), (kuchniaX, kuchniaY)])

### Stoliki
desks = set([(0, 1), (0, 2), (0, 3),(0, 4), (0, 5), (0, 6)])

### Okna
windows = set([(14, 2), (14, 3), (14, 4), (14, 6), (14, 7),
               (14, 8), (14, 10), (14, 11), (14, 12)])

### Klienci
desks = Genetic(desks, windows, rooms, size)
customers = set([])
for desk in desks:
    for desk2 in desks:
        if(desk2 != desk[0] and desk2 != desk[1] + 1 ):
            customers.add((desk[0] + 0.5, desk[1] + 1.5))
        if (desk2 != desk[0] and desk2 != desk[1] - 1):
            customers.add((desk[0] + 0.5, desk[1] - 0.5))

customersObstacles = set([])
cust = []
vis = []
c = customersList(customers)
n = len(c)
cInd = 0
while len(cust) < len(c):
    r = -1
    if c[cInd] not in vis:
        cust.append(c[cInd])
        vis.append(c[cInd])
    while r < n - 1:
        r = r + 1
        if r == cInd:
            continue
        if c[cInd][0] == c[r][0]:
            if (c[cInd][1] - c[r][1]) == 2 or (c[cInd][1] - c[r][1]) == -2:
                if c[r] not in vis or c[cInd] not in vis:
                    cust.append(c[r])
                    vis.append(c[r])
                    break
    cInd = cInd + 1

print(cust)

for customer in customers:
    customersObstacles.add((int(customer[0]), int(customer[1])))

obstaclesSet = desks | windows | customersObstacles | wc | wyjscie

class Obstacles:
    def __init__(self, desks, windows, wc, wyjscie, customersObstacles):
        self.desks = desks
        self.windows = windows
        self.customers = customersObstacles
        self.wc = wc
        self.wyjscie = wyjscie
        self.obstaclesAll = desks | windows | wc | wyjscie | customersObstacles

obstacles = Obstacles(desks, windows, wc, wyjscie, customersObstacles)

solution = None
sol_len = 0

screen = pygame.display.set_mode((sizeWindow + 15*m, sizeWindow))
done = False

kelnerX = int(m * 0)
kelnerY = int(m * 13)
directions = ['E', 'S', 'W', 'N']

krataX = 0
krataY = 0
clock = pygame.time.Clock()

waiterImg = pygame.image.load('images/kelner.png')
angle = -90
surf = pygame.transform.rotate(waiterImg, angle)

doorImg = pygame.image.load("images/doors.jpg")
wcImg = pygame.image.load("images/wc.png")
kitchenImg = pygame.image.load("images/kitchen.jpg")
windowImg = pygame.image.load("images/window.png")

### jednostka: 1 - przejście o 1 kratkę; początkowa kratka to kratka (0, 0)
### indeksowanie kratek: lewo/góra: (0, 0); prawo/dół: (rozmiar - 1, rozmiar - 1)
### krata: 14x14
