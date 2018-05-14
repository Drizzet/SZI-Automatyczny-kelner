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
### indeksowanie kratek: góra/lewo: (0, 0); dół/prawo: (rozmiar - 1, rozmiar - 1)
### krata: 17x17
obstacles = set([(0, 1), (0, 2), (0, 3), (0, 4), (1, 1), (1, 2), (1, 3), (1, 4)])
r = PlanRoute((0, 0), (0, 5), obstacles, 17)
solution = None
sol_len = 0
if (astar_search(r) != None):
    solution = astar_search(r).solution()
    sol_len = solution.__len__()
    print(solution)
j = -1

while not done:
    j = j + 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

    if j < sol_len and (solution != None):
        x = solution[j]
        if x == "UP":
            kelnerY -= 50
        if x == "DOWN":
            kelnerY += 50
        if x == "LEFT":
            kelnerX -= 50
        if x == "RIGHT":
            kelnerX += 50

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

    if j < sol_len and (solution != None):
        time.sleep(0.5)
        continue

    print(kelnerX,kelnerY)
