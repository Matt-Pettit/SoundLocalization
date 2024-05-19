import pygame
import pygame.font
import random



def readxy():
    x = None
    y = None
    file_path = 'data.txt'
    # Open the file
    try:
        with open(file_path, 'r') as file:
            # Read the first line
            first_line = file.readline()
            
            # Split the first line by comma
            values = first_line.split(',')

            try:
                if (values[0].strip() == "None" or values[1].strip() == "None"):
                    x,y = None,None
                    return(x,y)
            except:
                x,y = None,None
            # Check if there are at least 2 values
            if len(values) >= 2:
                # Assign the first two values to x and y
                x = float(values[0].strip())
                y = float(values[1].strip())
            else:
                print("File does not contain at least 2 comma-separated values on the first line.")
    except FileNotFoundError:
        return None,None
    return x,y








# Initialize the font module
pygame.font.init()

# Define the size of the A1 grid
width, height = 594,841
width, height = 841,594
# Create a new Pygame window
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
# Set the background color
screen.fill((110, 108, 104))

# Draw the grid lines
xlabels = []
ylabels = []
for x in range(0, width, 60):
    
    pygame.draw.line(screen, (0, 0, 0), (x, 0), (x, height))
for y in range(0, height, 60):
    pygame.draw.line(screen, (0, 0, 0), (0, y), (width, y))

# Label the a
for x in range(0, width, 60):
    text =str(x)
    #pygame.draw.rect(screen, (0, 0, 0), (x_pos, y_pos, 42, 20))
    text_surface = pygame.font.SysFont("Arial", 10).render(text, True, (0, 0, 0))
    screen.blit(text_surface, (x + 1, 1))
for y in range(0, height, 60):
    text = str(y)

    #pygame.draw.rect(screen, (0, 0, 0), (x_pos, y_pos, 20, 42))
    text_surface = pygame.font.SysFont("Arial", 10).render(text, True, (0, 0, 0))
    screen.blit(text_surface, (1, y + 1))

# Randomly generate the coordinates of the crosshair
x = int(random.randrange(0, width))
y = int(random.randrange(0, height))

# Draw the crosshair
pygame.draw.line(screen, (255, 0, 0), (x-40, y), (x + 40, y), 2)
pygame.draw.line(screen, (255, 0, 0), (x, y-40), (x, y + 40), 2)

# Update the display
pygame.display.update()

# Keep the window open until the user closes it
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        # Draw the crosshair
    #x = int(random.randrange(0, width))
   # y = int(random.randrange(0, height))
    #pygame.draw.line(screen, (255, 0, 0), (x-40, y), (x + 40, y), 2)
    #pygame.draw.line(screen, (255, 0, 0), (x, y-40), (x, y + 40), 2)
    pygame.display.update()
    clock.tick(60)
