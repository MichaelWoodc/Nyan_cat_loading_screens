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
pygame.display.set_caption("Webcam Scroll")

# Initialize webcams
num_cameras = 4  # Number of webcams to display
webcams = [cv2.VideoCapture(i) for i in range(num_cameras)]  # Open all available webcams

current_camera = 0
display_time_per_camera = 5  # Display time for each camera in seconds

last_switch_time = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    current_time = pygame.time.get_ticks()
    if current_time - last_switch_time >= display_time_per_camera * 1000:
        last_switch_time = current_time
        current_camera = (current_camera + 1) % num_cameras

    ret, frame = webcams[current_camera].read()

    if not ret:
        print(f"Error reading frame from webcam {current_camera}. Skipping...")
        current_camera = (current_camera + 1) % num_cameras
        continue

    frame = cv2.resize(frame, (screen_width, screen_height))
    pygame_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pygame_frame = np.rot90(pygame_frame)
    pygame_frame = pygame.surfarray.make_surface(pygame_frame)

    screen.blit(pygame_frame, (0, 0))
    pygame.display.flip()

# Release the webcams and quit
for webcam in webcams:
    webcam.release()

pygame.quit()
sys.exit()
