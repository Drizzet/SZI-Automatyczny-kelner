import pygame

pygame.init()
screen = pygame.display.set_mode((850, 850))
done = False
is_blue = True
kelnerX = 30
kelnerY = 30
krataX = 0
krataY = 0
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_blue = not is_blue

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: kelnerY -= 3
    if pressed[pygame.K_DOWN]: kelnerY += 3
    if pressed[pygame.K_LEFT]: kelnerX -= 3
    if pressed[pygame.K_RIGHT]: kelnerX += 3

    screen.fill((255, 255, 255))

    for i in range(0,85):
        pygame.draw.line(screen,(0,0,0),(krataX+i*10,0),(krataX+i*10,850),1)
        pygame.draw.line(screen,(0,0,0), (0,krataY+i*10),(850, krataY+i*10), 1)



    pygame.draw.rect(screen, (255, 0, 0) , pygame.Rect(0, 50, 100, 200))
    pygame.draw.rect(screen, (200, 200, 0), pygame.Rect(0, 600, 100, 200))

    pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(350, 100, 100, 100))
    pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(350, 370, 100, 100))
    pygame.draw.rect(screen, (139, 69, 19), pygame.Rect(350, 650, 100, 100))

    pygame.draw.rect(screen, (139,69,19), pygame.Rect(600, 100, 100, 100))
    pygame.draw.rect(screen, (139,69,19), pygame.Rect(600, 370, 100, 100))
    pygame.draw.rect(screen, (139,69,19), pygame.Rect(600, 650, 100, 100))

    if is_blue:
        color = (0, 128, 255)
    else:
        color = (255, 100, 0)
    pygame.draw.circle(screen, color, (kelnerX, kelnerY),25)

    pygame.draw.circle(screen, (0,102,0), (400, 75), 25)
    pygame.draw.circle(screen, (0, 102, 0), (400, 225), 25)

    pygame.draw.circle(screen, (0, 102, 0), (650, 75), 25)
    pygame.draw.circle(screen, (0, 102, 0), (650, 225), 25)

    pygame.draw.circle(screen, (0, 102, 0), (400, 345), 25)
    pygame.draw.circle(screen, (0, 102, 0), (400, 495), 25)

    pygame.draw.circle(screen, (0, 102, 0), (650, 345), 25)
    pygame.draw.circle(screen, (0, 102, 0), (650, 495), 25)

    pygame.draw.circle(screen, (0, 102, 0), (400, 625), 25)
    pygame.draw.circle(screen, (0, 102, 0), (400, 775), 25)

    pygame.draw.circle(screen, (0, 102, 0), (650, 625), 25)
    pygame.draw.circle(screen, (0, 102, 0), (650, 775), 25)

    pygame.display.flip()
    clock.tick(60)

    print(kelnerX,kelnerY)