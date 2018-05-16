import pygame
from astar2 import *

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
        self.obstaclesAll = desksI | desksII | windows | wc | customersObstacles

obstacles = Obstacles(desksI, desksII, windows, wc, wyjscie, customersObstacles)

solution = None
sol_len = 0

pygame.init()
screen = pygame.display.set_mode((sizeWindow, sizeWindow))
done = False
is_blue = True
kelnerX = int(m * 0.5)
kelnerY = int(m * 13.5)
krataX = 0
krataY = 0
clock = pygame.time.Clock()

### jednostka: 1 - przejście o 1 kratkę; początkowa kratka to kratka (0, 0)
### indeksowanie kratek: lewo/góra: (0, 0); prawo/dół: (rozmiar - 1, rozmiar - 1)
### krata: 17x17

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            coordsX = pos[0] // m
            coordsY = pos[1] // m
            waiterCoordsX = kelnerX // m
            waiterCoordsY = kelnerY // m
            if (coordsX, coordsY) not in obstaclesSet:
                j = 0
                rClick = PlanRoute((waiterCoordsX, waiterCoordsY), (coordsX, coordsY), obstacles, size)
                if (astar_search(rClick) != None):
                    solution = astar_search(rClick).solution()
                    sol_len = solution.__len__()
                    print(solution)

    if j>=0 and j < sol_len and (solution != None):
        x = solution[j]
        if x == "UP":
            kelnerY -= m
        if x == "DOWN":
            kelnerY += m
        if x == "LEFT":
            kelnerX -= m
        if x == "RIGHT":
            kelnerX += m
    j = j + 1

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: kelnerY -= m
    if pressed[pygame.K_DOWN]: kelnerY += m
    if pressed[pygame.K_LEFT]: kelnerX -= m
    if pressed[pygame.K_RIGHT]: kelnerX += m

    screen.fill((243, 138, 55))

    for i in range(0, 85):
        pygame.draw.line(screen,(0, 0, 0),(krataX+i*m, 0),(krataX+i*m, sizeWindow), 1)
        pygame.draw.line(screen,(0, 0, 0), (0, krataY+i*m),(sizeWindow, krataY+i*m), 1)

    pygame.draw.rect(screen, (255, 0, 0) , pygame.Rect(weWyX*m, weWyY*m, m, m)) ### wejscie/wyjscie
    pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(wcX*m, wcY*m, m, m)) ### WC
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(kuchniaX*m, kuchniaY*m, m, m)) ### kuchnia/zaplecze

    for desk in desksI: ## I kolumna stolikow
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(desk[0] * m, desk[1] * m, m, m))

    for desk in desksII: ## II kolumna stolikow
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(desk[0] * m, desk[1] * m, m, m))

    for window in windows: ## okna
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(window[0] * m, window[1] * m, m, m))

    if is_blue:
        color = (0, 128, 255)
    else:
        color = (255, 100, 0)

    pygame.draw.circle(screen, color, (kelnerX, kelnerY), int(m / 2))

    for customer in customers: ## klienci
        pygame.draw.circle(screen, (0, 102, 0), (int(customer[0] * m), int(customer[1] * m)), int(m / 2))

    pygame.display.flip()
    clock.tick(15)
