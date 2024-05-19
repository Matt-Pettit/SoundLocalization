import pygame
from pygame.locals import *
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import matplotlib.backends.backend_agg as agg
import numpy as np
import random
from numpy import floor
import matplotlib.patches as mpatches
from matplotlib.legend_handler import HandlerTuple
import networkx as nx
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import time


start_time = time.time()  # Record the start time

######MATTTTTTTT!!!!! Hi
### the following needs to be updated with the actual section speeds the speed of the GUI processign is stored in execution_time


labels = ['GUI', 'TDOA', 'Calculations', 'Transmission'] #this must remain the same but tells you what order to put the speeds in

### for the grid comment out later when you have added the for realzies things
global x_grid
global y_grid
x_grid = 0.5
y_grid = 0.3
# Initialize Pygame
pygame.init()

# Set up the window dimensions
screen_width, screen_height = 1450, 850
screen = pygame.display.set_mode((screen_width, screen_height))
screen = pygame.display.get_surface()
pygame.display.set_caption("Sound Localisation UI)")

# Colors
background_color = (92, 92, 92)
block_color = (42, 46, 50)
text_color = (255, 255, 255)

# Font
font = pygame.font.Font(None, 36)

# Font sizes
main_text_size = 36
subtext_size = 24  # Adjust the subtext font size

# Fonts
main_font = pygame.font.Font(None, main_text_size)
subtext_font = pygame.font.Font(None, subtext_size)  # Create a font for subtext

#set up for initial animation
x = 350
y = 40
velocity = 10

imageBoom = pygame.image.load("boom.png")
scaled_boom = pygame.transform.scale(imageBoom, (70, 50))

###############################################################
### this creates the grid. only the position needs to be inputed, the x any y position must be updated with your stuff
def create_grid(x, y):
    # Code to Graph the Grid
    # Set the figure size in inches
    fig_width = 8*2.5 / 2.54  # Convert cm to inches
    fig_height = 5*2.5 / 2.54

    # Create a figure with the specified size
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Set the axis limits to match the grid dimensions
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 0.5)

    # Set the major grid interval to 50mm (0.05cm)
    ax.set_xticks([i * 0.05 for i in range(int(0.8 / 0.05) + 1)])
    ax.set_yticks([i * 0.05 for i in range(int(0.5 / 0.05) + 1)])

    # Add minor grid lines every 5mm (0.005cm)
    ax.set_xticks([i * 0.05 for i in range(int(0.8 / 0.05) + 1)], minor=True)
    ax.set_yticks([i * 0.05 for i in range(int(0.5 / 0.05) + 1)], minor=True)

    # Turn on the grid lines
    ax.grid(which='both')

    # Set the grid line style and color (e.g., RGB color: R=0.2, G=0.4, B=0.6)
    ax.xaxis.grid(True, linestyle='--', linewidth=0.5, color=(1, 1, 1))
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color=(1, 1, 1))

    # Set the background color (e.g., RGB color: R=0.8, G=0.8, B=0.8)
    fig.patch.set_facecolor((0.164, 0.18, 0.196))

    # Set the x-axis and y-axis line colors based on RGB values
    ax.spines['bottom'].set_edgecolor((1, 1, 1))  # RGB value
    ax.spines['left'].set_edgecolor((1, 1, 1))  # RGB value
    ax.spines['top'].set_edgecolor((1, 1, 1))  # RGB value
    ax.spines['right'].set_edgecolor((1, 1, 1))  # RGB value

    # Set the tick label colors based on RGB values
    ax.xaxis.set_tick_params(labelcolor=(1, 1, 1), color=(1, 1, 1))  # RGB value
    ax.yaxis.set_tick_params(labelcolor=(1, 1, 1), color=(1, 1, 1))  # RGB value

    # Set the x-axis and y-axis labels and their colors based on RGB values
    ax.set_xlabel('X-axis (cm)', color=(1, 1, 1))  # RGB value
    ax.set_ylabel('Y-axis (cm)', color=(1, 1, 1))  # RGB value

    # Define the position (x, y) for the yellow triangle marker

    # x_position = random.uniform(0,0.8)
    # y_position = random.uniform(0,0.5)

    x_position = x
    y_position = y

    # Plot the yellow triangle marker
    ax.scatter(x_position, y_position, marker='^', color='#ffc907', s=100)  # s is marker size

    # Add a label next to the marker with its position
    label_text = f'({x_position}, {y_position})'  # Format the label text
    ax.annotate(label_text, (x_position, y_position), textcoords="offset points", xytext=(5, 5), color='white')

    # Set the background color (e.g., RGB color: R=0.7, G=0.7, B=0.7)
    ax.set_facecolor((0.164, 0.18, 0.196))
    return fig

def renderGrid(x, y):
    if plt.get_fignums():
        plt.close('all')
    fig = create_grid(x, y)
    # Render the Matplotlib plot to a buffer
    canvas = agg.FigureCanvas(fig)
    canvas.draw()

    # Convert the Matplotlib buffer to a Pygame surface
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    matplotlib_surface = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(matplotlib_surface, (350, 175))  # You can adjust the position her

#####################################################################################

# def sort_speeds(speeds):
#     if len(speesd) != 4:
#         raise ValueError("Input array must contain exactly 4 elements")
#
#     arr.sort(reverse=True)
#     return speeds

def processingSpeeds(speeds, labels):

    combined_data = sorted(zip(speeds, labels), reverse=True)

    # Unzip the sorted data into separate lists
    sorted_speeds, sorted_labels = zip(*combined_data)
    #sort_speeds()
    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(2, 6))

    # Set the background color of the figure to RGB (100, 100, 100)
    fig.set_facecolor((0.164, 0.18, 0.196))  # RGB values should be in the [0, 1] range

    # Set the background color of the plot area to RGB (200, 200, 200)
    ax.set_facecolor((0.164, 0.18, 0.196))  # RGB values should be in the [0, 1] range
    # Set the x-axis and y-axis line colors based on RGB values
    ax.spines['bottom'].set_edgecolor((1, 1, 1))  # RGB value
    ax.spines['left'].set_edgecolor((1, 1, 1))  # RGB value
    ax.spines['top'].set_edgecolor((1, 1, 1))  # RGB value
    ax.spines['right'].set_edgecolor((1, 1, 1))  # RGB value

    # Set the x-axis and y-axis labels and their colors based on RGB values
    ax.set_xlabel('X-axis (cm)', color=(1, 1, 1))  # RGB value
    ax.set_ylabel('Y-axis (cm)', color=(1, 1, 1))  # RGB value

    # Define the coordinates for the centers of each quadrant
    x_coordinates = [0, 0, 0, 0]
    y_coordinates = [0, 0, 0, 0]

    # Sizes of the four bubbles
    # speeds = [1, 0.8, 0.5, 0.3]
    totalSpeed = sum(sorted_speeds)

    bubble_sizes = [floor((speed / totalSpeed) * 100000) for speed in sorted_speeds]

    # Define RGB values for the colors of the bubbles
    colors = [(255, 10, 0), (255, 95, 0), (255, 150, 7), (255, 201, 20)]  # Red, Green, Blue, Purple

    # Normalize the RGB values to the [0, 1] range
    colors = [(r / 255, g / 255, b / 255) for r, g, b in colors]

    # Create the bubble chart with specified colors and fully opaque bubbles
    scatter = ax.scatter(x_coordinates, y_coordinates, s=bubble_sizes, c=colors, alpha=1)

    # Set axis limits and disable logarithmic scaling
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_xscale('linear')
    ax.set_yscale('linear')

    # You can add labels and use the custom legend
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')

    # Create a legend explaining the colors
    sorted_labels = ['GUI', 'TDOA', 'Calculations', 'Transmission']
    legend_patches = [mpatches.Patch(color=color, label=label) for color, label in zip(colors, sorted_labels)]

    handler_map = {scatter: HandlerTuple(ndivide=None)}
    ax.legend(handles=legend_patches, loc='best', title='Legend', handler_map=handler_map)

    plt.figure(figsize=(3, 1000))
   
    return fig

def renderSpeeds(speeds, labels):
    if plt.get_fignums():
        plt.close('all')
    fig = processingSpeeds(speeds, labels)
    # Render the Matplotlib plot to a buffer
    canvas = agg.FigureCanvas(fig)
    canvas.draw()

    # Convert the Matplotlib buffer to a Pygame surface
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    matplotlib_surface = pygame.image.fromstring(raw_data, size, "RGB")
    
    screen.blit(matplotlib_surface, (1200, 175))  # adjust the position her

#####################################
#check if network is working
#### MATTT! the connection true or false should be put into this program, then change line
#242 and 243 to be connection_status = the inputeed arguments - uncomment the following lines
def piConnections(Pi1ConnectStatus, Pi2ConnectStatus):

#def piConnections():
    # Create a graph
    G = nx.Graph()
    
    # Add nodes for the laptop and Raspberry Pis
    G.add_node("Laptop")
    G.add_node("Raspberry Pi 1")
    G.add_node("Raspberry Pi 2")

    # Add edges to represent connections
    #G.add_edge(" ", "Pi 1", connection_status=False)
    #G.add_edge(" ", "Pi 2", connection_status=True)
    G.add_edge(" ", "Pi 1", connection_status=Pi1ConnectStatus)
    G.add_edge(" ", "Pi 2", connection_status=Pi2ConnectStatus)

    # Extract the connection statuses from the graph
    edge_colors = [G[u][v]['connection_status'] for u, v in G.edges()]

    # Create a color map for the edges (red for False, green for True)
    colors = ['red' if status is False else 'green' for status in edge_colors]

    # Create a dictionary to map node names to their respective images and sizes
    node_images = {
        " ": {"path": "laptop.png", "size": (0.0005, 0.0005)},  # Customize the size as needed
        "Pi 1": {"path": "raspberry_pi.png", "size": (0.0005, 0.0005)},  # Customize the size as needed
        "Pi 2": {"path": "raspberry_pi.png", "size": (0.0005, 0.0005)},  # Customize the size as needed
    }

    # Define the background color as an RGB value (e.g., light gray)
    background_color = (0.164, 0.18, 0.196)  # RGB value for light gray

    # Create a figure with a specified background color
    plt.figure(figsize=(2.5, 1.5), facecolor=background_color)

    # Load and draw custom node icons with specified sizes
    pos = nx.spring_layout(G)

    # Set the edge thickness based on connection status (e.g., thicker for True)
    edge_widths = [4 if status is True else 1 for status in edge_colors]

    # Draw the edges with specified widths
    nx.draw_networkx_edges(G, pos, edge_color=colors, width=edge_widths)


    nx.draw_networkx_edges(G, pos, edge_color=colors)
    nx.draw_networkx_labels(G, pos)
    for node, info in node_images.items():
        image = plt.imread(info["path"])
        imagebox = OffsetImage(image, zoom=0.03)  # You can adjust the zoom factor here
        ab = AnnotationBbox(imagebox, pos[node], frameon=False, pad=0)
        plt.gca().add_artist(ab)

    # Draw node labels
    labels = {node: node for node in G.nodes()}  # Use node names as labels
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=12, font_color='white')
    plt.gca().set_facecolor(background_color)
    
    return plt.gcf()

def renderConnections(stat1, stat2):
                # Check if there are existing Matplotlib figures and close them
    if plt.get_fignums():
        plt.close('all')
    fig = piConnections(stat1, stat2)
    plt.close(fig)
    #Render the Matplotlib plot to a buffer
    canvas = agg.FigureCanvas(fig)
    canvas.draw()

    #Convert the Matplotlib buffer to a Pygame surface
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    matplotlib_surface = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(matplotlib_surface, (50, 670))  # adjust the position her


#####################################
##Button 1
button_width = 200
button_height = 75
button1_x = 350
button1_y = 750
button_color = (42, 46, 50)  # RGB color for the button
button1_color = button_color
button2_color = button_color
button3_color = button_color
button4_color = button_color
text_color = (255, 255, 255)  # RGB color for the text on the button
font = pygame.font.Font(None, 36)  # You can choose a different font if you prefer
button1_text = "Quit"

def draw_button1():
    pygame.draw.rect(screen, button1_color, (button1_x, button1_y, button_width, button_height))
    text_surface = font.render(button1_text, True, text_color)
    text_rect = text_surface.get_rect(center=(button1_x + button_width // 2, button1_y + button_height // 2))
    screen.blit(text_surface, text_rect)

##Button 2

button2_x = 575
button2_y = 750
button2_text = "Start"

def draw_button2():
    pygame.draw.rect(screen, button2_color, (button2_x, button2_y, button_width, button_height))
    text_surface = font.render(button2_text, True, text_color)
    text_rect = text_surface.get_rect(center=(button2_x + button_width // 2, button2_y + button_height // 2))
    screen.blit(text_surface, text_rect)

##Button 3

button3_x = 800
button3_y = 750
button3_text = "Frequency"

def draw_button3():
    pygame.draw.rect(screen, button3_color, (button3_x, button3_y, button_width, button_height))
    text_surface = font.render(button3_text, True, text_color)
    text_rect = text_surface.get_rect(center=(button3_x + button_width // 2, button3_y + button_height // 2))
    screen.blit(text_surface, text_rect)

##Button 4
button4_width = 125
button4_x = 1025
button4_y = 750
button4_text = "Duration"

def draw_button4():
    pygame.draw.rect(screen, button4_color, (button4_x, button4_y, button4_width, button_height))
    text_surface = font.render(button4_text, True, text_color)
    text_rect = text_surface.get_rect(center=(button4_x + button4_width // 2, button4_y + button_height // 2))
    screen.blit(text_surface, text_rect)
###################

test_results = {
    "QUETO JENKINS": "JNKKET001",
    "MATT PETTIT": "PTTMAT005",
    "HOLLY LEWIS" : "LWSHOL001",
    "":"",
    "COURSE":"EEE3097S",
    "PROJECT":"ACOUSTIC TRIANGULATION"
}

def display_test_results():
    y = 200
    for test, result in test_results.items():
        text = font.render(f"{test}: {result}", True, "white")
        screen.blit(text, (40, y))
        y += 28

# Create a block class

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, text, subtext=""):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.color = color
        self.text = text
        self.subtext = subtext

    def update(self):
        pass

# Create a sprite group for the blocks
blocks = pygame.sprite.Group()

# Create three initial blocks (rectangles)
header = Block(25, 25, 1400, 75, block_color, "Sound Localisation", "EEE3097S DESIGN ")
ATP_block = Block(25, 125, 300, 450, block_color, "MEMBERS", "")
grid = Block(350, 125, 800, 600, block_color, "Grid Showing Calculated Sound Position","")
processing_speed = Block(1175, 125, 250, 700, block_color, "Processing Speed","")
connections = Block(25, 600, 300, 225, block_color, "Connections", "Nodes connected to Controller")
#accuracy_block = Block(350, 750, 800, 75, block_color, "Real Time Accuracy Graph")
blocks.add(header, ATP_block, grid, processing_speed, connections)

def beginRecording():
    ##### the code to start recording fgoes here :))
    return 1

# Game loop
update_timer = 10
update_delay = 10  # 2 seconds delay
running = True
button1_clicked = False
button2_clicked = False
button3_clicked = False
button4_clicked = False
end_time = time.time()  # Record the end time
execution_time = end_time - start_time
oldx, oldy = 0,0
while running:
    start_time = time.time() 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
            # Check if there are existing Matplotlib figures and close them
        if plt.get_fignums():
            plt.close('all')

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for left mouse button click
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if button1_x <= mouse_x <= button1_x + button_width and button1_y <= mouse_y <= button1_y + button_height:
                # The mouse click is inside the button's area
                button1_clicked = True
            if button2_x <= mouse_x <= button2_x + button_width and button2_y <= mouse_y <= button2_y + button_height:
                # The mouse click is inside the button's area
                button2_clicked = True
            if button3_x <= mouse_x <= button3_x + button_width and button3_y <= mouse_y <= button3_y + button_height:
                # The mouse click is inside the button's area
                button3_clicked = True
            if button4_x <= mouse_x <= button4_x + button4_width and button4_y <= mouse_y <= button4_y + button_height:
                # The mouse click is inside the button's area
                button4_clicked = True

    # Clear the screen
    screen.fill(background_color)

    # Draw the blocks and text
    for block in blocks:
        pygame.draw.rect(screen, block.color, block.rect)
        main_text_surface = main_font.render(block.text, True, text_color)
        #subtext_surface = subtext_font.render(block.subtext, True, text_color)  # Use subtext font
        if block.text == "Sound Localisation":
            font = pygame.font.Font(None, 15)
        screen.blit(main_text_surface, (block.rect.x + 10, block.rect.y + 10))
        #screen.blit(subtext_surface, (block.rect.x + 10, block.rect.y + 50))  # Adjust Y position

        if block.subtext:
            subtext_surface = subtext_font.render(block.subtext, True, text_color)
            screen.blit(subtext_surface, (block.rect.x + 10, block.rect.y + 50))  # Adjust Y position

    #little boom animation
    x += velocity
    if x > 1350:
        # Reset the image's position to the starting position
        x = 350

    screen.blit(scaled_boom, (x, y))

    # display ATPS
    display_test_results()

    # Blit the Matplotlib surface to the Pygame screen
    # info needed from file: x,y,pi12status,pi34status,tdoaspeed,calculationspeed,transmissionspeed
    ## READ INFO HERE
    file_path = 'data.txt'

    boolpi12status = False
    boolpi34status = False
# Read the file and split the values into variables
    tdoaspeed = 0
    calculationspeed = 0
    transmissionspeed = 0
    with open(file_path, 'r') as file:
        values = file.read().split(',')
        if len(values) == 7:
            if values[0] == "None" or values[1] == "None":
                x_grid,y_grid = oldx,oldy
            else:
                x_grid = float(values[0])
                y_grid = float(values[1])
                oldx,oldy = x_grid,y_grid
            pi12status = values[2]
            pi34status = values[3]
            tdoaspeed = float(values[4])
            calculationspeed = float(values[5])
            transmissionspeed = float(values[6])
    
    execution_time = time.time() - start_time
    speeds = [execution_time, tdoaspeed, calculationspeed, transmissionspeed] #delete later # always comes in ['GUI', 'TDOA', 'Calculations', 'Transmission'] 1, 0.8, 0.5,

    if pi12status == "Connected":
        boolpi12status = True
    if pi34status == "Connected":
        boolpi34status = True


    
    ### 
    GUITIme = end_time
    renderGrid(x_grid, y_grid)
    renderSpeeds(speeds, labels)
    renderConnections(boolpi12status,boolpi34status)
    draw_button1()
    draw_button2()
    draw_button3()
    draw_button4()

    if button1_clicked:
        # perform action
        button1_text = "Terminated"
        button1_color = "red"
        print("Program terminated!")
        running = False
    if button2_clicked:
        button2_color = "red"
        #START the recording action on the pies here
        button2_text = "in progress"
        beginRecording()
        print("Started!")
    if button3_clicked:
        # stop recording
        print("Recording Stopped!")
    if button4_clicked:
        # perform action
        print("Button4 Clicked!")
    
    display_test_results()


    # Update the display
    pygame.display.flip()

    pygame.time.delay(10)

pygame.quit()