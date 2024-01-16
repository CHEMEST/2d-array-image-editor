import pygame
import sys
import random

# Initialize & set up Pygame
pygame.init()
img = pygame.image.load("Assets/birds.jpg")  # Image here
width, height = img.get_size()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Image render")
clock = pygame.time.Clock()

"""
rgb = red, green, blue
ncw = not compatible with
Keybinds:
ctrl + c --> reset (de)enhance values
shift + w --> whiten/sharpen (ncw sort)
shift + s --> sort (ncw whiten & blur)
shift + g --> grayscale
shift + b --> blur/watercolor (ncw sort)
h + rgb --> deenhance color (h = hide)
e + rgb --> enhance color
"""

# Colors set up in Utilities.colors

# Create a 2D array for pixel values
pixel_array = [[0] * width for _ in range(height)]

# Populate the pixel array
for y in range(height):
    for x in range(width):
        pixel_array[y][x] = img.get_at((x, y))
# functions
def sort_2d_array_by_blue(colors):
    # Flatten the 2D array into a 1D list
    flattened_colors = [color for row in colors for color in row]

    # Define a custom sorting key based on the blue value of Color
    def blue_value(color):
        return color.b

    # Sort the flattened list based on the blue value
    sorted_colors = sorted(flattened_colors, key=blue_value)

    # Reshape the sorted list back to the original 2D array shape
    sorted_2d_array = [sorted_colors[i:i+len(colors[0])] for i in range(0, len(sorted_colors), len(colors[0]))]

    return sorted_2d_array

# Main game loop
toWhiteModifierValue = 20
blurModifierValue = 1

redEnhancerModifierValue = 0
greenEnhancerModifierValue = 0
blueEnhancerModifierValue = 0


redHiderModifierValue = 0
greenHiderModifierValue = 0
blueHiderModifierValue = 0
modified = False
run = True

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LCTRL]:
        redEnhancerModifierValue = 0
        greenEnhancerModifierValue = 0
        blueEnhancerModifierValue = 0

        redHiderModifierValue = 0
        greenHiderModifierValue = 0
        blueHiderModifierValue = 0
    if keys[pygame.K_w] and keys[pygame.K_LSHIFT]:
        for y in range(height):
            for x in range(width):
                pixelMod = random.randint(1, 3)
                modifierRed = random.randint(1, toWhiteModifierValue * pixelMod)
                modifierGreen = random.randint(1, toWhiteModifierValue * pixelMod)
                modifierBlue = random.randint(1, toWhiteModifierValue * pixelMod)
                r, g, b, a = pixel_array[y][x]
                pixel_array[y][x] = (min(r + modifierRed, 255), min(g + modifierGreen, 255), min(b + modifierBlue, 255), a)  # turn to white
        modified = True
    if keys[pygame.K_b] and keys[pygame.K_LSHIFT]:
        for y in range(height):
            for x in range(width):
                randomX = random.randint(-blurModifierValue, blurModifierValue)
                randomY = random.randint(-blurModifierValue, blurModifierValue)
                next_y = min(y + randomY, height - randomY)  # Ensure within height bounds
                next_x = min(x + randomX, width - randomX)   # Ensure within width bounds
                pixel_array[y][x] = pixel_array[next_y][next_x]
        modfied = True
    if keys[pygame.K_s] and keys[pygame.K_LSHIFT]:
        if not modified: # gets messed up if attempting to sort after it has been modified already
            pixel_array = sort_2d_array_by_blue(pixel_array)
    if keys[pygame.K_g] and keys[pygame.K_LSHIFT]:
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixel_array[y][x]
                grayScale = (r + g + b) / 3
                pixel_array[y][x] = (grayScale, grayScale, grayScale, a)
    # enhance
    if keys[pygame.K_r] and keys[pygame.K_e]:
        redEnhancerModifierValue += 1
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixel_array[y][x]
                pixel_array[y][x] = (min(r + redEnhancerModifierValue, 255), g, b, a)
    if keys[pygame.K_g] and keys[pygame.K_e]:
        greenEnhancerModifierValue += 1
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixel_array[y][x]
                pixel_array[y][x] = (r, min(g + greenEnhancerModifierValue, 255), b, a)
    if keys[pygame.K_b] and keys[pygame.K_e]:
        blueEnhancerModifierValue += 1
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixel_array[y][x]
                pixel_array[y][x] = (r, g, min(b + blueEnhancerModifierValue, 255), a)
    # denhance
    if keys[pygame.K_r] and keys[pygame.K_h]:
        redHiderModifierValue += 1
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixel_array[y][x]
                pixel_array[y][x] = (max(r - redHiderModifierValue, 1), g, b, a)
    if keys[pygame.K_g] and keys[pygame.K_h]:
        greenHiderModifierValue += 1
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixel_array[y][x]
                pixel_array[y][x] = (r, max(g - greenHiderModifierValue, 1), b, a)
    if keys[pygame.K_b] and keys[pygame.K_h]:
        blueHiderModifierValue += 1
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixel_array[y][x]
                pixel_array[y][x] = (r, g, max(b - blueHiderModifierValue, 1), a)
                

    # Your game logic goes here

    # Drawing code (if needed)
    for y in range(height):
        for x in range(width):
            screen.set_at((x, y), pixel_array[y][x])

    # Update the display
    pygame.display.flip()


pygame.quit()
sys.exit()
