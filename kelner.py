import pygame
import time
from astar2 import *

pygame.init()
screen = pygame.display.set_mode((850, 850))
done = False
is_blue = True
kelnerX = 25
kelnerY = 25
krataX = 0
krataY = 0
clock = pygame.time.Clock()

### jednostka: 1 - przejście o 1 kratkę; początkowa kratka to kratka (0, 0)
### indeksowanie kratek: lewo/góra: (0, 0); prawo/dół: (rozmiar - 1, rozmiar - 1)
### krata: 17x17

j = -1
size = 17
wspKelnerX = 0
wspKelnerY = 0
wspX = 0
wspY = 0
obstacles = set([(7, 1), (8, 1), (12, 1), (13, 1), (7, 2), (8, 2),
                (12, 2), (13, 2), (7, 3), (8, 3), (12, 3), (13,3),
                (7, 7), (8, 7), (12, 7), (13, 7), (7, 8), (8, 8),
                (12, 8), (13, 8), (7, 9), (8, 9), (12, 9), (13, 9),
                (7, 13), (8, 13), (12, 13), (13, 13), (7, 14), (8, 14),
                (12, 14), (13, 14), (7, 15), (8, 15), (12, 15),(13, 15)
            ])

solution = None
sol_len = 0
## r = PlanRoute((wspKelnerX, wspKelnerY), (wspX, wspY), obstacles, size)
"""if (astar_search(r) != None):
    solution = astar_search(r).solution()
    sol_len = solution.__len__()
    print(solution)"""

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            wspX = pos[0] // 50
            wspY = pos[1] // 50
            wspKelnerX = kelnerX // 50
            wspKelnerY = kelnerY // 50
            if (wspX, wspY) not in obstacles:
                j = 0
                rClick = PlanRoute((wspKelnerX, wspKelnerY), (wspX, wspY), obstacles, size)
                if (astar_search(rClick) != None):
                    solution = astar_search(rClick).solution()
                    sol_len = solution.__len__()
                    print(solution)


    if j>=0 and j < sol_len and (solution != None):
        x = solution[j]
        if x == "UP":
            kelnerY -= 50
        if x == "DOWN":
            kelnerY += 50
        if x == "LEFT":
            kelnerX -= 50
        if x == "RIGHT":
            kelnerX += 50
    j = j + 1

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: kelnerY -= 50
    if pressed[pygame.K_DOWN]: kelnerY += 50
    if pressed[pygame.K_LEFT]: kelnerX -= 50
    if pressed[pygame.K_RIGHT]: kelnerX += 50

    screen.fill((255, 255, 255))

    for i in range(0,85):
        pygame.draw.line(screen,(0,0,0),(krataX+i*50,0),(krataX+i*50,850),1)
        pygame.draw.line(screen,(0,0,0), (0,krataY+i*50),(850, krataY+i*50), 1)

    pygame.draw.rect(screen, (255, 0, 0) , pygame.Rect(0, 50, 100, 200))
    pygame.draw.rect(screen, (200, 200, 0), pygame.Rect(0, 600, 100, 200))

    pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(350, 75, 100, 100))
    pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(350, 370, 100, 100))
    pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(350, 675, 100, 100))

    pygame.draw.rect(screen, (139,69,19), pygame.Rect(600, 75, 100, 100))
    pygame.draw.rect(screen, (139,69,19), pygame.Rect(600, 370, 100, 100))
    pygame.draw.rect(screen, (139,69,19), pygame.Rect(600, 675, 100, 100))

    if is_blue:
        color = (0, 128, 255)
    else:
        color = (255, 100, 0)

    pygame.draw.circle(screen, color, (kelnerX, kelnerY),25)

    pygame.draw.circle(screen, (0,102,0), (400, 50), 25)
    pygame.draw.circle(screen, (0, 102, 0), (400, 200), 25)

    pygame.draw.circle(screen, (0, 102, 0), (650, 50), 25)
    pygame.draw.circle(screen, (0, 102, 0), (650, 200), 25)

    pygame.draw.circle(screen, (0, 102, 0), (400, 345), 25)
    pygame.draw.circle(screen, (0, 102, 0), (400, 495), 25)

    pygame.draw.circle(screen, (0, 102, 0), (650, 345), 25)
    pygame.draw.circle(screen, (0, 102, 0), (650, 495), 25)

    pygame.draw.circle(screen, (0, 102, 0), (400, 650), 25)
    pygame.draw.circle(screen, (0, 102, 0), (400, 800), 25)

    pygame.draw.circle(screen, (0, 102, 0), (650, 650), 25)
    pygame.draw.circle(screen, (0, 102, 0), (650, 800), 25)

    pygame.display.flip()
    clock.tick(15)
