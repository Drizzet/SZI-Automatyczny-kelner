import pygame

j = -1

size = 14 ### ile kratek w rzedzie/kolumnie
m = 50 ## mnoznik 1 kratki na ekranie w px
sizeWindow = size*m ### rozmiar okna w px

waiterCoordsX = 0 ## polozenie X kelnera w jednostkach kratek
waiterCoordsY = 0 ## polozenie Y kelnera w jednostkach kratek
coordsX = 0 ## cel X w jednostkach kratek
coordsY = 0 ## cel Y w jednostkach kratek

### Pomieszczenia
weWyX = 0
weWyY = 2
wyjscie = set([(weWyX, weWyY)])
wcX = 0
wcY = 6
wc = set([(wcX, wcY)])
kuchniaX = 0
kuchniaY = 10
rooms = set([(weWyX, weWyY), (wcX, wcY), (kuchniaX, kuchniaY)])

### Stoliki - I kolumna
desksI = set([(6, 2), (6, 6), (6, 10)])

### Stoliki - II kolumna
desksII = set([(10, 2), (10, 6), (10, 10)])

### Okna
windows = set([(13, 1), (13, 2), (13, 3), (13, 5), (13, 6),
               (13, 7), (13, 9), (13, 10), (13, 11)])

### Klienci
customers = set([(6.5, 1.5), (6.5, 3.5), (10.5, 1.5), (10.5, 3.5),
                 (6.5, 5.5), (6.5, 7.5), (10.5, 5.5), (10.5, 7.5),
                 (6.5, 9.5), (6.5, 11.5), (10.5, 9.5), (10.5, 11.5)])
customersObstacles = set([])
for customer in customers:
    customersObstacles.add((int(customer[0]), int(customer[1])))

obstaclesSet = desksI | desksII | windows | customersObstacles | wc | wyjscie

class Obstacles:
    def __init__(self, desksI, desksII, windows, wc, wyjscie, customersObstacles):
        self.desksI = desksI
        self.desksII = desksII
        self.windows = windows
        self.customers = customersObstacles
        self.wc = wc
        self.wyjscie = wyjscie
        self.obstaclesAll = desksI | desksII | windows | wc | wyjscie | customersObstacles

obstacles = Obstacles(desksI, desksII, windows, wc, wyjscie, customersObstacles)

solution = None
sol_len = 0

screen = pygame.display.set_mode((sizeWindow, sizeWindow))
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
