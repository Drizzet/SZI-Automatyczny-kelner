import pygame

j = -1

size = 15 ### ile kratek w rzedzie/kolumnie
m = 50 ## mnoznik 1 kratki na ekranie w px
sizeWindow = size*m ### rozmiar okna w px

waiterCoordsX = 0 ## polozenie X kelnera w jednostkach kratek
waiterCoordsY = 0 ## polozenie Y kelnera w jednostkach kratek
coordsX = 0 ## cel X w jednostkach kratek
coordsY = 0 ## cel Y w jednostkach kratek

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

### Stoliki - I kolumna
desksI = set([(6, 3), (6, 7), (6, 11)])

### Stoliki - II kolumna
desksII = set([(10, 3), (10, 7), (10, 11)])

### Okna
windows = set([(14, 2), (14, 3), (14, 4), (14, 6), (14, 7),
               (14, 8), (14, 10), (14, 11), (14, 12)])

### Klienci
customers = set([(6.5, 2.5), (6.5, 4.5), (10.5, 2.5), (10.5, 4.5),
                 (6.5, 6.5), (6.5, 8.5), (10.5, 6.5), (10.5, 8.5),
                 (6.5, 10.5), (6.5, 12.5), (10.5, 10.5), (10.5, 12.5)])
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
