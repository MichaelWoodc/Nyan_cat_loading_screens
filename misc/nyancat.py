import pygame
import sys
from moviepy.editor import VideoFileClip
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize Pygame
pygame.init()

# Function to set the system volume
def set_system_volume(volume):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume_object = cast(interface, POINTER(IAudioEndpointVolume))
    volume_object.SetMasterVolumeLevelScalar(volume, None)

# Set the desired volume level (0.0 to 1.0)
desired_volume = 0.3  # Adjust as needed

# Set the system volume
set_system_volume(desired_volume)

# Get the display width and height
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
image_velocity = 0.4

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Create the fullscreen screen
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Dynamic GIF Animation")

# Load the audio file
pygame.mixer.init()
audio = pygame.mixer.Sound('nyanCatSound.mp3')  # Replace 'nyanCatSound.mp3' with your audio file
audio.set_volume(100.0)  # Set initial volume to 0

# Load the video clip
clip = VideoFileClip('nyanCat2.gif')  # Replace 'nyanCat2.gif' with your GIF file

# Convert the clip frames to Pygame surfaces
frames = [pygame.surfarray.make_surface(np.array(frame)) for frame in clip.iter_frames()]

# Initial position of the image
image_x = (-clip.size[0]) - 1000
image_y = ((screen_height - clip.size[1]) // 2) - 100

# Flags to control flipping and rotating
flip_horizontal = True  # Flip horizontally
flip_vertical = False
rotate_clockwise = 90  # Rotate by 90 degrees

# Load a font for text rendering
font = pygame.font.Font(None, 200)

# Load the additional image
additional_image = pygame.image.load('faculty_photos/10.jpg')  # Adjust path as needed
additional_image = pygame.transform.scale(additional_image, (300, 300))

# Initial offset for the additional image
additional_image_offset_x = 600
additional_image_offset_y = 0

# Game loop
clock = pygame.time.Clock()
running = True

frame_index = 0  # To keep track of the current frame

# Calculate the frame update delay based on the desired playback speed
playback_speed = 0.8  # Slow down playback speed to a tenth
frame_update_delay = int((1 / clip.fps) / playback_speed * 1000)  # Delay in milliseconds

last_frame_update_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = pygame.time.get_ticks()

    # Update the frame index if the time delay has passed
    if current_time - last_frame_update_time >= frame_update_delay:
        last_frame_update_time = current_time
        frame_index = (frame_index + 1) % len(frames)

    # Clear the screen
    screen.fill(white)

    # Get the current frame from the list
    frame = frames[frame_index]

    # Apply transformations if needed
    transformed_frame = frame
    if flip_horizontal:
        transformed_frame = pygame.transform.flip(transformed_frame, True, False)
    if flip_vertical:
        transformed_frame = pygame.transform.flip(transformed_frame, False, True)
    if rotate_clockwise:
        transformed_frame = pygame.transform.rotate(transformed_frame, rotate_clockwise)

    # Calculate the transformed rectangle's position and size for the GIF image
    transformed_rect = transformed_frame.get_rect(center=(image_x + clip.size[0] / 2, image_y + clip.size[1] / 2))

    # Calculate the position for the additional image
    additional_image_rect = additional_image.get_rect(
        center=(transformed_rect.centerx + additional_image_offset_x, transformed_rect.centery + additional_image_offset_y)
    )

    # Draw the transformed frame
    screen.blit(transformed_frame, transformed_rect)

    # Draw the additional image
    screen.blit(additional_image, additional_image_rect)

    # Render 'Loading...' text
    text_surface = font.render('Loading...', True, black)
    text_rect = text_surface.get_rect(center=((screen_width/2)-300,(screen_height/2)+100))

    # Draw the text
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

    # Adjust audio volume based on image position
    audio_pan = 1  # max(-1.0, min(1.0, (image_x / screen_width * 2) - 1.0))
    audio.set_volume(1.0)  # Mute the audio first
    audio.set_volume(1.0 * (audio_pan + 1) / 2)  # Adjust volume based on position

    # Play the audio
    if not pygame.mixer.get_busy():
        audio.play()

    # Limit the frame rate
    clock.tick(60)  # You can adjust this value to control the frame rate

    # Move the image_x position based on the speed and playback speed
    image_x += (clip.size[0] / (clip.fps / image_velocity)) * (frame_update_delay / 1000)

    # Check if the animation has completed
    if image_x > screen_width:
        running = False

# Load and play the video after the image animation
video_clip = VideoFileClip('rickRolled.mp4')  # Replace 'rickRolled.mp4' with your video file
video_clip.preview(fps=30)  # Remove fullscreen=True

pygame.quit()
sys.exit()
