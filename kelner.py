from config import *
from astar2 import *
import time
from genetic import *

def drawText(text):
    z = 40
    for t in text:
        screen.blit(t, (sizeWindow + 20, z))
        z = z + 20

def drawTextOrdersFirst(text):
    z = 40
    for t in text:
        screen.blit(t, (sizeWindow + 400, z))
        z = z + 20

def drawTextOrdersSecond(text):
    z = 40
    for t in text:
        screen.blit(t, (sizeWindow + 475, z))
        z = z + 20

waiting = True
przyKliencie = False
pokazuj = True
customerNow = (m, m)
text = []
orders = []
ordersTextFirst = []
ordersTextSecond = []

#desks = Genetic(desks, windows, rooms, size)
#print(desks)
while not done:
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            coordsX = pos[0] // m
            coordsY = pos[1] // m
            waiterCoordsX = kelnerX // m
            waiterCoordsY = kelnerY // m
            if (coordsX, coordsY) not in obstaclesSet:
                j = 0
                solution = None
                rClick = PlanRoute((waiterCoordsX, waiterCoordsY, directions[0]), (coordsX, coordsY), obstacles, size)
                if (astar_search(rClick) != None):
                    solution = astar_search(rClick).solution()
                    sol_len = solution.__len__()

    ### Wykonanie akcji
    if j>=0 and j < sol_len and (solution != None):
        x = solution[j]
        if (j == sol_len - 1):
            przyKliencie = True
            sol_len = 0
            solution = None
            j = 0
            ile = 0
        if x == 'TurnRight':
            angle = angle - 90
            surf = pygame.transform.rotate(waiterImg, angle)
            directions = directions[1:] + [directions[0]]
        if x == 'TurnLeft':
            angle = angle + 90
            surf = pygame.transform.rotate(waiterImg, angle)
            directions = [directions[3]] + directions[:3]
        if x == 'Forward':
            y = directions[0]
            if y == 'N':
                kelnerY -= m
            if y == 'S':
                kelnerY += m
            if y == 'W':
                kelnerX -= m
            if y == 'E':
                kelnerX += m
        j = j + 1
    else:
        waiting = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: kelnerY -= m
    if pressed[pygame.K_DOWN]: kelnerY += m
    if pressed[pygame.K_LEFT]: kelnerX -= m
    if pressed[pygame.K_RIGHT]: kelnerX += m

    ### Rysowanie
    screen.fill((243, 138, 55))

    for i in range(0, sizeWindow, 50): ## siatka
        vertical_line = pygame.Surface((1, sizeWindow), pygame.SRCALPHA)
        vertical_line.fill((0, 0, 0, 30))
        screen.blit(vertical_line, (i - 1, 0))
        horizontal_line = pygame.Surface((sizeWindow, 1), pygame.SRCALPHA)
        horizontal_line.fill((0, 0, 0, 30))
        screen.blit(horizontal_line, (0, i - 1))

    for desk in desks: ## stoliki
        pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(desk[0] * m, desk[1] * m, m, m))

    for window in windows: ## okna
        screen.blit(windowImg, (window[0] * m, window[1] * m))

    for customer in customers: ## klienci
        pygame.draw.circle(screen, (0, 102, 0), (int(customer[0] * m), int(customer[1] * m)), int(m / 2))

    pygame.draw.circle(screen, (255, 0, 0), (int(customerNow[0] * m), int(customerNow[1] * m)), int(m / 2))

    screen.blit(doorImg, (weWyX*m, weWyY*m)) ## wejscie/wyjscie
    screen.blit(wcImg, (wcX*m, wcY*m)) ## wc
    screen.blit(kitchenImg, (kuchniaX*m, kuchniaY*m)) ## kuchnia/zaplecze

    screen.blit(surf, (kelnerX, kelnerY)) ## kelner

    screen.blit(txt, (sizeWindow + 20, 0))  ## Tekst "Rozmowa z klientem"
    screen.blit(ordersHeader, (sizeWindow + 400, 0)) ## Tekst "Zamówienia"

    if len(cust) != 0: ## podchodzenie do klienta
        if waiting is True and pokazuj is False:
            customerNow = cust.pop()
            coordsX = int(customerNow[0] - 1.5)
            coordsY = int(customerNow[1] - 0.5)
            j = 0
            solution = None
            sol_len = 0
            waiterCoordsX = kelnerX // m
            waiterCoordsY = kelnerY // m
            rClick2 = PlanRoute((waiterCoordsX, waiterCoordsY, directions[0]), (coordsX, coordsY), obstacles, size)
            waiting = False
            if (astar_search(rClick2) != None):
                solution = astar_search(rClick2).solution()
                sol_len = solution.__len__()

    if przyKliencie:
        y = startCustomer()
        text = y[0]
        k = getDishName(y[1])
        orders.append(Order(customerNow, k))
        ordersTextFirst.append(create_text(str(customerNow), font_preferences, 16, (0, 0, 0)))
        ordersTextSecond.append(create_text(k, font_preferences, 16, (0, 0, 0)))
        przyKliencie = False
        pokazuj = True

    if len(text) != 0:
        drawText(text)

    if len(ordersTextFirst) != 0:
        drawTextOrdersFirst(ordersTextFirst)

    if len(ordersTextSecond) != 0:
        drawTextOrdersSecond(ordersTextSecond)

    pygame.display.flip()
    clock.tick(10)
    if pokazuj is True:
        time.sleep(3)
        pokazuj = False
