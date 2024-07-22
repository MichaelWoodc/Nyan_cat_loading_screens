import pygame
import cv2
import numpy as np
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Webcam Display")

# Initialize webcams
num_cameras = 4  # Number of webcams to display
webcams = [cv2.VideoCapture(i) for i in range(num_cameras)]  # Open all available webcams

tile_rows = 2
tile_cols = 2

tile_width = screen_width // tile_cols
tile_height = screen_height // tile_rows

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for row in range(tile_rows):
        for col in range(tile_cols):
            idx = row * tile_cols + col

            ret, frame = webcams[idx].read()

            if not ret:
                print(f"Error reading frame from webcam {idx}.")
                break

            frame = cv2.resize(frame, (tile_width, tile_height))
            pygame_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pygame_frame = np.rot90(pygame_frame)
            pygame_frame = pygame.surfarray.make_surface(pygame_frame)

            x = col * tile_width
            y = row * tile_height

            screen.blit(pygame_frame, (x, y))

    pygame.display.flip()

# Release the webcams and quit
for webcam in webcams:
    webcam.release()

pygame.quit()
sys.exit()
