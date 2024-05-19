import pygame
import pygame.font
import random
import time
def readxy():
    x = None
    y = None
    file_path = 'data.txt'
    try:
        with open(file_path, 'r') as file:
            first_line = file.readline()
            values = first_line.split(',')

            try:
                if (values[0].strip() == "None" or values[1].strip() == "None"):
                    x, y = None, None
                    return x, y
            except:
                x, y = None, None
            if len(values) >= 2:
                x = float(values[0].strip())
                y = float(values[1].strip())
            else:
                print("File does not contain at least 2 comma-separated values on the first line.")
    except FileNotFoundError:
        return None, None
    return x, y

def init():
    pygame.font.init()
    width, height = 800, 500
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    screen.fill((110, 108, 104))
    return screen, clock

def drawgrid(screen):
    width, height = 800, 500

    for x in range(0, width, 100):
        pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height))
    for y in range(0, height, 100):
        pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y))

    for x in range(0, width, 100):
        text = str(x)
        text_surface = pygame.font.SysFont("Arial", 10).render(text, True, (0, 0, 0))
        screen.blit(text_surface, (x + 1, height - 20))
    for y in range(0, height, 100):
        text = str(y)
        y = 500 - y
        text_surface = pygame.font.SysFont("Arial", 10).render(text, True, (0, 0, 0))
        screen.blit(text_surface, (1, y + 1))

    pygame.display.update()

def drawcross(screen, x, y):
    width, height = 800, 500

    if x is None or y is None:
        return
    y = 500 - y
    pygame.draw.line(screen, (255, 0, 0), (x - 40, y), (x + 40, y), 2)
    pygame.draw.line(screen, (255, 0, 0), (x, y - 40), (x, y + 40), 2)
    text = str(x) + "," + str(y)
    text_surface = pygame.font.SysFont("Arial", 10).render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x, y))

    pygame.display.update()
def gui_runner():
    screen, clock = init()
    x, y = readxy()

    while True:
        xnew, ynew = readxy()
        if xnew is None or ynew is None:
            #print("Nothing")
            screen.fill((110, 108, 104))
            drawgrid(screen)
            clock.tick(60)
            continue
        else:
            x, y = xnew, ynew
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        screen.fill((110, 108, 104))
        drawgrid(screen)
        drawcross(screen, x, y)
        print("Drawing cross")
        clock.tick(60)

        # Add a delay here to avoid continuous polling of the file
        time.sleep(0.1)  # Adjust the delay time as needed

gui_runner()

