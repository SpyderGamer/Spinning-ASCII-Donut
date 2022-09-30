# Spinning Donut with Python.

import os
from math import cos, sin
import pygame
import colorsys

# Change Current Directory to Where this File is Saved (For Accessing Window Icon Asset).
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Colours.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
hue = 0

# Visual Settings.
os.environ["SDL_VIDEO_CENTERED"] = "1"
RES = WIDTH, HEIGHT = 800, 800
FPS = 60

# Screen Setup.
pixel_width = 20
pixel_height = 20
x_pixel = 0
y_pixel = 0
screen_width = WIDTH // pixel_width
screen_height = HEIGHT // pixel_height
screen_size = screen_width * screen_height

A, B = 0, 0

theta_spacing = 10
phi_spacing = 3

chars = ".,-~:;=!*#$@"

R1 = 10
R2 = 20
K2 = 200
K1 = screen_height * K2 * 3 / (8 * (R1 + R2))

pygame.init()

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20, bold = True)

# Function to Turn HSV Values to RGB Values.
def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Function to Display Text on the Screen.
def text_display(char, x, y):
    text = font.render(str(char), True, hsv2rgb(hue, 1, 1))
    text_rect = text.get_rect(center = (x, y))
    screen.blit(text, text_rect)

k = 0

# Setting a Custom Icon for the Pygame Window.
try:
    pygame_icon = pygame.image.load("PygameIcon.png")
    pygame.display.set_icon(pygame_icon)
except:
    # Return a Custom Error Instead of Crashing the Whole Program.
    print("[Error] Pygame Window Icon Wasn't Found.")
    print("[Error] Maybe PygameIcon.png Does Not Exist in the Correct Directory?")

# Run the Program.
running = True
while running:
    clock.tick(FPS)
    pygame.display.set_caption("Spinning Donut! | FPS: {:.2f}".format(clock.get_fps()))
    screen.fill(BLACK)

    output = [" "] * screen_size
    zbuffer = [0] * screen_size

    for theta in range(0, 628, theta_spacing):
        for phi in range(0, 628, phi_spacing):
            # Math Stuff...
            cosA = cos(A)
            sinA = sin(A)
            cosB = cos(B)
            sinB = sin(B)

            costheta = cos(theta)
            sintheta = sin(theta)
            cosphi = cos(phi)
            sinphi = sin(phi)

            # x, y Coords Before Revolving.
            circlex = R2 + R1 * costheta
            circley = R1 * sintheta

            # 3D (x, y, z) Coords After Rotation.
            x = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z = K2 + cosA * circlex * sinphi + circley * sinA
            ooz = 1 / z # One Over Z.

            # x, y Projection.
            xp = int(screen_width / 2 + K1 * ooz * x)
            yp = int(screen_height / 2 - K1 * ooz * y)

            position = xp + screen_width * yp

            # Luminance.
            L = cosphi * costheta * sinB - cosA * costheta * sinphi - sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

            if ooz > zbuffer[position]:
                zbuffer[position] = ooz # Larger ooz Means the Pixel is Closer to the Viewer than What's Already Plotted.
                luminance_index = int(L * 8) # We Multiply by 8 to Get luminance_index range 0-11 (8 * sqrt(2) = 11).
                output[position] = chars[luminance_index if luminance_index > 0 else 0]

    for i in range(screen_height):
        y_pixel += pixel_height
        for j in range(screen_width):
            x_pixel += pixel_width
            text_display(output[k], x_pixel, y_pixel)
            # text_display("FPS: {:.2f}".format(clock.get_fps()), 700, 700)
            k += 1
        x_pixel = 0
    y_pixel = 0
    k = 0

    # Rotation Values.
    A += 0.15
    B += 0.035

    hue += 0.005

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Pressing the ESC Key will Terminate the Process.
            if event.key == pygame.K_ESCAPE:
                running = False